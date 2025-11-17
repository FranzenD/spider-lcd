"""Spider LCD - Simple Python client for making GET requests and handling JSON data."""

__version__ = "0.1.0"

from .client import APIClient
from .models import APIResponse
from .exceptions import APIError
from .utils import get_nested

__all__ = ["APIClient", "APIResponse", "APIError", "get_nested"]