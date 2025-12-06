# models_consultant.py
import openai
from config import settings

class HybridConsultantAI:
    """
    Sistem AI Hibrida Failover untuk Konsultasi Warung.
    Prioritas: Kolosal AI (MiniMax M2) -> Failover: OpenAI (gpt-4o-mini)
    """
    def __init__(self):
        # Setup Kolosal Client
        self.client_kolosal = None
        if settings.KOLOSAL_API_KEY:
            self.client_kolosal = openai.OpenAI(
                api_key=settings.KOLOSAL_API_KEY,
                base_url=settings.KOLOSAL_BASE_URL
            )
        
        # Setup OpenAI Client (Backup)
        self.client_openai = None
        if settings.OPENAI_API_KEY:
            self.client_openai = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY
                # base_url default ke api.openai.com
            )

    def ask_consultant(self, system_context: str, user_question: str) -> str:
        """
        Mengirim pertanyaan ke AI dengan mekanisme failover otomatis.
        """
        
        # --- PERCOBAAN 1: KOLOSAL AI (MiniMax M2) ---
        if self.client_kolosal:
            try:
                print("🤖 Menghubungi Konsultan Utama (Kolosal AI)...")
                response = self.client_kolosal.chat.completions.create(
                    model="MiniMax M2",
                    messages=[
                        {"role": "system", "content": system_context},
                        {"role": "user", "content": user_question}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"⚠️ Kolosal Error ({e}). Beralih ke Backup...")
        
        # --- PERCOBAAN 2: OPENAI (gpt-4o-mini) ---
        if self.client_openai:
            try:
                print("🚑 Menghubungi Konsultan Cadangan (OpenAI)...")
                # Sesuai dokumentasi: gpt-4o-mini lebih patuh pada role 'developer'
                response = self.client_openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "developer", "content": system_context},
                        {"role": "user", "content": user_question}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"❌ Maaf, semua sistem AI sedang sibuk. Error: {str(e)}"
        
        return "⚠️ Konfigurasi Error: API Key Kolosal maupun OpenAI belum diatur."