from google.api_core import page_iterator
from google.cloud.exceptions import NotFound, Conflict

from mockgcp.storage.bucket import Bucket
from mockgcp.backend import backend

from unittest import mock


class Client:
    def __init__(
        self,
        project=None,
        credentials=None,
        _http=None,
        client_info=None,
        client_options=None,
    ):
        self.backend = backend
        if self.backend.project is None:
            project = "<none>"
        else:
            project = self.backend.project

        self.project = project
        self.credentials = credentials
        self._http = _http
        self.client_info = client_info
        self.client_options = client_options

    @classmethod
    def create_anonymous_client(cls):
        raise NotImplementedError

    @property
    def _connection(self):
        raise NotImplementedError

    @_connection.setter
    def _connection(self, value):
        raise NotImplementedError

    def _push_batch(self, batch):
        raise NotImplementedError

    def _pop_batch(self):
        raise NotImplementedError

    def _bucket_arg_to_bucket(self, bucket_or_name):
        """Helper to return given bucket or create new by name.

        Args:
            bucket_or_name (Union[ \
                :class:`~mockgcp.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

        Returns:
            mockgcp.storage.bucket.Bucket
                The newly created bucket or the given one.
        """
        if isinstance(bucket_or_name, Bucket):
            bucket = bucket_or_name
        else:
            bucket = Bucket(self, name=bucket_or_name)
        return bucket

    @property
    def current_batch(self):
        raise NotImplementedError

    def get_service_account_email(self, project=None):
        raise NotImplementedError

    def bucket(self, bucket_name, user_project=None):
        """Factory constructor for bucket object.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to be instantiated.

        :type user_project: str
        :param user_project: (Optional) the project ID to be billed for API
                             requests made via the bucket.

        :rtype: :class:`mockgcp.storage.bucket.Bucket`
        :returns: The bucket object created.
        """
        return Bucket(client=self, name=bucket_name, user_project=user_project)

    def batch(self):
        raise NotImplementedError

    def get_bucket(self, bucket_or_name):
        """Retreive a bucket from StorageBackend.

        Args:
            bucket_or_name (Union[ \
                :class:`~mockgcp.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

        Returns:
            mockgcp.storage.bucket.Bucket
                The bucket matching the name provided.

        Raises:
            google.cloud.exceptions.NotFound
                If the bucket is not found.
        """
        bucket = self._bucket_arg_to_bucket(bucket_or_name)

        # TODO: Use bucket.reload(client=self) when Bucket class is implemented
        if bucket.name in self.backend.buckets.keys():
            return self.backend.buckets[bucket.name]
        else:
            raise NotFound(
                "404 GET https://storage.googleapis.com/storage/v1/b/{}?projection=noAcl".format(
                    bucket.name
                )
            )

    def lookup_bucket(self, bucket_name):
        """Get a bucket by name, returning None if not found.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to get.

        :rtype: :class:`mockgcp.storage.bucket.Bucket`
        :returns: The bucket matching the name provided or None if not found.
        """
        try:
            return self.get_bucket(bucket_name)
        except NotFound:
            return None

    def create_bucket(self, bucket_or_name, requester_pays=None, project=None):
        """Creates a bucket in StorageBackend

        Args:
            bucket_or_name (Union[ \
                :class:`~mockgcp.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.
            requester_pays (bool):
                Optional. Whether requester pays for API requests for this
                bucket and its blobs.
            project (str):
                Optional. the project under which the bucket is to be created.
                If not passed, uses the project set on the client.

        Returns:
            mockgcp.storage.bucket.Bucket
                The newly created bucket.

        Raises:
            google.cloud.exceptions.Conflict
                If the bucket already exists.
        """
        bucket = self._bucket_arg_to_bucket(bucket_or_name)
        # bucket.create(client=self, project=project)
        if bucket.name in self.backend.buckets.keys():
            raise Conflict
        else:
            self.backend.buckets[bucket.name] = bucket
        return bucket

    def download_blob_to_file(self, blob_or_uri, file_obj, start=None, end=None):
        """Download the contents of a blob object or blob URI into a file-like object.

        Args:
            blob_or_uri (Union[ \
            :class:`~google.cloud.storage.blob.Blob`, \
             str, \
            ]):
                The blob resource to pass or URI to download.
            file_obj (file):
                A file handle to which to write the blob's data.
            start (int):
                Optional. The first byte in a range to be downloaded.
            end (int):
                Optional. The last byte in a range to be downloaded.
        """
        raise NotImplementedError

    def list_blobs(
        self,
        bucket_or_name,
        max_results=None,
        page_token=None,
        prefix=None,
        delimiter=None,
        versions=None,
        projection="noAcl",
        fields=None,
    ):
        """Return an iterator used to find blobs in the bucket.

        If :attr:`user_project` is set, bills the API request to that project.

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

            max_results (int):
                (Optional) The maximum number of blobs in each page of results
                from this request. Non-positive values are ignored. Defaults to
                a sensible value set by the API.

            page_token (str):
                (Optional) If present, return the next batch of blobs, using the
                value, which must correspond to the ``nextPageToken`` value
                returned in the previous response.  Deprecated: use the ``pages``
                property of the returned iterator instead of manually passing the
                token.

            prefix (str):
                (Optional) prefix used to filter blobs.

            delimiter (str):
                (Optional) Delimiter, used with ``prefix`` to
                emulate hierarchy.

            versions (bool):
                (Optional) Whether object versions should be returned
                as separate blobs.

            projection (str):
                (Optional) If used, must be 'full' or 'noAcl'.
                Defaults to ``'noAcl'``. Specifies the set of
                properties to return.

            fields (str):
                (Optional) Selector specifying which fields to include
                in a partial response. Must be a list of fields. For
                example to get a partial response with just the next
                page token and the name and language of each blob returned:
                ``'items(name,contentLanguage),nextPageToken'``.
                See: https://cloud.google.com/storage/docs/json_api/v1/parameters#fields

        Returns:
            Iterator of all :class:`~google.cloud.storage.blob.Blob`
            in this bucket matching the arguments.
        """
        raise NotImplementedError

    def list_buckets(
        self,
        max_results=None,
        page_token=None,
        prefix=None,
        projection="noAcl",
        fields=None,
        project=None,
    ):
        """Get all buckets from StorageBackend associated with the client.

        :type max_results: int
        :param max_results: Optional. The maximum number of buckets to return.

        :type page_token: str
        :param page_token:
            Optional. If present, return the next batch of buckets, using the
            value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing the
            token.

        :type prefix: str
        :param prefix: Optional. Filter results to buckets whose names begin
                       with this prefix.

        :type projection: str
        :param projection:
            (Optional) Specifies the set of properties to return. If used, must
            be 'full' or 'noAcl'. Defaults to 'noAcl'.

        :type fields: str
        :param fields:
            (Optional) Selector specifying which fields to include in a partial
            response. Must be a list of fields. For example to get a partial
            response with just the next page token and the language of each
            bucket returned: 'items/id,nextPageToken'

        :type project: str
        :param project: (Optional) the project whose buckets are to be listed.
                        If not passed, uses the project set on the client.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :raises ValueError: if both ``project`` is ``None`` and the client's
                            project is also ``None``.
        :returns: Iterator of all :class:`~google.cloud.storage.bucket.Bucket`
                  belonging to this project.
        """
        if project is None:
            project = self.project

        if project is None:
            raise ValueError("Client project not set:  pass an explicit project.")

        if isinstance(max_results, int):
            buckets = list(self.backend.buckets.values())[:max_results]
        else:
            buckets = list(self.backend.buckets.values())

        if isinstance(prefix, str):
            buckets = [bucket for bucket in buckets if bucket.name.startswith(prefix)]

        path = "/foo"
        page_response = {"items": buckets}
        api_request = mock.Mock(return_value=page_response)
        extra_params = {"key": "val"}

        return page_iterator.HTTPIterator(
            mock.sentinel.client,
            api_request,
            path=path,
            item_to_value=page_iterator._item_to_value_identity,
            max_results=max_results,
            page_token=mock.sentinel.token,
            extra_params=extra_params,
        )

    def create_hmac_key(
        self, service_account_email, project_id=None, user_project=None
    ):
        raise NotImplementedError

    def list_hmac_keys(
        self,
        max_results=None,
        service_account_email=None,
        show_deleted_keys=None,
        project_id=None,
        user_project=None,
    ):
        raise NotImplementedError

    def get_hmac_key_metadata(self, access_id, project_id=None, user_project=None):
        raise NotImplementedError


def _item_to_bucket(iterator, item):
    raise NotImplementedError


def _item_to_hmac_key_metadata(iterator, item):
    raise NotImplementedError
