# analyzers_expense.py
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, Optional
from models import WarungVisionAI
from utils import today_id_date_str

@dataclass
class ExpenseResult:
    merchant: str
    date: str
    numeric_total: float
    items_summary: str
    confidence_note: str
    raw_text: str

class ExpenseAnalyzer:
    """
    Logika ekstraksi data struk belanja.
    """
    def __init__(self, ai: WarungVisionAI):
        self.ai = ai

    def _clean_amount(self, amount_str: str) -> float:
        """Bersihkan format uang jadi float dengan aman"""
        try:
            # 1. Pastikan string dan strip spasi kiri/kanan
            s = str(amount_str).strip()
            
            # 2. Hapus suffix ,00 atau .00 di akhir string secara manual
            # Ini mengatasi bug di mana regex kadang gagal membaca akhir string
            # Contoh: "Rp 50.000,00" -> dibuang ",00" nya -> "Rp 50.000"
            if s.endswith(",00") or s.endswith(".00"):
                s = s[:-3] # Potong 3 karakter terakhir

            # 3. Hapus "Rp", titik ribuan, spasi, dll. Ambil digit saja
            # Contoh: "Rp 50.000" -> "50000"
            clean = re.sub(r'[^\d]', '', s)
            
            return float(clean) if clean else 0.0
        except:
            return 0.0

    def analyze(self, image: Any) -> ExpenseResult:
        """Ekstrak data belanja dari foto"""
        today_str = today_id_date_str()
        
        prompt = (
            "Kamu adalah akuntan warung profesional. Tugasmu: Baca foto nota/struk belanja ini.\n"
            "Nota bisa berupa cetakan printer atau TULISAN TANGAN cakar ayam.\n\n"
            f"Konteks Hari Ini: {today_str}\n"
            "Instruksi Ekstraksi:\n"
            "1. Cari NAMA TOKO/SUPPLIER (jika tidak ada, tebak dari header).\n"
            "2. Cari TANGGAL TRANSAKSI (jika tidak ada, gunakan tanggal hari ini).\n"
            "3. Cari TOTAL AKHIR (Grand Total) yang harus dibayar.\n"
            "4. Buat ringkasan barang apa saja yang dibeli (max 5 kata).\n\n"
            "=== OUTPUT FORMAT (JSON ONLY) ===\n"
            "{\n"
            '  "merchant": "Nama Toko",\n'
            '  "date": "DD/MM/YYYY",\n'
            '  "total_amount": "150000",\n'
            '  "items_summary": "Beras, Gula, dan Minyak",\n'
            '  "confidence_note": "Tulisan jelas/agak buram"\n'
            "}"
        )

        # Gunakan method internal _generate dari WarungVisionAI
        raw_text = self.ai._generate([prompt, image])
        
        # Parsing JSON
        try:
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            start = clean_json.find('{')
            end = clean_json.rfind('}') + 1
            if start != -1 and end != -1:
                clean_json = clean_json[start:end]
            
            data = json.loads(clean_json)
        except:
            # Fallback jika gagal parse
            data = {
                "merchant": "Tidak Terbaca",
                "date": today_str,
                "total_amount": "0",
                "items_summary": "Gagal membaca detail",
                "confidence_note": "Error parsing"
            }

        # Post-processing
        numeric_total = self._clean_amount(data.get('total_amount', '0'))
        
        return ExpenseResult(
            merchant=data.get('merchant', 'Tanpa Nama'),
            date=data.get('date', today_str),
            numeric_total=numeric_total,
            items_summary=data.get('items_summary', '-'),
            confidence_note=data.get('confidence_note', ''),
            raw_text=raw_text
        )