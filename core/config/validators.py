import re

def validate_database_url(url: str) -> bool:
    """
    Validates that a URL conforms to standard postgres or postgresql connection schemes.
    """
    pattern = r"^postgres(ql)?://.+:.+@.+:.+/.+$"
    return bool(re.match(pattern, url))

def validate_secret_strength(secret: str) -> bool:
    """
    Ensures that secrets are not using trivial settings in production scopes.
    """
    return len(secret.strip()) >= 16
