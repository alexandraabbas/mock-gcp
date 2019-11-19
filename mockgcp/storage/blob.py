from mockgcp.storage import backend

from google.cloud.storage import Blob

# from six.moves.urllib.parse import quote

# from google.cloud._helpers import _bytes_to_unicode
# from google.cloud._helpers import _to_bytes
from google.cloud.exceptions import NotFound


class MockBlob(Blob):
    _chunk_size = None
    _CHUNK_SIZE_MULTIPLE = 256 * 1024

    def __init__(
        self,
        name,
        bucket,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        super(MockBlob, self).__init__(
            name=name,
            bucket=bucket,
            chunk_size=chunk_size,
            encryption_key=encryption_key,
            kms_key_name=kms_key_name,
            generation=generation,
        )
        # TODO: Implement storage.acl
        self._acl = None
        self._backend = backend.backend

    def generate_signed_url(
        self,
        expiration=None,
        api_access_endpoint=_API_ACCESS_ENDPOINT,
        method="GET",
        content_md5=None,
        content_type=None,
        response_disposition=None,
        response_type=None,
        generation=None,
        headers=None,
        query_parameters=None,
        client=None,
        credentials=None,
        version=None,
    ):
        return NotImplementedError

    def exists(self, client=None):
        if self.name in self._backend.blobs.values():
            return True
        else:
            return False

    def delete(self, client=None):
        # TODO: Implement Bukcet.delete_blob
        return NotImplementedError

    def _get_transport(self, client):
        return NotImplementedError

    def _do_download(
        self, transport, file_obj, download_url, headers, start=None, end=None
    ):
        return NotImplementedError

    def download_to_file(self, file_obj, client=None, start=None, end=None):
        return NotImplementedError

    def download_to_filename(self, filename, client=None, start=None, end=None):
        return NotImplementedError

    def download_as_string(self, client=None, start=None, end=None):
        return NotImplementedError

    def _do_multipart_upload(
        self, client, stream, content_type, size, num_retries, predefined_acl
    ):
        return NotImplementedError

    def _initiate_resumable_upload(
        self,
        client,
        stream,
        content_type,
        size,
        num_retries,
        predefined_acl=None,
        extra_headers=None,
        chunk_size=None,
    ):
        return NotImplementedError

    def _do_upload(
        self, client, stream, content_type, size, num_retries, predefined_acl
    ):
        return NotImplementedError

    def upload_from_file(
        self,
        file_obj,
        rewind=False,
        size=None,
        content_type=None,
        num_retries=None,
        client=None,
        predefined_acl=None,
    ):
        return NotImplementedError

    def upload_from_filename(
        self, filename, content_type=None, client=None, predefined_acl=None
    ):
        return NotImplementedError

    def upload_from_string(
        self, data, content_type="text/plain", client=None, predefined_acl=None
    ):
        return NotImplementedError

    def create_resumable_upload_session(
        self, content_type=None, size=None, origin=None, client=None
    ):
        return NotImplementedError

    def update_storage_class(self, new_class, client=None):
        # Storage class must be stored as part of the MockBucket object
        return NotImplementedError

    @property
    def component_count(self):
        return NotImplementedError

