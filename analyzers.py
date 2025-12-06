# analyzers.py
from dataclasses import dataclass
from typing import Optional, Any, List
import json
import re  # Penting untuk membersihkan output AI

from models import WarungVisionAI


# =========================
# Dataclasses hasil analisis
# =========================

@dataclass
class TransferResult:
    status: str
    confidence: int
    findings: List[str]
    recommendations: List[str]
    raw_text: str


@dataclass
class InventoryCategory:
    name: str
    status: str
    notes: Optional[str] = None


@dataclass
class InventoryResult:
    categories: List[InventoryCategory]
    summary: str
    raw_text: str


# =========================
# Transfer Verifier
# =========================

class TransferVerifier:
    """
    Layer logika bisnis untuk verifikasi bukti transfer.
    """

    def __init__(self, ai: WarungVisionAI):
        self.ai = ai

    def _clean_json_string(self, text: str) -> str:
        """
        Membersihkan string dari markdown code block (```json ... ```)
        dan mencari kurung kurawal pertama dan terakhir.
        """
        try:
            # Cari substring yang diawali { dan diakhiri }
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return match.group(0)
            return text
        except Exception:
            return text

    def _parse_json(self, text: str) -> TransferResult:
        """
        Parse string JSON dari model menjadi TransferResult.
        """
        clean_text = self._clean_json_string(text)

        # Default fallback kalau semuanya gagal
        fallback = TransferResult(
            status="PERLU DICEK LAGI",
            confidence=50,
            findings=["Analisis otomatis kurang jelas, mohon cek manual."],
            recommendations=[
                "Cek mutasi rekening dan pastikan dana benar-benar masuk.",
                "Jangan serahkan barang sebelum saldo bertambah."
            ],
            raw_text=text,
        )

        try:
            data = json.loads(clean_text)
        except Exception:
            return fallback

        # Status
        raw_status = str(data.get("status", "")).strip().upper()
        allowed_status = {
            "ASLI",
            "PERLU DICEK LAGI",
            "MENCURIGAKAN",
            "DIDUGA PALSU",
        }
        status = raw_status if raw_status in allowed_status else "PERLU DICEK LAGI"

        # Confidence
        confidence = data.get("confidence_score", 0)
        try:
            confidence = int(confidence)
        except Exception:
            confidence = 0
        if confidence < 0: confidence = 0
        if confidence > 100: confidence = 100

        # Findings (Temuan)
        findings_raw = (
            data.get("key_findings")
            or data.get("findings")
            or data.get("temuan")
            or []
        )
        if isinstance(findings_raw, str):
            findings_list = [findings_raw]
        else:
            findings_list = list(findings_raw)

        findings: List[str] = [
            str(f).strip() for f in findings_list if str(f).strip()
        ]
        
        if not findings:
            findings = ["Tidak ada temuan spesifik, namun harap waspada."]

        # Recommendations (Saran)
        rec_raw = (
            data.get("recommendations")
            or data.get("rekomendasi")
            or data.get("recommendation")
            or []
        )
        if isinstance(rec_raw, str):
            rec_list = [rec_raw]
        else:
            rec_list = list(rec_raw)

        recommendations: List[str] = [
            str(r).strip() for r in rec_list if str(r).strip()
        ]
        if not recommendations:
            recommendations = [
                "Cek mutasi rekening di aplikasi bank / e-wallet.",
                "Kalau ragu, tahan barang sampai dana masuk.",
            ]

        return TransferResult(
            status=status,
            confidence=confidence,
            findings=findings,
            recommendations=recommendations,
            raw_text=text,
        )

    def verify(self, notes: str, image: Optional[Any]) -> TransferResult:
        text = self.ai.analyze_transfer(notes, image)
        return self._parse_json(text)


# =========================
# Inventory Analyzer
# =========================

class InventoryAnalyzer:
    """
    Layer logika bisnis untuk smart photo inventory.
    """

    def __init__(self, ai: WarungVisionAI):
        self.ai = ai
    
    def _clean_json_string(self, text: str) -> str:
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return match.group(0)
            return text
        except Exception:
            return text

    def _parse_json(self, text: str) -> InventoryResult:
        """
        Parse string JSON dari model menjadi InventoryResult.
        """
        clean_text = self._clean_json_string(text)
        
        # Fallback
        fallback_category = InventoryCategory(
            name="Umum",
            status="PERLU CEK MANUAL",
            notes="Foto kurang jelas atau analisis terkendala.",
        )
        fallback_result = InventoryResult(
            categories=[fallback_category],
            summary="Silakan cek stok secara langsung di rak.",
            raw_text=text,
        )

        try:
            data = json.loads(clean_text)
        except Exception:
            return fallback_result

        categories_data = data.get("categories") or []
        categories: List[InventoryCategory] = []

        allowed_status = {"AMAN", "MULAI MENIPIS", "HAMPIR HABIS"}

        if isinstance(categories_data, dict):
            categories_data = [categories_data]

        if isinstance(categories_data, list):
            for item in categories_data:
                try:
                    name = str(item.get("name", "Tanpa nama")).strip()
                    status_raw = str(item.get("status", "")).strip().upper()
                    status = status_raw if status_raw in allowed_status else "MULAI MENIPIS"
                    
                    notes = item.get("notes")
                    if notes is not None:
                        notes = str(notes).strip()
                    
                    categories.append(
                        InventoryCategory(
                            name=name or "Tanpa nama",
                            status=status,
                            notes=notes,
                        )
                    )
                except Exception:
                    continue

        if not categories:
            categories = [fallback_category]

        summary = data.get("summary") or data.get("ringkasan") or ""
        summary = str(summary).strip() or "Cek stok manual."

        return InventoryResult(
            categories=categories,
            summary=summary,
            raw_text=text,
        )

    def analyze(self, notes: str, image: Optional[Any]) -> InventoryResult:
        text = self.ai.analyze_inventory(notes, image)
        return self._parse_json(text)