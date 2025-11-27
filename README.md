# 🌍 Deprem Takip Botu / Earthquake Tracking Bot

![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat&logo=python)
![Platform](https://img.shields.io/badge/Platform-GitHub%20Actions-2088FF?style=flat&logo=github-actions)
![License](https://img.shields.io/badge/License-MIT-green)

**[TR]** Kişisel kullanım için geliştirilmiş, sunucu maliyeti olmayan, konum tabanlı ve günlük raporlama yapan Python tabanlı deprem takip botu.
<br>
**[EN]** A personal, serverless, location-based earthquake tracking bot powered by Python and GitHub Actions with daily reporting features.

---

## 🇹🇷 Proje Hakkında (Turkish)

Bu proje, **Kandilli Rasathanesi** verilerini kullanarak belirlediğiniz konum ve yarıçap içerisindeki depremleri anlık olarak takip eder ve **Telegram** üzerinden size bildirir. En önemli özelliği, **GitHub Actions** altyapısını kullandığı için 7/24 çalışması için herhangi bir sunucuya (VPS/Raspberry Pi) veya bilgisayara ihtiyaç duymamasıdır.

### ✨ Özellikler
* **Sunucusuz Mimari:** GitHub Actions üzerinde CRON job olarak çalışır (Her 15 dakikada bir).
* **Konum Filtresi:** Haversine formülü ile sizin konumunuza olan mesafeyi ölçer (Örn: Sadece 500km çapındakileri bildir).
* **Haritalı Bildirim:** Depremin merkez üssünü ve sizin konumunuzu gösteren görsel harita ekler (Geoapify).
* **Akıllı Bildirim:** Sadece belirlediğiniz büyüklük (Örn: 4.0+) üzerindeki depremleri bildirir.
* **Spam Koruması:** Yoğun artçı sarsıntılarda mesaj kirliliğini önlemek için akıllı özetleme yapar (İlk 5 detaylı, gerisi özet).
* **Heartbeat (Günlük Rapor):** Her sabah 09:00'da sistemin çalıştığını teyit eder ve son 24 saatin istatistiklerini raporlar.
* **Güvenlik:** Hassas veriler GitHub Secrets içerisinde şifreli saklanır.
* **Anti-Ban:** `User-Agent Spoofing` tekniği ile API engellemelerine karşı korumalıdır.

---

## 🇬🇧 About Project (English)

This project tracks real-time earthquake data from **Kandilli Observatory**, filters it based on your location radius, and sends notifications via **Telegram**. Its key feature is running entirely on **GitHub Actions**, meaning it requires no dedicated server, VPS, or always-on computer.

### ✨ Features
* **Serverless Architecture:** Runs as a CRON job on GitHub Actions (Every 15 minutes).
* **Location Filter:** Uses Haversine formula to calculate distance to user (e.g., alert only within 500km radius).
* **Visual Maps:** Attaches a static map image showing the epicenter and your location (Geoapify).
* **Smart Alerts:** Notifications only for earthquakes above a specific magnitude (e.g., 4.0+).
* **Spam Protection:** Summarizes notifications during seismic storms to prevent flooding (Top 5 detailed, rest summarized).
* **Heartbeat (Daily Report):** Sends a "System Active" confirmation at 09:00 AM daily with 24h statistics.
* **Security:** Sensitive data is stored securely in GitHub Secrets.
* **Anti-Ban:** Implements `User-Agent Spoofing` to prevent API blocking.

---

## ⚙️ Kurulum / Installation

### 1. Fork this Repository
**[TR]** Bu projeyi kendi GitHub hesabınıza **Fork** edin (Sağ üstteki buton).
<br>
**[EN]** **Fork** this project to your own GitHub account (Button on top right).

### 2. Telegram Bot Setup
**[TR]**
1. Telegram'da `@BotFather` ile konuşarak yeni bir bot oluşturun ve **Token** alın.
2. `@userinfobot` ile konuşarak kendi **Chat ID**'nizi öğrenin.

**[EN]**
1. Create a new bot via `@BotFather` on Telegram to get a **Token**.
2. Find your own **Chat ID** via `@userinfobot`.

### 3. Geoapify Setup (For Maps)
**[TR]** [Geoapify.com](https://www.geoapify.com/)'a üye olun, yeni bir proje oluşturun ve **API Key** alın (Ücretsizdir).
<br>
**[EN]** Sign up at [Geoapify.com](https://www.geoapify.com/), create a new project, and get an **API Key** (Free tier available).

### 4. GitHub Secrets Configuration
**[TR]** Reponuzun **Settings -> Secrets and variables -> Actions** kısmına giderek aşağıdaki "Repository Secret"ları ekleyin:
<br>
**[EN]** Go to **Settings -> Secrets and variables -> Actions** in your repository and add the following 'Repository Secrets':

| Secret Name | Description (Açıklama) | Example Value (Örnek) |
| :--- | :--- | :--- |
| `TELEGRAM_TOKEN` | BotFather'dan alınan token | `123456:ABC-Def...` |
| `TELEGRAM_CHAT_ID` | Sizin kullanıcı ID'niz | `987654321` |
| `MY_LAT` | Evinizin Enlemi (Latitude) | `41.00` (Istanbul Example) |
| `MY_LON` | Evinizin Boylamı (Longitude) | `28.97` (Istanbul Example) |
| `GEOAPIFY_API_KEY` | Harita Görseli için API Key | `aa7890abcdef...` |

### 5. Enable Actions
**[TR]** Reponuzdaki **Actions** sekmesine gidin ve workflow'ların çalışmasına izin verin (Enable). İlk çalıştırmayı manuel olarak "Run workflow" butonuyla yapabilirsiniz.
<br>
**[EN]** Go to the **Actions** tab in your repository and enable the workflows. You can trigger the first run manually using the "Run workflow" button.

---

## 🛠️ Configuration (Ayarlar)

Kod içerisindeki `main.py` dosyasında aşağıdaki sabitleri değiştirerek filtreleri özelleştirebilirsiniz:
<br>
You can customize filters by changing these constants in `main.py`:

```python
MIN_MAGNITUDE = 4.0   # Minimum magnitude to alert
CHECK_INTERVAL = 20   # Time window in minutes
MAX_DISTANCE_KM = 500 # Radius in Kilometers
MESSAGE_LIMIT = 5     # Max detailed messages per run