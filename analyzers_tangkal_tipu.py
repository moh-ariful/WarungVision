import re
import requests
import whois
import json
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional, Any, Dict

from config import settings
from models_tangkal_tipu import HybridScamAI
# Kita gunakan existing WarungVisionAI hanya untuk OCR (baca gambar)
from models import WarungVisionAI 

class ScamAnalyzer:
    def __init__(self, vision_ai: WarungVisionAI):
        self.vision_ai = vision_ai # Dipakai untuk OCR
        self.kolosal_ai = HybridScamAI()

    def _extract_urls(self, text: str) -> list:
        """
        Mengambil semua URL dari teks menggunakan Regex yang lebih fleksibel.
        Bisa menangkap:
        - https://contoh.com
        - http://contoh.com
        - www.contoh.com
        - subdomain.contoh.co.id
        """
        # Regex diperbaiki untuk menangkap www. dan domain tanpa protokol
        url_pattern = r'(?:(?:https?://)|(?:www\.))[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        found_urls = re.findall(url_pattern, text)
        
        # Bersihkan hasil (kadang ada karakter sisa di ujung)
        cleaned_urls = [u.rstrip('.,)]}') for u in found_urls]
        return cleaned_urls

    def _check_safe_browsing(self, url: str) -> str:
        """Cek URL ke Google Safe Browsing API"""
        if not settings.GOOGLE_SAFE_BROWSING_KEY:
            return "Tidak dicek (API Key missing)"
        
        # Google Safe Browsing butuh format full URI
        check_url = url
        if not check_url.startswith("http"):
            check_url = f"http://{check_url}"

        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={settings.GOOGLE_SAFE_BROWSING_KEY}"
        payload = {
            "client": {"clientId": "warungvision", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": check_url}]
            }
        }
        try:
            r = requests.post(api_url, json=payload, timeout=5)
            # Jika ada matches, berarti berbahaya
            if r.status_code == 200 and "matches" in r.json():
                return "🚨 TERDETEKSI BERBAHAYA oleh Google!"
            return "✅ Aman (Belum terdaftar di blacklist Google)"
        except Exception as e:
            return f"Gagal koneksi ke Safe Browsing: {str(e)}"

    def _check_whois(self, url: str) -> str:
        """Cek umur domain menggunakan library python-whois"""
        try:
            # Bersihkan protokol dan path untuk ambil domain utama
            clean_domain = url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
            
            w = whois.whois(clean_domain)
            
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if not creation_date:
                return "⚠️ Data domain disembunyikan (Private WHOIS)"

            age_days = (datetime.now() - creation_date).days
            if age_days < 30:
                return f"🚩 SANGAT BARU ({age_days} hari). Indikasi Penipuan!"
            return f"✅ Domain sudah lama ({age_days} hari)."
        except Exception:
            # WHOIS sering gagal kalau domainnya aneh/subdomain
            return "⚠️ Gagal mengambil data WHOIS (Mungkin subdomain)"

    def _scan_page_content(self, url: str) -> str:
        """Scraping ringan untuk cari input sensitif"""
        try:
            # Pastikan ada protokol
            target_url = url
            if not target_url.startswith("http"):
                target_url = f"http://{target_url}"

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            r = requests.get(target_url, headers=headers, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            inputs = soup.find_all('input')
            sensitive_keywords = ['password', 'sandi', 'pin', 'nik', 'atm', 'cvv', 'kartu']
            found = []
            
            for i in inputs:
                name = i.get('name', '').lower()
                placeholder = i.get('placeholder', '').lower()
                i_type = i.get('type', '').lower()
                
                for kw in sensitive_keywords:
                    if kw in name or kw in placeholder or i_type == 'password':
                        found.append(kw)
            
            if found:
                return f"⚠️ Ditemukan form input sensitif: {', '.join(set(found))}"
            return "ℹ️ Tidak ditemukan form login mencurigakan."
        except Exception:
            return "❌ Gagal membuka website (Mungkin sudah diblokir/mati)"

    def analyze(self, image: Optional[Any]) -> Dict[str, Any]:
        """
        Flow Utama Tangkal Tipu:
        1. OCR Image via Gemini (WarungVisionAI)
        2. Technical Check (Regex, SafeBrowsing, Whois)
        3. Context Analysis via Kolosal AI
        """
        # Langkah 1: Ekstraksi Teks (OCR)
        ocr_prompt = (
            "Ekstrak semua teks yang ada di gambar ini secara presisi. "
            "Jangan lewatkan URL, link, atau nomor telepon. "
            "Tulis apa adanya tanpa komentar."
        )
        # Gunakan method _generate milik class WarungVisionAI
        extracted_text = self.vision_ai._generate([ocr_prompt, image]) if image else ""

        # Langkah 2: Technical Check
        urls = self._extract_urls(extracted_text)
        tech_findings = []
        
        extracted_url = "-"
        if urls:
            extracted_url = urls[0] # Ambil URL pertama yg ditemukan
            tech_findings.append(f"🔗 URL Ditemukan: {extracted_url}")
            tech_findings.append(f"🛡️ Safe Browsing: {self._check_safe_browsing(extracted_url)}")
            tech_findings.append(f"📅 WHOIS Domain: {self._check_whois(extracted_url)}")
            tech_findings.append(f"🕵️ Analisis Web: {self._scan_page_content(extracted_url)}")
        else:
            tech_findings.append("ℹ️ Tidak ditemukan URL/Link aktif dalam gambar.")

        tech_summary = "; ".join(tech_findings)

        # Langkah 3: Kolosal AI Analysis
        ai_result_json = self.kolosal_ai.analyze_context(extracted_text, tech_summary)
        
        # Parse JSON output dari Kolosal
        try:
            clean_json = ai_result_json.replace("```json", "").replace("```", "").strip()
            # Kadang AI memberi teks sebelum JSON, cari kurung kurawal
            start = clean_json.find('{')
            end = clean_json.rfind('}') + 1
            if start != -1 and end != -1:
                clean_json = clean_json[start:end]
                
            result = json.loads(clean_json)
        except:
            # Fallback jika JSON rusak
            result = {
                "status": "PERLU WASPADA", 
                "reason": "AI memberikan respon tidak baku, tapi harap hati-hati karena sistem mendeteksi kejanggalan.",
                "action": "Jangan klik link sembarangan dan abaikan pesan."
            }

        return {
            "text": extracted_text,
            "url": extracted_url,
            "tech_data": tech_findings,
            "final_verdict": result
        }