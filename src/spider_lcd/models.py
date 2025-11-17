"""Data models for API responses."""

from typing import Any, Dict


class APIResponse:
    """Simple class representing an API response."""
    
    def __init__(
        self,
        status_code: int,
        data: Dict[str, Any],
        headers: Dict[str, str] = None,
        success: bool = True
    ):
        """
        Initialize an API response.
        
        Args:
            status_code: HTTP status code
            data: Response data (parsed JSON)
            headers: Response headers
            success: Whether the request was successful
        """
        self.status_code = status_code
        self.data = data
        self.headers = headers or {}
        self.success = success
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get value from response data.
        
        Supports both simple key and nested 'dot notation':
        - get_data("title") => data["title"]
        - get_data("departure.nextDepartureIn") => data["departure"]["nextDepartureIn"]
        
        Args:
            key: Key or path (with dots for nested data)
            default: Value to return if key doesn't exist
        
        Returns:
            The value or default
        """
        # Om nyckeln innehåller punkt, använd nästlad hämtning
        if "." in key:
            from .utils import get_nested
            return get_nested(self.data, key, default)
        
        # Annars, enkel dictionary-åtkomst
        return self.data.get(key, default)
    
    def has_key(self, key: str) -> bool:
        """Check if a key exists in the response data."""
        return key in self.data