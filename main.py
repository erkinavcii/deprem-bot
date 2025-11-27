import requests
import json
import os
import math
import sys
from datetime import datetime, timedelta

# Yerelde çalışırken .env dosyasını yükle
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- KULLANICI AYARLARI ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


try:
    MY_LAT = float(os.getenv("MY_LAT"))
    MY_LON = float(os.getenv("MY_LON"))
except (TypeError, ValueError):
    print("❌ HATA: Koordinatlar (MY_LAT, MY_LON) bulunamadı veya hatalı!")
    sys.exit(1) # Kodu durdur

# FİLTRELER
MAX_DISTANCE_KM = 500 # Sadece 500 km çapındakileri bildir
MIN_MAGNITUDE = 4.0   # Büyüklük sınırı
CHECK_INTERVAL = 20   # Son 20 dakikadaki depremler

API_URL = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"

# --- MATEMATİKSEL MESAFE HESAPLAMA (HAVERSINE FORMÜLÜ) ---
def calculate_distance(lat1, lon1, lat2, lon2):
    # Dünya'nın yarıçapı (km)
    R = 6371  
    
    # Dereceyi radyana çevir
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
         
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram ayarları eksik!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Telegram bildirimi gönderildi.")
    except Exception as e:
        print(f"❌ Telegram hatası: {e}")

def check_earthquakes():
    print(f"📡 Konumuna ({MAX_DISTANCE_KM}km) yakın depremler taranıyor...")
    
    try:
        response = requests.get(API_URL, timeout=15)
        if response.status_code != 200:
            print(f"❌ API Hatası: {response.status_code}") 
            return
        data = response.json()
        if not data.get("status"):
            print("❌ API verisi hatalı.")
            return
        earthquakes = data["result"]
    except Exception as e:
        print(f"❌ Veri çekme hatası: {e}")
        return

    # Türkiye saati ayarı (UTC+3)
    now_tr = datetime.utcnow() + timedelta(hours=3)
    
    found_any = False

    for eq in earthquakes:
        try:
            mag = float(eq["mag"])
            title = eq["title"]
            date_str = eq["date_time"]
            depth = eq["depth"]
            
            # Koordinatları al
            # GeoJSON formatında önce Boylam(0), sonra Enlem(1) gelir.
            eq_lon = eq["geojson"]["coordinates"][0]
            eq_lat = eq["geojson"]["coordinates"][1]
            
            # Mesafeyi Hesapla
            dist_km = calculate_distance(MY_LAT, MY_LON, eq_lat, eq_lon)
            
            # Zaman Farkı
            eq_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            diff_minutes = (now_tr - eq_time).total_seconds() / 60
            
            # --- ANA KONTROL ---
            # 1. Mesafe sınırın içindeyse
            # 2. Büyüklük yeterliyse
            # 3. Yeni olduysa
            
            if dist_km <= MAX_DISTANCE_KM and mag >= MIN_MAGNITUDE and 0 <= diff_minutes <= CHECK_INTERVAL:
                
                msg = (
                    f"🚨 **DEPREM UYARISI!**\n\n"
                    f"📍 **Yer:** {title}\n"
                    f"📏 **Mesafe:** {int(dist_km)} km ötede\n"
                    f"📉 **Büyüklük:** {mag}\n"
                    f"🕒 **Saat:** {date_str}\n"
                    f"⚠ **Derinlik:** {depth} km"
                )
                
                print(f"⚠ TESPİT: {title} - {int(dist_km)}km uzaklıkta.")
                send_telegram(msg)
                found_any = True
                
        except Exception as e:
            continue

    if not found_any:
        print("Yakınlarda kriterlere uyan tehlikeli bir durum yok.")

if __name__ == "__main__":
    check_earthquakes()