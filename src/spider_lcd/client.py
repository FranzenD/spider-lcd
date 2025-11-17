"""Simple API Client for making GET requests and handling JSON responses."""

import json
import logging
from typing import Any, Dict, Optional

import requests

from .exceptions import APIError
from .models import APIResponse


logger = logging.getLogger(__name__)


class APIClient:
    """Simple HTTP client for making GET requests."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize the API client.

        Args:
            base_url: The base URL for the API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        
        # Set default headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        # Set authentication if provided
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def _build_url(self, endpoint: str) -> str:
        """Build the full URL for an endpoint."""
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> APIResponse:
        """Handle the HTTP response and convert to APIResponse."""
        try:
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                # If not JSON, store raw text
                data = {"raw_content": response.text}
            
            return APIResponse(
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                success=True
            )
            
        except requests.exceptions.HTTPError:
            # Handle HTTP errors
            try:
                error_data = response.json()
            except json.JSONDecodeError:
                error_data = {"error": response.text}
            
            raise APIError(
                f"HTTP {response.status_code}: {response.reason}",
                status_code=response.status_code,
                response_data=error_data
            )

    def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
    ) -> APIResponse:
        """
        Make a GET request to the specified endpoint.

        Args:
            endpoint: The API endpoint (relative to base_url)
            params: Query parameters to include in the request

        Returns:
            APIResponse object containing the response data

        Raises:
            APIError: If the request fails
        """
        url = self._build_url(endpoint)
        
        try:
            logger.info(f"Making GET request to {url}")
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
            
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise APIError(f"Request failed: {str(e)}")