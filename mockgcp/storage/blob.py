from mockgcp.storage import backend
from mockgcp.storage.bucket import MockBucket

from google.cloud.storage import Blob

from six.moves.urllib.parse import quote
from six.moves.urllib.parse import urlsplit


class MockBlob:
    def __init__(
        self,
        name,
        bucket,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        self.name = name
        self._bucket = bucket
        self._backend = backend.backend

    @property
    def bucket(self):
        return self._bucket

    @property
    def client(self):
        return self.bucket.client

    @property
    def path(self):
        if not self.name:
            raise ValueError("Cannot determine path without a blob name.")
        # TODO: Make sure this is the same output as the original function
        return self.bucket.path + "/" + self.name

    def exists(self, client=None):
        if self.name in self._backend.blobs[self.bucket.name].keys():
            return True
        else:
            return False

    def delete(self, client=None):
        return self.bucket.delete_blob(
            self.name, client=client, generation=self.generation
        )

    @classmethod
    def from_string(cls, uri, client=None):
        scheme, netloc, path, query, frag = urlsplit(uri)
        if scheme != "gs":
            raise ValueError("URI scheme must be gs")

        bucket = MockBucket(client, name=netloc)
        return cls(path[1:], bucket)
    

