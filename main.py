import requests
import json
import os
import sys
from datetime import datetime, timedelta

# Yerelde çalışırken .env dosyasını yükle
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
MIN_MAGNITUDE = 4.0   # 4.0 ve üzeri
CHECK_INTERVAL = 20   # Son 20 dakika

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram ayarları eksik! Mesaj atılamadı.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Telegram bildirimi gönderildi.")
    except Exception as e:
        print(f"❌ Telegram hatası: {e}")

def check_earthquakes():
    print("📡 Deprem verisi çekiliyor...")
    
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
        print(f"❌ Bağlantı sorunu: {e}")
        return

    # Şu anki Türkiye Saati (UTC+3)
    now_tr = datetime.utcnow() + timedelta(hours=3)
    
    found_any = False

    for eq in earthquakes:
        try:
            mag = float(eq["mag"])
            location = eq["title"]
            date_str = eq["date_time"]
            depth = eq["depth"]
            
            # Tarihi objeye çevir
            eq_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            
            # Ne kadar zaman önce oldu? (Dakika)
            diff_minutes = (now_tr - eq_time).total_seconds() / 60
            
            # --- KONTROL ---
            if mag >= MIN_MAGNITUDE and 0 <= diff_minutes <= CHECK_INTERVAL:
                msg = (
                    f"🚨 **DEPREM UYARISI!**\n\n"
                    f"📍 **Yer:** {location}\n"
                    f"📉 **Büyüklük:** {mag}\n"
                    f"🕒 **Saat:** {date_str}\n"
                    f"⚠ **Derinlik:** {depth} km"
                )
                print(f"⚠ TESPİT EDİLDİ: {location} ({mag})")
                send_telegram(msg)
                found_any = True
                
        except Exception as e:
            continue

    if not found_any:
        print(f"Son {CHECK_INTERVAL} dakikada {MIN_MAGNITUDE} üzeri deprem yok.")

if __name__ == "__main__":
    check_earthquakes()