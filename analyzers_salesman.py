# analyzers_salesman.py
import json
import requests
import re
from typing import Tuple, Optional
from config import settings
from models import WarungVisionAI
from storage_salesman import log_promotion

class SalesmanAnalyzer:
    """Logika Salesman WA: Generate Caption & Kirim via Fonnte"""

    def __init__(self, ai: WarungVisionAI):
        self.ai = ai

    def _clean_json(self, text: str) -> str:
        """Bersihkan markdown JSON"""
        try:
            match = re.search(r'\{[\s\S]*\}', text)
            return match.group(0) if match else text
        except:
            return text

    # -----------------------
    # NEW: hanya generate caption (tidak langsung kirim)
    # -----------------------
    def generate_caption(self, style: str, image_obj) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate caption using AI (Gemini).
        Returns (caption_text, error_message)
        """
        try:
            raw_ai = self.ai.generate_promo_caption(style, image_obj)
            clean_json = self._clean_json(raw_ai)
            try:
                data_json = json.loads(clean_json)
            except Exception as e_json:
                # jika AI kadang keluarkan teks non-json, coba ambil baris caption mentah
                # fallback: ambil akhir string setelah "caption":
                try:
                    m = re.search(r'"caption"\s*:\s*"(.+?)"', clean_json, re.DOTALL)
                    caption = m.group(1) if m else clean_json.strip().strip('"')
                except:
                    return None, f"Gagal parse JSON AI: {str(e_json)}"
            else:
                caption = data_json.get("caption", "").strip()
                if not caption:
                    return None, "AI mengembalikan caption kosong."
            return caption, None
        except Exception as e:
            return None, f"⚠️ Gagal membuat caption AI: {str(e)}"

    # -----------------------
    # NEW: hanya kirim promosi (pakai caption yang sudah diedit oleh user)
    # -----------------------
    def send_promotion(self, image_path: str, target_phone: str, caption: str) -> Tuple[str, str]:
        """
        Send message + image via Fonnte API.
        Returns (human_readable_message, status)
        status: "SUCCESS", "API_ERROR", "SYSTEM_ERROR", "FAILED"
        """
        try:
            url = settings.FONNTE_URL
            headers = {
                "Authorization": settings.FONNTE_TOKEN
            }

            payload = {
                'target': target_phone,
                'message': caption,
                'countryCode': '62',  # Default ID
                'delay': '2'
            }

            # open file in binary mode
            with open(image_path, 'rb') as img_file:
                files = {
                    'file': img_file
                }
                response = requests.post(url, headers=headers, data=payload, files=files)

            try:
                resp_json = response.json()
            except Exception:
                # jika bukan JSON, log seluruh text
                detail_api = response.text
                status_api = False
            else:
                status_api = resp_json.get("status", False)
                detail_api = resp_json.get("detail", str(resp_json))

            log_status = "SENT" if status_api else "API_ERROR"
            log_promotion(target_phone, payload.get('message', ''), caption, log_status, str(detail_api))

            if status_api:
                return (
                    f"✅ **Sukses Terkirim!**\n\n"
                    f"🎯 **Tujuan:** {target_phone}\n"
                    f"📝 **Caption:**\n_{caption}_",
                    "SUCCESS"
                )
            else:
                return f"❌ **Gagal Kirim Fonnte:** {detail_api}", "FAILED"

        except Exception as e:
            # Log error
            try:
                log_promotion(target_phone, payload.get('message', ''), caption, "SYSTEM_ERROR", str(e))
            except:
                pass
            return f"⚠️ Error Sistem: {str(e)}", "SYSTEM_ERROR"

    # -----------------------
    # KEEP: backward-compatibility wrapper (generate + send)
    # -----------------------
    def process_and_send(self, image_path: str, target_phone: str, style: str, image_obj) -> Tuple[str, str]:
        """
        Legacy single-call: generate caption, then send.
        Returns (result_text, status)
        """
        caption, err = self.generate_caption(style, image_obj)
        if err:
            return err, "FAILED"
        return self.send_promotion(image_path, target_phone, caption)
