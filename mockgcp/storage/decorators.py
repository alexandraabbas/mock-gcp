from unittest.mock import patch

from mockgcp.storage.client import Client


def mock_storage(func):
    def wrapper(*args, **kwargs):
        with patch("google.cloud.storage.Client", Client):
            return func(*args, **kwargs)

    return wrapper
