# test.py
import unittest
import json
import os
from unittest.mock import MagicMock, patch, ANY

# Set dummy env vars sebelum import config
os.environ["GOOGLE_API_KEY"] = "DUMMY_KEY"
os.environ["KOLOSAL_API_KEY"] = "DUMMY_KEY" 
os.environ["FONNTE_TOKEN"] = "DUMMY_TOKEN"

# Import modul yang akan ditest
from models import WarungVisionAI
from analyzers import TransferVerifier, InventoryAnalyzer, TransferResult, InventoryResult
from analyzers_expense import ExpenseAnalyzer
from analyzers_salesman import SalesmanAnalyzer
from analyzers_tangkal_tipu import ScamAnalyzer

class TestWarungVision(unittest.TestCase):

    def setUp(self):
        """Setup awal untuk setiap test case"""
        # Mock WarungVisionAI agar tidak panggil API asli
        self.mock_ai = MagicMock(spec=WarungVisionAI)
        # Bypass validasi API Key di init
        self.mock_ai.model = MagicMock() 

    # ----------------------------------------------------------------
    # 1. TEST TRANSFER VERIFIER
    # ----------------------------------------------------------------
    def test_transfer_verify_valid_json(self):
        """Tes parsing JSON valid dari Transfer Verifier"""
        json_resp = json.dumps({
            "status": "ASLI",
            "confidence_score": 95,
            "key_findings": ["Font konsisten", "Nominal wajar"],
            "recommendations": ["Simpan bukti"]
        })
        self.mock_ai.analyze_transfer.return_value = f"```json\n{json_resp}\n```"

        verifier = TransferVerifier(self.mock_ai)
        result = verifier.verify("Cek nominal", None)

        self.assertIsInstance(result, TransferResult)
        self.assertEqual(result.status, "ASLI")
        self.assertEqual(result.confidence, 95)
        self.assertEqual(len(result.findings), 2)

    def test_transfer_verify_broken_json(self):
        """Tes fallback jika AI return JSON rusak"""
        self.mock_ai.analyze_transfer.return_value = "Maaf saya tidak bisa analisa."

        verifier = TransferVerifier(self.mock_ai)
        result = verifier.verify("", None)

        self.assertEqual(result.status, "PERLU DICEK LAGI")
        self.assertEqual(result.confidence, 50)
        self.assertIn("kurang jelas", result.findings[0])

    # ----------------------------------------------------------------
    # 2. TEST INVENTORY ANALYZER
    # ----------------------------------------------------------------
    def test_inventory_parsing(self):
        """Tes parsing kategori stok barang"""
        json_resp = json.dumps({
            "categories": [
                {"name": "Minyak", "status": "AMAN", "notes": "Penuh"},
                {"name": "Beras", "status": "HAMPIR HABIS", "notes": "Sisa 1"}
            ],
            "summary": "Belanja beras segera."
        })
        self.mock_ai.analyze_inventory.return_value = json_resp

        analyzer = InventoryAnalyzer(self.mock_ai)
        result = analyzer.analyze("Cek sembako", None)

        self.assertIsInstance(result, InventoryResult)
        self.assertEqual(len(result.categories), 2)
        self.assertEqual(result.categories[1].status, "HAMPIR HABIS")

    # ----------------------------------------------------------------
    # 3. TEST EXPENSE ANALYZER (BUG FIX CHECK)
    # ----------------------------------------------------------------
    def test_expense_amount_cleaning(self):
        """Tes pembersihan format mata uang"""
        # Input AI: Format Rp dengan desimal ,00 (Standar Indonesia)
        json_resp = json.dumps({
            "merchant": "Toko Makmur",
            "date": "01/01/2025",
            "total_amount": "Rp 50.000,00", 
            "items_summary": "Rokok"
        })
        self.mock_ai._generate.return_value = json_resp

        analyzer = ExpenseAnalyzer(self.mock_ai)
        result = analyzer.analyze(None)

        # Logic baru harusnya membuang suffix ,00
        # Rp 50.000,00 -> 50000.0 (SEHARUSNYA BENAR SEKARANG)
        self.assertEqual(result.numeric_total, 50000.0)
        self.assertEqual(result.merchant, "Toko Makmur")

    # ----------------------------------------------------------------
    # 4. TEST SALESMAN WA
    # ----------------------------------------------------------------
    @patch('requests.post')
    def test_salesman_send_success(self, mock_post):
        """Tes logika pengiriman API Fonnte sukses"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": True, "detail": "Sent"}
        mock_post.return_value = mock_response

        with patch("builtins.open", unittest.mock.mock_open(read_data=b"img_data")):
            sales = SalesmanAnalyzer(self.mock_ai)
            msg, status = sales.send_promotion("dummy.jpg", "08123", "Promo Murah!")

        self.assertEqual(status, "SUCCESS")
        self.assertIn("Sukses Terkirim", msg)
        mock_post.assert_called_once()

    # ----------------------------------------------------------------
    # 5. TEST SCAM ANALYZER
    # ----------------------------------------------------------------
    def test_scam_analyzer_workflow(self):
        """Tes alur OCR -> Ekstraksi URL -> AI Verdict"""
        # 1. Mock OCR (Vision AI)
        self.mock_ai._generate.return_value = "Silakan klik https://penipu.com segera."
        
        # 2. Mock Kolosal/Hybrid AI logic
        analyzer = ScamAnalyzer(self.mock_ai)
        analyzer.kolosal_ai.analyze_context = MagicMock(return_value=json.dumps({
            "status": "BERBAHAYA",
            "reason": "Phishing link",
            "action": "Blokir"
        }))

        # 3. Mock Network checks
        analyzer._check_safe_browsing = MagicMock(return_value="Aman")
        analyzer._check_whois = MagicMock(return_value="Domain Baru")
        analyzer._scan_page_content = MagicMock(return_value="Login Form")

        # FIX: Kirim string sebagai image agar logic if image: jalan
        result = analyzer.analyze("dummy_image_data") 

        self.assertEqual(result["final_verdict"]["status"], "BERBAHAYA")
        self.assertIn("https://penipu.com", result["tech_data"][0])
        self.mock_ai._generate.assert_called_once()

    # ----------------------------------------------------------------
    # 6. TEST PROMPT UPDATE
    # ----------------------------------------------------------------
    @patch("google.generativeai.GenerativeModel")
    def test_prompt_includes_user_notes(self, MockModel):
        """Tes apakah catatan user masuk ke prompt Gemini"""
        real_ai = WarungVisionAI()
        real_ai.model = MockModel()
        
        mock_response = MagicMock()
        mock_response.text = "{}"
        real_ai.model.generate_content.return_value = mock_response

        user_note = "Cek apakah ini editan sotosop?"
        real_ai.analyze_transfer(user_note, None)

        call_args = real_ai.model.generate_content.call_args[0][0]
        full_prompt = call_args[0]

        self.assertIn("KONTEKS KHUSUS DARI USER", full_prompt)
        self.assertIn(user_note, full_prompt)

if __name__ == '__main__':
    unittest.main()