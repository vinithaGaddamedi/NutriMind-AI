import os
from typing import Optional

def _load_dotenv_if_present():
    """Load variables from local .env file if available."""
    env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() not in os.environ:
                            os.environ[k.strip()] = v.strip()
        except Exception:
            pass

_load_dotenv_if_present()

# Backward compatible module variables
BASE_URL = os.getenv("BASE_URL", "http://localhost:5173")
API_URL = os.getenv("API_URL", "http://localhost:8000")
ENV = os.getenv("ENV", "QA")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))

class FrameworkConfig:
    """Enterprise Framework Configuration Manager."""
    
    @classmethod
    def get_base_url(cls) -> str:
        return BASE_URL

    @classmethod
    def get_api_url(cls) -> str:
        return API_URL

    @classmethod
    def get_gemini_model(cls) -> str:
        return GEMINI_MODEL

    @classmethod
    def get_timeout(cls) -> int:
        return DEFAULT_TIMEOUT

    @classmethod
    def is_headless(cls) -> bool:
        return HEADLESS
