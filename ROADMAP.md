# 🗺️ Deprem Botu Yol Haritası (Roadmap) / Earthquake Bot Roadmap

[TR] Bu proje, kişisel kullanım için geliştirilmiş, sunucusuz (serverless) çalışan bir deprem takip botudur.
[EN] This project is a personal, serverless earthquake tracking bot developed for real-time notifications.

---

## 🇬🇧 English

### ✅ Completed Features (v1.0 - v1.2)
- [x] **Basic Tracking:** Fetching data from Kandilli Observatory API.
- [x] **Smart Filtering:** Checks for Magnitude (4.0+) and Time (Last 20m).
- [x] **Location-Based Warning:** Calculating distance relative to the user via Haversine formula (e.g., 500km radius).
- [x] **Security:** Hiding sensitive coordinates and API tokens via `GitHub Secrets`.
- [x] **Anti-Ban:** Preventing IP blocking via `User-Agent Spoofing` (Browser Mimicking).
- [x] **Heartbeat (Daily Report):** Sends a "System Active" report at 09:00 AM with 24h earthquake stats (Total, Max, Avg).
- [x] **Optimization:** O(1) space complexity for average calculations and Timezone fixes.

### 🚀 Planned Enhancements (Backlog)
1. **🖼️ Static Map Image:** Attaching a visual map image to the notification showing the epicenter and user location (Mapbox/Geoapify).
2. **🎛️ Remote Config via Telegram:** Ability to update bot settings (location, radius) by simply "pinning" a message in the Telegram chat, without changing code.
3. **🧠 Smart Aftershock Filter:** Analyzing and summarizing small tremors (aftershocks) following a major earthquake to reduce notification noise.
4. **🏙️ Reverse Geocoding:** verifying exact district/city details via external mapping APIs (Optional).

---

## 🇹🇷 Türkçe (Turkish)

### ✅ Tamamlanan Özellikler (v1.0 - v1.2)
- [x] **Temel Takip:** Kandilli Rasathanesi verilerini çekme (API).
- [x] **Akıllı Filtreleme:** Büyüklük (4.0+) ve Zaman (Son 20dk) kontrolü.
- [x] **Konum Bazlı Uyarı:** Haversine formülü ile kullanıcıya olan mesafeyi ölçme (Örn: 500km çap).
- [x] **Güvenlik:** Koordinatların ve API anahtarlarının `GitHub Secrets` ile gizlenmesi.
- [x] **Anti-Ban:** `User-Agent Spoofing` ile tarayıcı taklidi yaparak engellenmeyi önleme.
- [x] **Heartbeat (Günlük Rapor):** Her sabah 09:00'da sistemin çalıştığını bildiren ve son 24 saatlik deprem istatistiklerini (Toplam, Max, Ort) sunan rapor.
- [x] **Optimizasyon:** Ortalama hesaplamasında O(1) space complexity kullanımı ve Timezone düzeltmeleri.

### 🚀 Planlanan Geliştirmeler (Backlog)
1. **🖼️ Statik Harita Görseli (Static Map):** Bildirim mesajının altına, depremin merkez üssünü ve kullanıcının konumunu gösteren küçük bir harita görseli eklenecek.
2. **🎛️ Telegram Üzerinden Uzaktan Ayar:** Kod değiştirmeden, Telegram grubuna sabitlenen (pinned) bir mesaj ile botun ayarlarını değiştirme yeteneği.
3. **🧠 Akıllı Artçı Filtresi:** Büyük bir depremden sonra gelen yüzlerce küçük artçıyı analiz edip bildirim kirliliğini önlemek.
4. **🏙️ En Yakın Şehir Detayı:** Koordinatın hangi ilçe sınırlarında kaldığını harici API ile doğrulamak (Opsiyonel).


