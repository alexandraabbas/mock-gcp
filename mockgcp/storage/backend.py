import uuid
import functools
from unittest.mock import patch

from mockgcp.storage.client import MockClient


class StorageBackend(object):
    def __init__(self, project=None):
        if project is None:
            project = "test-project-" + str(uuid.uuid1())
        self.project = project
        self.buckets = {}
        self.blobs = {}

    def reset(self):
        self.buckets = {}
        self.blobs = {}

    def mock_storage(self, func):
        def wrapper(*args, **kwargs):
            self.reset()
            with patch("google.cloud.storage.Client", MockClient):
                return func(*args, **kwargs)

        functools.update_wrapper(wrapper, func)
        wrapper.__wrapped__ = func
        return wrapper


backend = StorageBackend()
mock_storage = backend.mock_storage
