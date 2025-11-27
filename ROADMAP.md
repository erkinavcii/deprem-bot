# 🗺️ Deprem Botu Yol Haritası (Roadmap) / Earthquake Bot Roadmap

[TR] Bu proje, kişisel kullanım için geliştirilmiş, sunucusuz (serverless) çalışan bir deprem takip botudur.
[EN] This project is a personal, serverless earthquake tracking bot developed for real-time notifications.

---

## 🇹🇷 Türkçe (Turkish)

### ✅ Tamamlanan Özellikler (v1.0 - v2.0)
- [x] **Temel Takip:** Kandilli Rasathanesi verilerini çekme (API).
- [x] **Akıllı Filtreleme:** Büyüklük (4.0+) ve Zaman (Son 20dk) kontrolü.
- [x] **Konum Bazlı Uyarı:** Haversine formülü ile kullanıcıya olan mesafeyi ölçme (Örn: 500km çap).
- [x] **Güvenlik:** Koordinatların ve API anahtarlarının `GitHub Secrets` ile gizlenmesi.
- [x] **Anti-Ban:** `User-Agent Spoofing` ile tarayıcı taklidi yaparak engellenmeyi önleme.
- [x] **Heartbeat (Günlük Rapor):** Her sabah 09:00'da sistemin çalıştığını bildiren ve son 24 saatlik deprem istatistiklerini (Toplam, Max, Ort) sunan rapor.
- [x] **🖼️ Statik Harita Görseli:** Bildirim mesajlarına, depremin ve kullanıcının konumunu gösteren harita görseli (Geoapify) eklendi.
- [x] **🧠 Akıllı Artçı Filtresi (Rate Limiting):** Çok sayıda artçı olduğunda ilk 5 tanesini detaylı, geri kalanını "Özet Mesaj" olarak ileterek bildirim kirliliği önlendi.
- [x] **Hata Yönetimi (Error Handling):** API kesintilerinde veya hatalı verilerde sistemin çökmemesi ve kullanıcıya bilgi vermesi sağlandı.

### 🚀 Planlanan Geliştirmeler (Backlog)
1. **🎛️ Telegram Üzerinden Uzaktan Ayar:** Kod değiştirmeden, Telegram grubuna sabitlenen (pinned) bir mesaj ile botun ayarlarını değiştirme yeteneği.
2. **🏙️ En Yakın Şehir Detayı:** Koordinatın hangi ilçe sınırlarında kaldığını harici API ile doğrulamak (Opsiyonel).

---

## 🇬🇧 English

### ✅ Completed Features (v1.0 - v2.0)
- [x] **Basic Tracking:** Fetching data from Kandilli Observatory API.
- [x] **Smart Filtering:** Checks for Magnitude (4.0+) and Time (Last 20m).
- [x] **Location-Based Warning:** Calculating distance relative to the user via Haversine formula (e.g., 500km radius).
- [x] **Security:** Hiding sensitive coordinates and API tokens via `GitHub Secrets`.
- [x] **Anti-Ban:** Preventing IP blocking via `User-Agent Spoofing` (Browser Mimicking).
- [x] **Heartbeat (Daily Report):** Sends a "System Active" report at 09:00 AM daily with 24h earthquake stats.
- [x] **🖼️ Static Map Image:** Visual map attached to notifications showing epicenter and user location via Geoapify.
- [x] **🧠 Smart Aftershock Filter:** Implemented rate limiting (Top 5 + Summary) to prevent notification flooding during seismic storms.
- [x] **Robust Error Handling:** Fallback mechanisms for API failures and network errors.

### 🚀 Planned Enhancements (Backlog)
1. **🎛️ Remote Config via Telegram:** Ability to update bot settings (location, radius) by simply "pinning" a message in the Telegram chat.
2. **🏙️ Reverse Geocoding:** Verifying exact district/city details via external mapping APIs (Optional).