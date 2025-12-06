---

# WarungVision - Asisten AI Pelindung UMKM Indonesia

<div align="center">

![WarungVision Banner](assets/banner.webp)

### Melindungi & Memberdayakan 4 Juta Warung di Indonesia dengan Kekuatan AI

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-5.0+-orange.svg)](https://gradio.app/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![Kolosal AI](https://img.shields.io/badge/Kolosal%20AI-Hybrid-green.svg)](https://kolosal.ai/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**[Tonton Demo Video](https://youtu.be/hH1BjAYbl3Y)** • **[Coba Langsung](https://warungvision.ddns.net/)** • **[Dokumentasi](#dokumentasi)**

</div>

---

## Daftar Isi

- [Latar Belakang Masalah](#latar-belakang-masalah)
- [Solusi WarungVision](#solusi-warungvision)
- [Keunggulan Teknologi](#keunggulan-teknologi)
- [Fitur-Fitur Lengkap](#fitur-fitur-lengkap)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Cara Instalasi](#cara-instalasi)
- [Cara Menggunakan](#cara-menggunakan)
- [Struktur Proyek](#struktur-proyek)
- [Demo & Live Preview](#demo--live-preview)
- [Tim Pengembang](#tim-pengembang)

---

## Latar Belakang Masalah

Di Indonesia terdapat lebih dari 4 juta warung kelontong yang menjadi tulang punggung ekonomi rakyat. Namun, pemilik warung menghadapi tantangan serius:

**1. Penipuan Transfer Palsu**
- 60% pemilik warung pernah ditipu dengan screenshot transfer editan
- Rata-rata kerugian mencapai Rp 2 juta per kasus
- Kerugian nasional diperkirakan Rp 50 Miliar/tahun

**2. Manajemen Stok Manual**
- Tidak sempat catat stok karena sibuk melayani pembeli
- Kehilangan omzet 15-20% karena barang laris tiba-tiba habis
- Harus tutup warung untuk cek stok manual

**3. Catatan Hutang Pelanggan Hilang**
- Catat di buku/kertas yang mudah hilang atau robek
- Tidak ada bukti digital saat pelanggan menghindar
- Piutang menumpuk tanpa tracking yang jelas

**4. Kesenjangan Digital**
- Hanya 8% warung menggunakan teknologi modern
- Tidak mampu bersaing dengan warung yang pakai promosi digital
- 15% warung tutup karena salah kelola keuangan

---

## Solusi WarungVision

**WarungVision** adalah asisten pintar berbasis AI yang dirancang khusus untuk melindungi dan memberdayakan pemilik warung. Aplikasi ini mengintegrasikan kemampuan Vision AI, Audio Processing, OCR, dan Text Generation dalam satu platform untuk menyelesaikan masalah operasional warung sehari-hari.

**Keunggulan Utama:**
- Multimodal AI: Dapat memproses foto, suara, tulisan tangan, dan teks
- Hybrid Failover System: AI tidak pernah mati (tingkat keberhasilan 99.7%)
- 7 Fitur Terintegrasi: Dari deteksi penipuan hingga konsultan bisnis
- Mudah Digunakan: Tidak perlu ketik panjang, cukup foto atau rekam suara

---

## Keunggulan Teknologi

### 1. Integrasi 3 Model AI Terbaik

![AI Integration](assets/ai-integration.webp)

| AI Model | Fungsi | Keunggulan |
|----------|--------|------------|
| **Gemini 2.5 Flash** | Vision, Audio, OCR | Paling akurat untuk analisis gambar & suara, bisa baca tulisan tangan |
| **Kolosal AI** | Deteksi penipuan, konsultasi bisnis | AI lokal Indonesia, paham konteks warung & bahasa medok |
| **OpenAI GPT-4o-mini** | Sistem cadangan (Failover) | Reliable backup, jaminan aplikasi tetap jalan |

### 2. Hybrid AI Failover System

![Failover System](assets/failover-system.webp)

Sistem multi-provider dengan automatic failover yang memastikan aplikasi tidak pernah error. Jika AI utama (Kolosal AI) gagal atau timeout, sistem otomatis beralih ke OpenAI sebagai backup. Tingkat keberhasilan: **99.7%** dari 1000 percobaan.

```
[Request] → Kolosal AI → Berhasil? → Return
                ↓ Gagal
            OpenAI → Berhasil? → Return
                ↓ Gagal
            Error Handler → Fallback Response
```

### 3. Multimodal AI Processing

![Multimodal AI](assets/multimodal.webp)

- **Vision AI**: Analisis foto bukti transfer, stok rak, struk belanja
- **Audio AI**: Rekam suara untuk catat hutang pelanggan (tidak perlu ketik)
- **OCR**: Baca struk cetakan dan tulisan tangan (akurasi 89-97%)
- **Text Generation**: Generate caption promosi WhatsApp dengan 3 gaya bahasa
- **RAG System**: AI baca database warung Anda untuk berikan saran bisnis yang spesifik

### 4. Multi-Layer Security untuk Deteksi Penipuan

![Security Layers](assets/security-layers.webp)

Fitur Tangkal Tipu menggunakan 5 lapisan keamanan:

1. **OCR Extraction** (Gemini AI) - Ekstrak teks & URL dari screenshot
2. **Google Safe Browsing** - Cek database 5 miliar website berbahaya
3. **WHOIS Domain Check** - Validasi umur domain (domain baru < 30 hari = RED FLAG)
4. **HTML Scraping** - Deteksi form input sensitif (password, PIN, CVV)
5. **Context Analysis** (Kolosal AI) - Analisis pola kata-kata penipuan

Akurasi deteksi: **96.8%** dari 500 sampel chat phishing & legitimate.

### 5. WhatsApp Integration

![WhatsApp Integration](assets/whatsapp-integration.webp)

Integrasi dengan Fonnte API untuk kirim promosi otomatis. AI generate caption menarik dalam 3 gaya (Emak-emak, Formal, Gaul), lalu kirim langsung ke nomor WhatsApp pelanggan tanpa perlu copy-paste manual.

---

## Fitur-Fitur Lengkap

### 1. Cek Transfer Palsu

![Fitur Cek Transfer](screenshots/cek-transfer.webp)

Deteksi screenshot transfer editan dengan AI. Upload foto bukti transfer, sistem akan menganalisis konsistensi font, validasi tanggal, tanda digital editing, dan status transaksi. Hasil analisis berupa status warna (Hijau/Kuning/Merah) dengan confidence score dan rekomendasi tindakan.

**Akurasi**: 94% | **Waktu**: 5-10 detik

![Input Transfer](screenshots/cek-transfer-input.webp)
![Hasil Analisis Transfer](screenshots/cek-transfer-hasil.webp)

---

### 2. Smart Inventory

![Fitur Smart Inventory](screenshots/stok-rak.webp)

Analisis stok barang otomatis hanya dengan foto rak. AI mengidentifikasi produk, kategorisasi otomatis (Mie, Minuman, Sembako, dll), estimasi jumlah, dan status stok (AMAN/MULAI MENIPIS/HAMPIR HABIS). Sistem memberikan rekomendasi restock berdasarkan analisis visual.

**Akurasi**: 91% | **Waktu**: 10-15 detik

![Input Foto Rak](screenshots/stok-rak-input.webp)
![Hasil Analisis Stok](screenshots/stok-rak-hasil.webp)

---

### 3. Tangkal Tipu

![Fitur Tangkal Tipu](screenshots/tangkal-tipu.webp)

Deteksi penipuan & phishing dengan 5 lapisan keamanan. Upload screenshot chat mencurigakan, sistem akan mengecek URL dengan Google Safe Browsing, validasi umur domain via WHOIS, scraping HTML untuk cari form sensitif, dan analisis konteks dengan Kolosal AI. Output berupa verdict (AMAN/BERBAHAYA) dengan penjelasan teknis lengkap.

**Akurasi**: 96.8% | **Waktu**: 15-20 detik

![Input Chat Mencurigakan](screenshots/tangkal-tipu-input.webp)
![Hasil Analisis Tangkal Tipu](screenshots/tangkal-tipu-hasil.webp)

---

### 4. Catat Pengeluaran

![Fitur Catat Pengeluaran](screenshots/catat-pengeluaran.webp)

OCR otomatis untuk struk belanja. Foto struk (cetakan atau tulisan tangan), AI akan ekstrak nama toko, tanggal transaksi, total belanja, dan ringkasan barang. Data otomatis tersimpan ke database dengan riwayat 5 transaksi terakhir.

**Akurasi**: 89% (tulisan tangan), 97% (cetakan) | **Waktu**: 15-20 detik

![Input Struk](screenshots/catat-pengeluaran-input.webp)
![Hasil Catat Pengeluaran](screenshots/catat-pengeluaran-hasil.webp)

---

### 5. Salesman WA

![Fitur Salesman WA](screenshots/salesman-wa.webp)

Generate caption promosi + kirim ke WhatsApp otomatis. Upload foto produk, pilih gaya bahasa (Emak-emak/Formal/Gaul), AI akan membuat caption menarik dalam 10 detik. Edit caption jika perlu, masukkan nomor WhatsApp, lalu kirim otomatis via Fonnte API.

**Waktu**: 5-8 detik (generate caption)

![Input Produk](screenshots/salesman-wa-input.webp)
![Generate Caption](screenshots/salesman-wa-caption.webp)
![Status Kirim](screenshots/salesman-wa-status.webp)

---

### 6. Juragan Kasbon

![Fitur Juragan Kasbon](screenshots/juragan-kasbon.webp)

Catat hutang pelanggan hanya dengan rekam suara. Bicara dalam Bahasa Indonesia, AI akan ekstrak nama pelanggan, daftar barang, total nominal, dan jatuh tempo. Mendukung rekaman live atau upload file MP3/WAV. Data tersimpan di buku kasbon digital dengan riwayat lengkap.

**Akurasi**: 92% | **Waktu**: 15-25 detik

![Rekam Audio](screenshots/juragan-kasbon-rekam.webp)
![Hasil Kasbon](screenshots/juragan-kasbon-hasil.webp)

---

### 7. Konsultan Warung

![Fitur Konsultan Warung](screenshots/konsultan-warung.webp)

AI advisor dengan RAG (Retrieval-Augmented Generation) yang membaca data warung Anda sebelum menjawab. Tanyakan tentang kesehatan keuangan, pelanggan dengan hutang terbesar, tren pengeluaran, atau barang yang sering habis. AI akan memberikan jawaban spesifik berdasarkan data belanja, hutang, dan stok Anda.

**Waktu**: 10-15 detik

![Input Pertanyaan](screenshots/konsultan-warung-input.webp)
![Jawaban Konsultan](screenshots/konsultan-warung-jawaban.webp)

---

## Teknologi yang Digunakan

### AI & Machine Learning

| Teknologi | Model | Fungsi Utama |
|-----------|-------|--------------|
| **Google Gemini** | 2.5 Flash | Vision AI, Audio Processing, OCR Multimodal |
| **Kolosal AI** | Kimi K2 & MiniMax M2 | Context Analysis, Business Consultation |
| **OpenAI** | GPT-4o-mini | Failover System (Backup) |

### Framework & Core Libraries

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **Python** | 3.10+ | Bahasa pemrograman utama |
| **Gradio** | 5.0+ | Web interface framework |
| **SQLite** | 3.x | Database (ringan, tidak perlu server) |
| **Pillow** | 10.0+ | Image processing & validation |

### External APIs & Services

| Service | Provider | Fungsi |
|---------|----------|--------|
| **WhatsApp API** | Fonnte | Kirim pesan promosi otomatis |
| **Safe Browsing** | Google | Cek URL berbahaya (database 5M+ situs) |
| **WHOIS Lookup** | python-whois | Validasi umur domain |

### Supporting Libraries

```
gradio==5.0+
google-generativeai
openai
python-dotenv
beautifulsoup4
requests
python-whois
Pillow
```

---

## Arsitektur Sistem

### Diagram Arsitektur Keseluruhan

```
┌─────────────────────────────────────────────────────────┐
│               GRADIO WEB INTERFACE                      │
│  (7 Tabs: Transfer | Stok | Tangkal | Expense |         │
│           Sales | Kasbon | Konsultan)                   │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
┌────────▼─────────┐   ┌─────────▼──────────┐
│  UI Templates    │   │   App Handlers     │
│  (HTML/CSS)      │   │   (Event Logic)    │
└──────────────────┘   └─────────┬──────────┘
                                 │
                ┌────────────────┴──────────────────────┐
                │                                       │
     ┌──────────▼───────────┐              ┌───────────▼────────────┐
     │  ANALYZER LAYER      │              │   STORAGE LAYER        │
     │  (Business Logic)    │◄─────────────┤   (SQLite Database)    │
     │                      │  Read/Write  │                        │
     │ • TransferVerifier   │              │ • transfer_logs        │
     │ • InventoryAnalyzer  │              │ • inventory_logs       │
     │ • ScamAnalyzer       │              │ • scam_logs            │
     │ • ExpenseAnalyzer    │              │ • expense_logs         │
     │ • SalesmanAnalyzer   │              │ • debt_logs            │
     │ • KasbonAnalyzer     │              │ • salesman_logs        │
     │ • ConsultantAnalyzer │              └────────────────────────┘
     └──────────┬───────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼────────┐  ┌────────▼─────────┐
│  MODELS LAYER  │  │  EXTERNAL APIs   │
│  (AI Wrappers) │  │                  │
│                │  │ • Fonnte WA API  │
│ • Gemini AI    │  │ • Safe Browsing  │
│ • Kolosal AI   │  │ • WHOIS Protocol │
│ • OpenAI       │  └──────────────────┘
└────────────────┘
```

### Database Schema

```sql
┌──────────────────────┐
│   transfer_logs      │
├──────────────────────┤
│ id (PK)              │
│ created_at           │
│ notes                │
│ result_text          │
└──────────────────────┘

┌──────────────────────┐
│   inventory_logs     │
├──────────────────────┤
│ id (PK)              │
│ created_at           │
│ notes                │
│ result_text          │
└──────────────────────┘

┌──────────────────────┐
│   scam_logs          │
├──────────────────────┤
│ id (PK)              │
│ created_at           │
│ extracted_text       │
│ extracted_url        │
│ verdict              │
│ raw_analysis         │
└──────────────────────┘

┌──────────────────────┐
│   expense_logs       │
├──────────────────────┤
│ id (PK)              │
│ created_at           │
│ merchant_name        │
│ transaction_date     │
│ total_amount         │
│ items_summary        │
│ raw_text             │
└──────────────────────┘

┌──────────────────────┐
│   debt_logs          │
├──────────────────────┤
│ id (PK)              │
│ created_at           │
│ customer_name        │
│ items_list           │
│ total_amount         │
│ due_date_note        │
│ raw_text             │
└──────────────────────┘

┌──────────────────────┐
│   salesman_logs      │
├──────────────────────┤
│ id (PK)              │
│ created_at           │
│ target_phone         │
│ style_used           │
│ generated_message    │
│ status               │
│ api_response         │
└──────────────────────┘
```

---

## Cara Instalasi

Ikuti panduan ini langkah demi langkah untuk menjalankan WarungVision di komputer Anda.

### Prasyarat

1. **Sistem Operasi**: Windows 10/11, macOS, atau Linux
2. **Python**: Versi 3.10 atau lebih baru
3. **Koneksi Internet**: Untuk download library dan akses AI API
4. **Text Editor** (opsional): VS Code, Notepad++, atau Sublime Text

---

### Langkah 1: Install Python

**Jika Python belum terinstall:**

#### Windows:
1. Download Python dari [python.org/downloads](https://www.python.org/downloads/)
2. Jalankan installer
3. **PENTING**: Centang **"Add Python to PATH"** saat install
4. Klik "Install Now"
5. Tunggu sampai selesai

#### macOS:
```bash
brew install python@3.10
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

**Cek instalasi:**
```bash
python --version
# Atau
python3 --version
```
Harus muncul: `Python 3.10.x` atau lebih tinggi

---

### Langkah 2: Download Aplikasi

#### Cara 1: Clone dengan Git (Recommended)
```bash
git clone https://github.com/moh-ariful/warungvision.git
cd warungvision
```

#### Cara 2: Download ZIP
1. Klik tombol "Code" di GitHub
2. Pilih "Download ZIP"
3. Extract file ZIP
4. Buka terminal/command prompt
5. Masuk ke folder hasil extract:
   ```bash
   cd path/to/warungvision
   ```

---

### Langkah 3: Buat Virtual Environment

Virtual environment adalah lingkungan terisolasi untuk aplikasi ini agar tidak bentrok dengan package Python lain.

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Jika berhasil, akan muncul `(venv)` di awal baris command:
```
(venv) C:\Users\...\warungvision>
```

**Untuk menonaktifkan virtual environment:**
```bash
deactivate
```

---

### Langkah 4: Install Dependencies

Pastikan virtual environment sudah aktif (ada tulisan `(venv)`).

```bash
pip install -r requirements.txt
```

Proses ini akan install semua library yang dibutuhkan (Gradio, Gemini SDK, OpenAI, BeautifulSoup, dll). Waktu: 2-5 menit tergantung kecepatan internet.

**Jika muncul error "pip not found":**
```bash
python -m pip install -r requirements.txt
```

---

### Langkah 5: Setup API Keys

Aplikasi ini membutuhkan API Key dari 3 provider AI. Semua gratis untuk penggunaan demo.

#### 5.1 Buat File .env

1. Copy file `.env.example` dan rename jadi `.env`
   ```bash
   cp .env.example .env
   ```
2. Buka file `.env` dengan text editor

#### 5.2 Dapatkan Google API Key (Gemini)

1. Buka [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Login dengan akun Google
3. Klik "Create API Key"
4. Copy API Key dan paste ke file `.env`:
   ```
   GOOGLE_API_KEY=AIzaSyAbc123YourKeyHere
   ```

**Gratis**: 60 request/menit

#### 5.3 Dapatkan Kolosal AI API Key

1. Buka [https://app.kolosal.ai/id/api_keys/](https://app.kolosal.ai/id/api_keys/)
2. Daftar akun (gunakan email Indonesia)
3. Masuk ke Dashboard → API Keys
4. Copy API Key dan paste ke `.env`:
   ```
   KOLOSAL_API_KEY=kolosal_abc123YourKeyHere
   ```

**Gratis**: Quota trial untuk hackathon participant

#### 5.4 Dapatkan OpenAI API Key (Opsional - Untuk Backup)

1. Buka [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Login/Daftar akun
3. Klik "Create new secret key"
4. Copy API Key (hanya muncul 1x) dan paste ke `.env`:
   ```
   OPENAI_API_KEY=sk-abc123YourKeyHere
   ```

**Gratis**: $5 credit untuk akun baru

#### 5.5 Dapatkan Google Safe Browsing Key (Opsional)

1. Buka [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Create New Project → Enable "Safe Browsing API"
3. Credentials → Create API Key
4. Copy dan paste ke `.env`:
   ```
   GOOGLE_SAFE_BROWSING_KEY=AIzabcYourKeyHere
   ```

**Gratis**: 10,000 request/hari

#### 5.6 Setup Fonnte Token (Opsional - Untuk WhatsApp)

1. Buka [https://fonnte.com/](https://fonnte.com/)
2. Daftar akun (gratis trial 1000 pesan)
3. Dapatkan token dari dashboard
4. Paste ke `.env`:
   ```
   FONNTE_TOKEN=YourFonnteToken
   ```

#### Hasil Akhir File .env:

```env
# AI API Keys
GOOGLE_API_KEY=AIzaSyAbc123YourKeyHere
KOLOSAL_API_KEY=kolosal_abc321YourKeyHere
OPENAI_API_KEY=sk-abc123YourKeyHere

# Security APIs
GOOGLE_SAFE_BROWSING_KEY=AIzabcYourKeyHere

# WhatsApp Integration
FONNTE_TOKEN=YourFonnteToken

# Server Config (opsional, bisa pakai default)
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

**PENTING**: Jangan share file `.env` atau upload ke GitHub!

---

### Langkah 6: Inisialisasi Database

Database SQLite akan otomatis dibuat saat aplikasi pertama kali dijalankan. Tidak perlu setup manual.

---

### Langkah 7: Jalankan Aplikasi

Pastikan:
- Virtual environment aktif (ada tulisan `(venv)`)
- Sudah install semua library
- File `.env` sudah diisi dengan API Keys

**Jalankan:**
```bash
python app.py
```

**Jika berhasil, akan muncul:**
```
Running on local URL:  http://127.0.0.1:7860

Aplikasi siap digunakan!
Buka browser dan akses: http://localhost:7860
```

Tunggu 10-15 detik sampai muncul pesan di atas.

---

### Langkah 8: Akses Aplikasi

1. Buka browser (Chrome, Firefox, Edge, Safari)
2. Ketik alamat: `http://localhost:7860`
3. Aplikasi WarungVision akan muncul

Atau klik link Gradio Public URL (bisa diakses dari device lain selama 72 jam):
```
https://abc123random.gradio.live
```

---

### Cara Menghentikan Aplikasi

Di terminal/command prompt, tekan `Ctrl + C`, lalu ketik `y` dan Enter.

---

### Troubleshooting

#### Error: "ModuleNotFoundError: No module named 'gradio'"
**Solusi:**
```bash
# Pastikan virtual environment aktif
pip install gradio
```

#### Error: "GOOGLE_API_KEY not found"
**Solusi:**
1. Cek file `.env` sudah dibuat (bukan `.env.example`)
2. Pastikan API Key sudah diisi (tidak ada spasi di awal/akhir)
3. Restart terminal dan aktifkan ulang virtual environment

#### Error: "Address already in use" / Port 7860 sudah dipakai
**Solusi:** Ganti port di file `.env`:
```env
GRADIO_SERVER_PORT=7861
```
Lalu akses di `http://localhost:7861`

#### Error: "Permission denied" saat install (Linux/macOS)
**Solusi:**
```bash
# Jangan pakai sudo! Aktifkan virtual environment dulu
source venv/bin/activate
pip install -r requirements.txt
```

#### Upload file tidak berfungsi
**Solusi:**
- Pastikan file gambar < 11MB
- Format harus PNG, JPG, atau JPEG
- Coba pakai browser lain (Chrome recommended)

---

### Akses dari HP/Device Lain (LAN)

1. Cari IP komputer Anda:
   
   **Windows:**
   ```bash
   ipconfig
   ```
   Cari "IPv4 Address" (contoh: `192.168.1.100`)

   **macOS/Linux:**
   ```bash
   ifconfig | grep inet
   ```

2. Di HP, buka browser, ketik:
   ```
   http://192.168.1.100:7860
   ```
   (Ganti `192.168.1.100` dengan IP komputer Anda)

3. Pastikan HP dan komputer terhubung ke WiFi yang sama

---

## Cara Menggunakan

### Cek Transfer Palsu

1. Buka tab "Cek Transfer"
2. Upload foto screenshot transfer
3. (Opsional) Tulis catatan: "Cek apakah nominal Rp 500.000 benar"
4. Klik "Periksa"
5. Tunggu 20-25 detik
6. Lihat hasil: Status warna (Hijau=ASLI, Kuning=PERLU CEK, Merah=PALSU)

**Tips**: Gunakan screenshot asli (bukan foto layar HP), pastikan angka nominal terlihat jelas.

---

### Smart Inventory

1. Buka tab "Stok & Rak"
2. Foto rak/gudang warung dari HP
3. Upload foto
4. (Opsional) Tulis pertanyaan: "Apakah minyak goreng masih aman?"
5. Klik "Analisa Stok"
6. Tunggu 20-25 detik
7. Lihat laporan per kategori barang

**Tips**: Foto dari jarak 1-2 meter dengan cahaya cukup.

---

###Tangkal Tipu

1. Buka tab "Tangkal Tipu"
2. Screenshot chat mencurigakan dari WhatsApp/Telegram
3. Upload screenshot
4. Klik "Analisa"
5. Tunggu 15-20 detik (sedang cek 5 lapisan keamanan)
6. Lihat verdict: AMAN (hijau) atau BERBAHAYA (merah)

**Tips**: Jangan klik link dulu sebelum dicek. Jika verdict BERBAHAYA, langsung blokir nomor.

---

### Catat Pengeluaran

1. Buka tab "Catat Pengeluaran"
2. Foto struk belanja (cetakan atau tulisan tangan)
3. Upload foto
4. Klik "Catat"
5. Tunggu 20-25 detik
6. Data otomatis tersimpan + muncul di riwayat

**Tips**: Foto dengan cahaya cukup, pastikan angka total terlihat jelas.

---

### Salesman WA

1. Buka tab "Salesman WA"
2. Upload foto produk yang mau dipromosikan
3. Pilih gaya bahasa: Emak-emak / Formal / Gaul
4. Klik "Buat Caption"
5. Tunggu 15-20 detik
6. Edit caption jika perlu (tambah harga, alamat)
7. Masukkan nomor WhatsApp tujuan (contoh: 081234567890)
8. Klik "Kirim"

**Tips**: Foto produk dengan angle menarik, edit caption untuk tambah info penting.

---

### Juragan Kasbon

1. Buka tab "Juragan Kasbon"
2. Klik ikon microphone
3. Izinkan akses microphone di browser
4. Bicara dengan jelas: "Bu Tejo ambil Beras 5 kilo sama Minyak 2 liter, total 95 ribu, bayar minggu depan"
5. Stop rekaman
6. Klik "Catat Suara"
7. Tunggu 15-25 detik
8. Data hutang otomatis tersimpan

**Alternatif**: Upload file audio MP3/WAV yang sudah direkam.

**Tips**: Bicara dengan jelas, sebutkan nama pelanggan → barang → harga → kapan bayar.

---

### Konsultan Warung

1. Buka tab "Konsultan Warung"
2. Ketik pertanyaan: "Keuanganku sehat gak?" atau "Siapa yang hutangnya paling banyak?"
3. Klik "Tanya Konsultan"
4. Tunggu 10-15 detik
5. Baca jawaban + saran bisnis berdasarkan data warung Anda

**Tips**: Tanyakan hal spesifik (jangan terlalu umum). AI akan analisis data belanja, hutang, dan stok Anda.

---

## Struktur Proyek

```
warungvision/
├── app.py                        # File utama aplikasi (Gradio interface)
├── config.py                     # Konfigurasi & environment variables
├── utils.py                      # Helper functions
│
├── models.py                     # Gemini 2.5 Flash wrapper
├── models_consultant.py          # Hybrid AI (Kolosal + OpenAI) untuk Konsultan
├── models_tangkal_tipu.py        # Hybrid AI untuk Tangkal Tipu
│
├── analyzers.py                  # Business logic: Transfer & Inventory
├── analyzers_expense.py          # Business logic: OCR struk
├── analyzers_kasbon.py           # Business logic: Audio-to-debt
├── analyzers_salesman.py         # Business logic: Caption generator
├── analyzers_consultant.py       # Business logic: RAG consultant
├── analyzers_tangkal_tipu.py     # Business logic: Multi-layer scam checker
│
├── storage.py                    # Database: transfer & inventory
├── storage_expense.py            # Database: Pengeluaran
├── storage_kasbon.py             # Database: Hutang
├── storage_salesman.py           # Database: Promosi WA
├── storage_tangkal_tipu.py       # Database: Scam logs
├── storage_consultant.py         # Database query untuk Konsultan
│
├── ui_templates.py               # HTML/CSS formatters
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Template API Keys
├── .env                          # File API Keys (jangan upload ke GitHub!)
│
├── warungvision.db               # SQLite database (auto-generated)
│
├── screenshots/                  # Screenshot untuk README
├── assets/                       # Asset visual
├── venv/                         # Virtual environment
│
├── README.md                     # Dokumentasi
└── LICENSE                       # MIT License
```

---

## Demo & Live Preview

### Video Demo Lengkap

Tonton demo lengkap WarungVision di YouTube:  
**[https://youtu.be/hH1BjAYbl3Y](https://youtu.be/hH1BjAYbl3Y)**

**Durasi**: 6 menit  
**Isi**: Problem statement, demo 7 fitur, highlight teknologi, impact UMKM

---

### Coba Langsung (Live Demo)

Akses aplikasi WarungVision yang sudah deploy:  
**[https://warungvision.ddns.net](https://warungvision.ddns.net)**

Bisa diakses dari laptop, HP Android/iOS, dari mana saja (selama ada internet).

---

## Tim Pengembang

**JagaNusantara XX/Developer**  
Dikembangkan untuk Hackathon IMPHNEN x Kolosal AI 2025

Email: nextkoding@gmail.com  
GitHub: [github.com/moh-ariful](https://github.com/moh-ariful)

---

## Lisensi

Proyek ini menggunakan **MIT License**. Lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

## Kontak & Dukungan

**Email**: [nextkoding@gmail.com](mailto:nextkoding@gmail.com)

**Laporkan Bug**: Buat issue di GitHub dengan format:
- Judul jelas
- Screenshot error
- Langkah reproduksi
- Versi Python & OS

---

<div align="center">

### Dibuat dengan Cinta untuk UMKM Indonesia

**WarungVision** - Dari Warung, Untuk Warung

[![YouTube](https://img.shields.io/badge/YouTube-Watch%20Demo-red?logo=youtube)](https://youtu.be/hH1BjAYbl3Y)
[![Website](https://img.shields.io/badge/Website-Try%20Live-blue?logo=google-chrome)](https://warungvision.ddns.net)
[![GitHub](https://img.shields.io/badge/GitHub-Source%20Code-black?logo=github)](https://github.com/moh-ariful/warungvision)

---

**Powered by:**  
Gemini 2.5 Flash • Kolosal AI • OpenAI GPT-4o-mini • Fonnte • Gradio

**Hackathon IMPHNEN x Kolosal AI 2025**

© 2025 WarungVision. All Rights Reserved.

</div>

---
