# tools.py
from typing import Dict, Any
import datetime

def get_current_time(_: Dict[str, Any]) -> Dict[str, Any]:
    """Return the current UTC time."""
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {"time_utc": now}

def add_numbers(params: Dict[str, Any]) -> Dict[str, Any]:
    """Add two numbers."""
    a = params.get("a")
    b = params.get("b")
    return {"result": a + b}

