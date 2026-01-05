from datetime import datetime


def now_iso() -> str:
    """現在時刻を ISO 8601 で返す"""
    return datetime.utcnow().isoformat()
