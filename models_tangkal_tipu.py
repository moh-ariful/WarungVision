# models_tangkal_tipu.py
import openai
from config import settings

class HybridScamAI:
    """
    Load Balancer AI untuk Tangkal Tipu.
    - Primary: Kolosal AI (Model: Kimi K2)
    - Backup: OpenAI (Model: gpt-4o-mini)
    """
    def __init__(self):
        # 1. Setup Primary Client (Kolosal)
        if settings.KOLOSAL_API_KEY:
            self.client_primary = openai.OpenAI(
                api_key=settings.KOLOSAL_API_KEY,
                base_url=settings.KOLOSAL_BASE_URL
            )
        else:
            self.client_primary = None
            print("⚠️ Warning: KOLOSAL_API_KEY belum diset.")

        # 2. Setup Backup Client (OpenAI Resmi)
        if settings.OPENAI_API_KEY:
            self.client_backup = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY
                # base_url default ke api.openai.com
            )
        else:
            self.client_backup = None
            print("⚠️ Warning: OPENAI_API_KEY belum diset (Backup off).")

    def analyze_context(self, message_text: str, technical_findings: str) -> str:
        """
        Mencoba model utama, jika gagal, beralih ke backup.
        """
        
        # --- Prompt Construction ---
        # Untuk gpt-4o-mini, role 'developer' lebih disarankan (sesuai docs).
        # Untuk Kolosal, kita pakai 'system' (standar kompatibilitas).
        
        system_instruction = (
            "Kamu adalah ahli keamanan siber untuk fitur 'Tangkal Tipu' WarungVision. "
            "Tugasmu menganalisis pesan dan data teknis untuk menentukan apakah ini penipuan.\n\n"
            "Aturan Output:\n"
            "Kembalikan HANYA JSON VALID dengan format:\n"
            "{\n"
            '  "status": "AMAN" atau "BERBAHAYA",\n'
            '  "reason": "Penjelasan singkat maksimal 2 kalimat untuk orang awam",\n'
            '  "action": "Saran tindakan (misal: Blokir nomor, Abaikan, Hapus)"\n'
            "}"
        )

        user_content = (
            f"Isi Pesan: \"{message_text}\"\n"
            f"Temuan Teknis: {technical_findings}\n\n"
            "Analisis pesan ini! Apakah ini penipuan?"
        )

        # ----------------------------------------
        # PERCOBAAN 1: PRIMARY (KOLOSAL AI)
        # ----------------------------------------
        if self.client_primary:
            try:
                print("🔄 Mengubungi Primary AI (Kolosal)...")
                response = self.client_primary.chat.completions.create(
                    model="Kimi K2",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"❌ Kolosal Error: {e}")
                print("⚠️ Beralih ke Backup AI...")
        else:
            print("⚠️ Kolosal Key tidak ada, langsung ke Backup.")

        # ----------------------------------------
        # PERCOBAAN 2: BACKUP (OPENAI gpt-4o-mini)
        # ----------------------------------------
        if self.client_backup:
            try:
                print("🔄 Mengubungi Backup AI (OpenAI gpt-4o-mini)...")
                response = self.client_backup.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        # Menggunakan role 'developer' sesuai dokumentasi OpenAI gpt-4o-mini
                        {"role": "developer", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            except Exception as e:
                error_msg = f"Backup AI Error: {e}"
                print(f"❌ {error_msg}")
                return self._error_json("SEMUA AI GAGAL", error_msg)
        
        # Jika kedua client tidak tersedia
        return self._error_json("KONFIGURASI ERROR", "API Key Primary dan Backup belum diset.")

    def _error_json(self, status_short: str, detail: str) -> str:
        """Helper untuk format pesan error JSON"""
        # Escape quote agar JSON valid
        safe_detail = detail.replace('"', "'")
        return f'{{"status": "ERROR", "reason": "{status_short}: {safe_detail}", "action": "Hubungi admin atau coba lagi nanti."}}'