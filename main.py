import requests
import json
import os
import math
import sys
from datetime import datetime, timedelta, timezone

# Yerelde çalışırken .env yükle
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- AYARLAR ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"

# FİLTRELER
MIN_MAGNITUDE = 4.0
CHECK_INTERVAL = 20
MAX_DISTANCE_KM = 500
MESSAGE_LIMIT = 5  # En fazla kaç detaylı mesaj atılsın?

# Koordinat Kontrolü
try:
    MY_LAT = float(os.getenv("MY_LAT"))
    MY_LON = float(os.getenv("MY_LON"))
except (TypeError, ValueError):
    print("❌ HATA: Koordinatlar eksik!")
    sys.exit(1)

# --- MATEMATİKSEL FONKSİYONLAR ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def get_earthquake_data():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(API_URL, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                return data["result"]
    except Exception as e:
        print(f"Hata: {e}")
    return []

# --- GÜNLÜK RAPOR ---
def check_daily_report(earthquakes, now_tr):
    if not (now_tr.hour == 9 and 0 <= now_tr.minute <= 20):
        return

    print("☕ Günlük rapor hazırlanıyor...")
    
    count_24h = 0
    max_mag_24h = 0.0
    total_mag_sum = 0.0
    
    for eq in earthquakes:
        try:
            date_str = eq["date_time"]
            eq_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            diff_hours = (now_tr - eq_time).total_seconds() / 3600
            
            if diff_hours > 24: continue
                
            eq_lon = eq["geojson"]["coordinates"][0]
            eq_lat = eq["geojson"]["coordinates"][1]
            dist = calculate_distance(MY_LAT, MY_LON, eq_lat, eq_lon)
            
            if dist <= MAX_DISTANCE_KM:
                mag = float(eq["mag"])
                count_24h += 1
                total_mag_sum += mag
                if mag > max_mag_24h: max_mag_24h = mag
        except:
            continue
            
    avg_mag = 0
    if count_24h > 0:
        avg_mag = total_mag_sum / count_24h

    msg = (
        f"☀️ **GÜNAYDIN! SİSTEM AKTİF.**\n\n"
        f"Son 24 saatte senin {MAX_DISTANCE_KM}km çevrende:\n"
        f"📊 Toplam **{count_24h}** sarsıntı oldu.\n"
        f"📈 En büyüğü: **{max_mag_24h}**\n"
        f"➗ Ortalama: **{avg_mag:.2f}**\n\n"
        f"Nöbetteyim, güvendesin. 🤖"
    )
    send_telegram(msg)
    print("✅ Günlük rapor gönderildi.")

# --- ANLIK KONTROL (LİMİTLİ) ---
def check_new_earthquakes(earthquakes, now_tr):
    # 1. Havuz (Toplama)
    valid_quakes = []

    for eq in earthquakes:
        try:
            mag = float(eq["mag"])
            title = eq["title"]
            date_str = eq["date_time"]
            depth = eq["depth"]
            
            eq_lon = eq["geojson"]["coordinates"][0]
            eq_lat = eq["geojson"]["coordinates"][1]
            dist_km = calculate_distance(MY_LAT, MY_LON, eq_lat, eq_lon)
            
            eq_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            diff_minutes = (now_tr - eq_time).total_seconds() / 60
            
            # Filtreleme
            if dist_km <= MAX_DISTANCE_KM and mag >= MIN_MAGNITUDE and 0 <= diff_minutes <= CHECK_INTERVAL:
                # Tüm veriyi bir sözlük (dict) olarak listeye atıyoruz
                valid_quakes.append({
                    "mag": mag,
                    "title": title,
                    "date": date_str,
                    "depth": depth,
                    "dist": dist_km
                })
        except:
            continue

    if not valid_quakes:
        print("Anlık risk yok.")
        return

    # 2. Sıralama (En büyükten en küçüğe)
    # 'mag' anahtarına göre ters (reverse) sırala
    valid_quakes.sort(key=lambda x: x["mag"], reverse=True)

    # 3. Dilimleme (Slicing)
    top_quakes = valid_quakes[:MESSAGE_LIMIT]      # İlk 5
    remaining_quakes = valid_quakes[MESSAGE_LIMIT:] # Geriye kalanlar

    print(f"⚠ Toplam {len(valid_quakes)} deprem bulundu. İlk {len(top_quakes)} tanesi gönderiliyor.")

    # 4. Detaylı Mesajları Gönder
    for q in top_quakes:
        msg = (
            f"🚨 **DEPREM UYARISI!**\n\n"
            f"📍 **Yer:** {q['title']}\n"
            f"📏 **Mesafe:** {int(q['dist'])} km\n"
            f"📉 **Büyüklük:** {q['mag']}\n"
            f"🕒 **Saat:** {q['date']}\n"
            f"⚠ **Derinlik:** {q['depth']} km"
        )
        send_telegram(msg)

    # 5. Özet Mesaj (Eğer limit aşıldıysa)
    if remaining_quakes:
        count_rem = len(remaining_quakes)
        max_rem = max(q["mag"] for q in remaining_quakes)
        
        summary_msg = (
            f"⚠️ **DİKKAT:** Bölgede yoğun hareketlilik var.\n\n"
            f"Yukarıdakilere ek olarak **{count_rem} adet** daha sarsıntı tespit edildi.\n"
            f"Bunların en büyüğü: **{max_rem}** büyüklüğünde.\n"
            f"Lütfen tedbirli olun."
        )
        send_telegram(summary_msg)
        print(f"➕ Ekstra {count_rem} deprem için özet geçildi.")

if __name__ == "__main__":
    now_tr = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=3)
    print(f"🕒 Sistem Saati (TR): {now_tr.strftime('%H:%M')}")
    
    quakes = get_earthquake_data()
    
    if quakes:
        check_daily_report(quakes, now_tr)
        check_new_earthquakes(quakes, now_tr)
    else:
        print("Veri çekilemedi.")