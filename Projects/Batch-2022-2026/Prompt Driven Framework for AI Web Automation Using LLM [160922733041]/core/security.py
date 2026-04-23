"""Security utilities: URL validation, API key masking, rate limiting."""

import re
import time
from urllib.parse import urlparse
from collections import defaultdict


# --- URL Validation ---

BLOCKED_SCHEMES = {"file", "ftp", "data", "javascript"}

BLOCKED_HOSTS = {
    "0.0.0.0",
    "metadata.google.internal",
    "169.254.169.254",  # AWS/cloud metadata
}

INTERNAL_IP_PATTERNS = [
    re.compile(r"^127\."),             # 127.x.x.x
    re.compile(r"^10\."),              # 10.x.x.x
    re.compile(r"^192\.168\."),        # 192.168.x.x
    re.compile(r"^172\.(1[6-9]|2\d|3[01])\."),  # 172.16-31.x.x
]


def validate_url(url, allow_localhost=False):
    """Validate a URL for safety.

    Args:
        url: URL string to validate
        allow_localhost: If True, allow localhost URLs (for demo form)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not url:
        return False, "URL is required."

    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format."

    # Check scheme
    scheme = parsed.scheme.lower()
    if scheme in BLOCKED_SCHEMES:
        return False, f"URL scheme '{scheme}://' is not allowed."

    if scheme not in ("http", "https"):
        return False, f"Only http:// and https:// URLs are allowed."

    # Check host
    host = parsed.hostname or ""
    host_lower = host.lower()

    if not host:
        return False, "URL must include a hostname."

    # Block known dangerous hosts
    if host_lower in BLOCKED_HOSTS:
        return False, f"Access to '{host}' is blocked for security."

    # Check localhost
    if host_lower in ("localhost", "127.0.0.1", "::1") and not allow_localhost:
        return False, "Access to localhost is not allowed. Use the demo form button instead."

    # Check internal/private IPs
    if not allow_localhost:
        for pattern in INTERNAL_IP_PATTERNS:
            if pattern.match(host):
                return False, f"Access to internal/private IP addresses is blocked."

    return True, None


# --- API Key Masking ---

API_KEY_PATTERN = re.compile(r"sk-ant-[a-zA-Z0-9_\-]{10,}")


def mask_sensitive(text):
    """Mask API keys and other sensitive data in text."""
    if not isinstance(text, str):
        return text
    return API_KEY_PATTERN.sub("sk-ant-***MASKED***", text)


# --- Rate Limiting ---

class RateLimiter:
    """Simple in-memory rate limiter by IP address."""

    def __init__(self, max_requests=5, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(list)

    def is_allowed(self, ip):
        """Check if a request from this IP is allowed.

        Returns:
            tuple: (allowed: bool, retry_after: int or None)
        """
        now = time.time()
        cutoff = now - self.window_seconds

        # Clean old entries
        self._requests[ip] = [t for t in self._requests[ip] if t > cutoff]

        if len(self._requests[ip]) >= self.max_requests:
            oldest = self._requests[ip][0]
            retry_after = int(oldest + self.window_seconds - now) + 1
            return False, retry_after

        self._requests[ip].append(now)
        return True, None


# Global rate limiter instance
agent_rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
