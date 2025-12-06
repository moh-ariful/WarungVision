# config.py
from dataclasses import dataclass
from dotenv import load_dotenv
import os

# Load variabel dari file .env
load_dotenv()

@dataclass
class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # --- Config Tangkal Tipu (Hybrid AI) ---
    KOLOSAL_API_KEY: str = os.getenv("KOLOSAL_API_KEY", "")
    KOLOSAL_BASE_URL: str = "https://api.kolosal.ai/v1"
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    GOOGLE_SAFE_BROWSING_KEY: str = os.getenv("GOOGLE_SAFE_BROWSING_KEY", "")
    # ---------------------------------------

    # --- Config Fonnte (Salesman WA) ---
    FONNTE_TOKEN: str = os.getenv("FONNTE_TOKEN", "")
    FONNTE_URL: str = "https://api.fonnte.com/send"

    GRADIO_TITLE: str = "WarungVision – Asisten AI Warung"
    GRADIO_THEME: str = "soft"
    GRADIO_SERVER_NAME: str = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    GRADIO_SERVER_PORT: int = int(os.getenv("GRADIO_SERVER_PORT", "7860"))

    DEBUG: bool = True


settings = Settings()