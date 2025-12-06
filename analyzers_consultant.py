# analyzers_consultant.py
from storage_consultant import get_business_summary
from models_consultant import HybridConsultantAI

class ConsultantAnalyzer:
    """
    Logika bisnis untuk fitur Konsultan Warung.
    Menggabungkan Data Database + Pertanyaan User -> Kirim ke AI Hibrida.
    """
    def __init__(self):
        self.ai = HybridConsultantAI()

    def consult(self, user_question: str) -> str:
        if not user_question.strip():
            return "Silakan tulis pertanyaan Anda mengenai kondisi warung."

        # 1. Ambil Data Konteks (RAG Sederhana)
        data_context = get_business_summary()

        # 2. Susun Instruksi Sistem (Persona)
        system_prompt = (
            "Kamu adalah Konsultan Bisnis Profesional khusus UMKM Warung di Indonesia.\n"
            "Tugasmu adalah menjawab pertanyaan pemilik warung berdasarkan DATA NYATA yang diberikan.\n\n"
            f"=== DATA WARUNG SAAT INI ===\n{data_context}\n\n"
            "PANDUAN MENJAWAB:\n"
            "1. Jawablah dengan ramah, suportif, dan menggunakan Bahasa Indonesia yang mudah dimengerti.\n"
            "2. Gunakan data di atas sebagai landasan fakta. Jangan mengarang angka.\n"
            "3. Jika data tidak ada (misal hutang kosong), katakan bahwa data belum tersedia.\n"
            "4. Berikan saran praktis jika diminta (misal: cara menagih hutang, cara hemat stok).\n"
            "5. Jangan terlalu formal, anggap user adalah mitra kerjamu."
        )

        # 3. Kirim ke AI
        answer = self.ai.ask_consultant(system_prompt, user_question)
        return answer