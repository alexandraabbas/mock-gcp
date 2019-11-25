from six.moves.urllib.parse import urlsplit

from google.cloud.exceptions import NotFound
from google.cloud.storage._helpers import _validate_name

from mockgcp.storage import backend
from mockgcp.storage.blob import MockBlob


class MockBucket:
    def __init__(self, client, name=None, user_project=None):
        name = _validate_name(name)
        self.name = name
        self._client = client
        self._user_project = user_project
        self._blobs = []
        self._backend = backend.backend

    def __repr__(self):
        return "<Bucket: %s>" % (self.name,)

    @property
    def client(self):
        return self._client

    @property
    def user_project(self):
        return self._user_project

    @classmethod
    def from_string(cls, uri, client=None):
        scheme, netloc, path, query, frag = urlsplit(uri)

        if scheme != "gs":
            raise ValueError("URI scheme must be gs")

        return cls(client, name=netloc)

    def blob(
        self,
        blob_name,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        raise NotImplementedError

    def notification(
        self,
        topic_name,
        topic_project=None,
        custom_attributes=None,
        event_types=None,
        blob_name_prefix=None,
        # payload_format=NONE_PAYLOAD_FORMAT,
    ):
        raise NotImplementedError

    def exists(self, client=None):
        if self.name in self.backend.buckets.keys():
            return True
        else:
            return False

    def create(
        self,
        client=None,
        project=None,
        location=None,
        predefined_acl=None,
        predefined_default_object_acl=None,
    ):
        if self.user_project is not None:
            raise ValueError("Cannot create bucket with 'user_project' set.")

        if project is None:
            project = client.project

        if project is None:
            raise ValueError("Client project not set:  pass an explicit project.")

        self._backend[self.name] = self

    def patch(self, client=None):
        raise NotImplementedError

    @property
    def acl(self):
        raise NotImplementedError

    @property
    def default_object_acl(self):
        raise NotImplementedError

    @staticmethod
    def path_helper(bucket_name):
        return "/b/" + bucket_name

    @property
    def path(self):
        if not self.name:
            raise ValueError("Cannot determine path without bucket name.")

        return self.path_helper(self.name)

    def get_blob(
        self, blob_name, client=None, encryption_key=None, generation=None, **kwargs
    ):
        if blob_name in self.backend.blobs[self.name]:
            return MockBlob(
                bucket=self,
                name=blob_name,
                encryption_key=encryption_key,
                generation=generation,
                **kwargs
            )
        else:
            return None

    def list_blobs(
        self,
        max_results=None,
        page_token=None,
        prefix=None,
        delimiter=None,
        versions=None,
        projection="noAcl",
        fields=None,
        client=None,
    ):
        if isinstance(max_results, int):
            blobs = list(self.backend.blobs[self.name])[:max_results]
        else:
            blobs = list(self.backend.blobs[self.name])

        if isinstance(delimiter, str):
            raise NotImplementedError

        if isinstance(prefix, str):
            raise NotImplementedError

        extra_params = {"projection": projection}

        client = self._require_client(client)
        path = self.path + "/o"
        # iterator = page_iterator.HTTPIterator(
        #     client=client,
        #     api_request=client._connection.api_request,
        #     path=path,
        #     item_to_value=_item_to_blob,
        #     page_token=page_token,
        #     max_results=max_results,
        #     extra_params=extra_params,
        #     page_start=_blobs_page_start,
        # )
        # iterator.bucket = self
        # iterator.prefixes = set()
        # return iterator
