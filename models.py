# models.py
import google.generativeai as genai
from typing import Optional, Any, List, Union
import time
from config import settings
from utils import today_id_date_str


class WarungVisionAI:
    """
    Wrapper sederhana untuk Gemini 2.5 Flash.
    Di sini kita sediakan fungsi utama:
    - analyze_transfer: analisis bukti transfer
    - analyze_inventory: analisis foto rak/stok
    - generate_promo_caption: buat caption promosi WA
    - analyze_kasbon_audio: analisis rekaman suara untuk hutang (NEW)

    UPDATE: Refined Prompt untuk memprioritaskan 'Catatan User'.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        if not settings.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY belum diset. Isi dulu di file .env berdasarkan .env.example"
            )
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def _generate(self, contents: List[Union[str, Any]]) -> str:
        """
        Fungsi pembungkus panggilan ke Gemini.
        contents bisa berisi teks + image (PIL Image).
        """
        response = self.model.generate_content(contents)
        # Antisipasi kalau response kosong/aneh
        try:
            return response.text
        except Exception:
            return str(response)

    def analyze_transfer(self, notes: str, image: Optional[Any]) -> str:
        """
        Analisis bukti transfer berdasarkan deskripsi & gambar.
        """
        today_str = today_id_date_str()  # contoh: "01/12/2025"
        user_notes = notes.strip() if notes else "Tidak ada catatan khusus."

        base_prompt = (
            "Kamu adalah asisten AI keamanan untuk pemilik warung UMKM di Indonesia. "
            "Tugasmu adalah memverifikasi keaslian bukti transfer digital/struk ATM.\n\n"
            
            f"📅 KONTEKS WAKTU: Hari ini adalah {today_str} (Format: DD/MM/YYYY).\n"
            "Aturan Waktu:\n"
            "- Tanggal sama dengan hari ini = NORMAL.\n"
            "- Selisih 1-2 hari = WAJAR (mungkin delay).\n"
            "- Tanggal jauh di masa depan = INDIKASI PENIPUAN.\n\n"

            "📝 KONTEKS KHUSUS DARI USER (PRIORITAS TINGGI):\n"
            f"User memberikan catatan: \"{user_notes}\"\n"
            "INSTRUKSI: Jika user menyebutkan detail tertentu dalam catatan di atas (misal: 'cek nominal', 'cek nama pengirim'), "
            "kamu WAJIB memverifikasi hal tersebut pada gambar secara spesifik.\n\n"

            "TUGAS ANALISIS VISUAL:\n"
            "1. Cek Font & Layout: Apakah ada jenis huruf yang beda sendiri? (Indikasi editan).\n"
            "2. Cek Nominal & Status: Apakah status BERHASIL? Apakah nominal sesuai logika?\n"
            "3. Cek Tanda-tanda Editan: Adakah bekas tempelan, background tidak rata, atau pixel pecah di area angka?\n\n"

            "=== OUTPUT FORMAT (JSON ONLY) ===\n"
            "Kembalikan JAWABAN HANYA dalam bentuk JSON VALID (tanpa markdown ```json, tanpa teks lain) "
            "dengan struktur persis seperti ini:\n\n"
            "{\n"
            '  "status": "ASLI | PERLU DICEK LAGI | MENCURIGAKAN | DIDUGA PALSU",\n'
            "  \"confidence_score\": 0-100,\n"
            "  \"key_findings\": [\n"
            "    \"temuan 1 (jika catatan user benar/salah, sebutkan disini)\",\n"
            "    \"temuan 2 (visual)\",\n"
            "    \"temuan 3\"\n"
            "  ],\n"
            "  \"recommendations\": [\n"
            "    \"saran tindakan 1\",\n"
            "    \"saran tindakan 2\"\n"
            "  ]\n"
            "}\n"
        )

        parts: List[Union[str, Any]] = [base_prompt]
        if image is not None:
            parts.append(image)

        return self._generate(parts)

    def analyze_inventory(self, notes: str, image: Optional[Any]) -> str:
        """
        Analisis foto rak / stok barang.
        """
        user_notes = notes.strip() if notes else "Tidak ada catatan khusus."
        
        base_prompt = (
            "Kamu adalah asisten gudang warung pintar. Tugasmu melakukan Stock Opname Visual.\n"
            "Lihat foto rak/barang yang dilampirkan dan buat laporan stok.\n\n"

            "📝 PERMINTAAN KHUSUS USER (PRIORITAS UTAMA):\n"
            f"Catatan User: \"{user_notes}\"\n"
            "INSTRUKSI: Jika catatan user bertanya tentang barang spesifik (misal: 'cek stok minyak', 'apakah gula habis?'), "
            "kamu HARUS menjawab pertanyaan itu di dalam 'notes' kategori yang relevan atau di 'summary'.\n\n"

            "INSTRUKSI UMUM:\n"
            "- Kelompokkan barang per kategori (Mie, Minuman, Sembako, Rokok, dll).\n"
            "- Status Stok: AMAN (Penuh), MULAI MENIPIS (Setengah), HAMPIR HABIS (Sedikit/Kosong).\n"
            "- Gunakan bahasa Indonesia yang santai tapi jelas.\n\n"

            "=== OUTPUT FORMAT (JSON ONLY) ===\n"
            "Kembalikan JAWABAN HANYA dalam bentuk JSON VALID (tanpa markdown ```json) dengan struktur:\n\n"
            "{\n"
            "  \"categories\": [\n"
            "    {\n"
            "      \"name\": \"Nama Kategori (misal: Minuman)\",\n"
            "      \"status\": \"AMAN | MULAI MENIPIS | HAMPIR HABIS\",\n"
            "      \"notes\": \"Kondisi visual + Jawaban atas catatan user jika relevan\"\n"
            "    }\n"
            "  ],\n"
            "  \"summary\": \"Ringkasan umum stok & saran belanja\"\n"
            "}\n"
        )

        parts: List[Union[str, Any]] = [base_prompt]
        if image is not None:
            parts.append(image)

        return self._generate(parts)

    def generate_promo_caption(self, style: str, image: Any) -> str:
        """
        Membuat caption promosi berdasarkan gambar dan gaya bahasa.
        """
        prompt = (
            "Kamu adalah Copywriter Handal khusus WhatsApp Marketing untuk Warung.\n"
            "Tugasmu: Lihat foto produk/makanan ini, lalu buatkan caption promosi yang menarik.\n\n"
            f"GAYA BAHASA: {style}\n\n"
            "Instruksi:\n"
            "1. Caption harus persuasif, ramah, dan cocok untuk WhatsApp (gunakan emoji).\n"
            "2. Jangan terlalu panjang, maksimal 3-4 kalimat intinya saja.\n"
            "3. Sesuaikan nada dengan gaya bahasa yang diminta.\n"
            "   - Emak-emak: Gunakan kata sapaan 'Bunda', 'Say', akrab, sedikit heboh.\n"
            "   - Formal: Sopan, informatif, to the point.\n"
            "   - Anak Muda: Gaul, santai, pakai istilah kekinian.\n"
            "4. Output HARUS dalam format JSON agar bisa diproses sistem.\n\n"
            "=== OUTPUT FORMAT (STRICT JSON) ===\n"
            "{\n"
            '  "caption": "Tulis caption promosi di sini..."\n'
            "}"
        )
        
        parts: List[Union[str, Any]] = [prompt, image]
        return self._generate(parts)

    def analyze_kasbon_audio(self, audio_path: str) -> str:
        """
        Menganalisa file audio (voice note) untuk mengekstrak data hutang/kasbon.
        Menggunakan fitur Native Audio Gemini 2.5 Flash.
        """
        prompt = (
            "Kamu adalah asisten administrasi warung yang teliti (Juragan Kasbon).\n"
            "Dengarkan rekaman suara pemilik warung ini dengan seksama.\n"
            "Tugasmu: Ekstrak data transaksi hutang (kasbon) dari ucapan tersebut.\n\n"
            
            "INSTRUKSI EKSTRAKSI:\n"
            "1. Cari NAMA PELANGGAN (siapa yang berhutang? Jika tidak ada, tulis 'Pelanggan').\n"
            "2. Cari DAFTAR BARANG yang diambil (item & kuantitas).\n"
            "3. Cari TOTAL NOMINAL Rupiah (jika disebutkan). Jika hanya menyebut harga satuan, hitung totalnya.\n"
            "4. Cari TANGGAL JATUH TEMPO / JANJI BAYAR (misal: 'minggu depan', 'besok', 'tanggal 5'). Jika tidak ada, tulis '-'.\n\n"
            
            "=== OUTPUT FORMAT (STRICT JSON) ===\n"
            "{\n"
            '  "customer_name": "Bu Tejo",\n'
            '  "items": ["Beras 5kg", "Minyak 2L"],\n'
            '  "amount": 95000,\n'
            '  "due_date_note": "Minggu depan"\n'
            "}"
        )

        # Upload file audio ke Gemini File API
        # Note: Gemini akan memproses file audio ini secara native multimodal
        print(f"Uploading audio: {audio_path}...")
        audio_file = genai.upload_file(path=audio_path)
        
        # Proses generate content dengan prompt + audio file
        response = self.model.generate_content([prompt, audio_file])
        
        # (Opsional) Best practice: File di server Google akan expired otomatis (default 48 jam),
        # tapi kita tidak perlu menghapusnya manual di sini untuk mempercepat respon demo.
        
        try:
            return response.text
        except Exception:
            return str(response)