"""Utility functions for the Spider LCD client."""

import json
from typing import Any, Dict


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as pretty JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def get_nested(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Get value from nested dictionary using dot notation.
    
    Example:
        data = {"departure": {"nextDepartureIn": "5 min"}}
        get_nested(data, "departure.nextDepartureIn")  # => "5 min"
        get_nested(data, "departure.missing", "N/A")   # => "N/A"
    
    Args:
        data: Dictionary to search in
        path: Path with dot notation, e.g. "user.address.city"
        default: Value to return if key is not found
    
    Returns:
        The value at the specified path or default
    """
    keys = path.split(".")
    value = data
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value