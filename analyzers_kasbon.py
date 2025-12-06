# analyzers_kasbon.py
import json
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from models import WarungVisionAI

@dataclass
class KasbonResult:
    customer_name: str
    items_summary: str
    numeric_amount: float
    due_date: str
    raw_text: str
    status: str # SUCCESS atau FAILED

class KasbonAnalyzer:
    """
    Logika ekstraksi data hutang dari Audio (Voice Processing).
    """
    def __init__(self, ai: WarungVisionAI):
        self.ai = ai

    def _clean_amount(self, amount_val: Any) -> float:
        """Bersihkan format angka/uang jadi float"""
        try:
            s = str(amount_val).strip()
            # Hapus Rp, titik, koma, spasi
            clean = re.sub(r'[^\d]', '', s)
            return float(clean) if clean else 0.0
        except:
            return 0.0

    def analyze(self, audio_path: str) -> KasbonResult:
        """
        Proses audio menjadi data hutang terstruktur.
        """
        if not audio_path:
            return KasbonResult("-", "-", 0.0, "-", "No audio file", "FAILED")

        # 1. Kirim audio ke AI
        raw_text = self.ai.analyze_kasbon_audio(audio_path)

        # 2. Parsing JSON
        try:
            # Bersihkan markdown json jika ada
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            start = clean_json.find('{')
            end = clean_json.rfind('}') + 1
            if start != -1 and end != -1:
                clean_json = clean_json[start:end]
            
            data = json.loads(clean_json)
        except Exception as e:
            # Fallback jika gagal parse
            return KasbonResult(
                customer_name="Gagal Baca",
                items_summary="-",
                numeric_amount=0.0,
                due_date="-",
                raw_text=raw_text,
                status="FAILED"
            )

        # 3. Normalisasi Data
        # Ambil items dan gabungkan jadi string jika list
        items_raw = data.get("items", [])
        if isinstance(items_raw, list):
            items_str = ", ".join([str(i) for i in items_raw])
        else:
            items_str = str(items_raw)

        amount = self._clean_amount(data.get("amount", 0))

        return KasbonResult(
            customer_name=data.get("customer_name", "Tanpa Nama"),
            items_summary=items_str,
            numeric_amount=amount,
            due_date=data.get("due_date_note", "Tidak disebutkan"),
            raw_text=raw_text,
            status="SUCCESS"
        )