import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


def load_config(path: str | None = None) -> dict:
    load_dotenv(ROOT / ".env")
    cfg_path = Path(path) if path else ROOT / "config.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    key = os.getenv("G2B_SERVICE_KEY", "").strip().strip('"').strip("'")
    if "%" in key:  # 포털이 Encoding 키만 보여주는 경우 → 자동 디코딩
        from urllib.parse import unquote
        key = unquote(key)
    cfg["g2b"]["service_key"] = key
    return cfg
