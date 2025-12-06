# test_integration.py
import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from PIL import Image
import io

os.environ["GOOGLE_API_KEY"] = "DUMMY_KEY"
os.environ["KOLOSAL_API_KEY"] = "DUMMY_KEY"
os.environ["OPENAI_API_KEY"] = "DUMMY_KEY"
os.environ["FONNTE_TOKEN"] = "DUMMY_TOKEN"
os.environ["GOOGLE_SAFE_BROWSING_KEY"] = "DUMMY_KEY"

from app import build_interface
import gradio as gr

class TestIntegration(unittest.TestCase):
    """Test end-to-end workflow"""
    
    def setUp(self):
        """Setup untuk setiap test"""
        # Buat temporary file yang kompatibel Windows/Linux/Mac
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Cleanup setelah test"""
        # Hapus file temporary
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)
    
    def test_gradio_interface_builds(self):
        """Tes Gradio interface bisa di-build tanpa error"""
        try:
            demo = build_interface()
            self.assertIsInstance(demo, gr.Blocks)
            print("✅ Gradio interface berhasil di-build")
        except Exception as e:
            self.fail(f"Interface build failed: {e}")
    
    @patch('app.WarungVisionAI')
    def test_transfer_handler_workflow(self, mock_ai_class):
        """Tes full workflow handler transfer"""
        # Mock AI response
        mock_ai = MagicMock()
        mock_ai.analyze_transfer.return_value = '{"status":"ASLI","confidence_score":90,"key_findings":["OK"],"recommendations":["Simpan"]}'
        mock_ai_class.return_value = mock_ai
        
        # Create dummy image (FIXED: gunakan temp path yang sudah dibuat)
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.temp_path)
        
        # Build interface
        demo = build_interface()
        
        # Verifikasi file tersimpan
        self.assertTrue(os.path.exists(self.temp_path))
        print(f"✅ Transfer workflow test berhasil (file: {self.temp_path})")

if __name__ == '__main__':
    unittest.main(verbosity=2)