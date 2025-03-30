from dotenv import load_dotenv
import os
from pathlib import Path

# Resolve path to the parent directory
dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path)

print("Username:", os.getenv("GRAFANA_USERNAME"))
print("API Key:", os.getenv("GRAFANA_API_KEY"))
