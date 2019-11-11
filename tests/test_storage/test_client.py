from mockgcp.storage.backend import mock_storage
from mockgcp.storage.client import MockClient
from mockgcp.storage.bucket import MockBucket

from google.cloud import storage
from google.api_core import page_iterator
from google.cloud.exceptions import NotFound, Conflict

import pytest
import sys


class TestBucketConstructor:
    @mock_storage
    def test_with_valid_name(self):
        client = storage.Client()
        assert isinstance(client, MockClient)

        bucket = client.bucket("test-bucket-name")

        assert isinstance(bucket, MockBucket)
        assert bucket.name == "test-bucket-name"

    @mock_storage
    def test_with_invalid_name(self):
        with pytest.raises(ValueError):
            client = storage.Client()
            bucket = client.bucket("test-bucket-name-")


class TestGetBucket:
    @mock_storage
    def test_with_existing_bucket_name(self):
        client = storage.Client()
        bucket = client.create_bucket("test-bucket-name")

        assert client.get_bucket("test-bucket-name") is bucket

    @mock_storage
    def test_with_non_existing_bucket_name(self):
        with pytest.raises(NotFound):
            client = storage.Client()
            client.get_bucket("test-bucket-name")


class TestLookupBucket:
    @mock_storage
    def test_wiht_existing_bucket_name(self):
        client = storage.Client()
        bucket = client.create_bucket("test-bucket-name")

        assert client.lookup_bucket("test-bucket-name") is bucket

    @mock_storage
    def test_wiht_non_existing_bucket_name(self):
        client = storage.Client()

        assert client.lookup_bucket("test-bucket-name") == None


class TestCreateBucket:
    @mock_storage
    def test_simple(self):
        client = storage.Client()
        bucket = client.create_bucket("test-bucket-name")

        assert isinstance(bucket, MockBucket)
        assert list(client.list_buckets()) == [bucket]

    @mock_storage
    def test_with_existing_bucket_name(self):
        with pytest.raises(Conflict):
            client = storage.Client()
            bucket = client.create_bucket("test-bucket-name")

            client.create_bucket("test-bucket-name")


class TestListBlobs:
    def test_simple(self):
        # TODO: Write tests when Blob methods are implemented
        pass


class TestListBuckets:
    @mock_storage
    def test_with_no_bucket(self):
        client = storage.Client()
        buckets = client.list_buckets()

        assert isinstance(buckets, page_iterator.HTTPIterator)
        assert list(buckets) == []

    @mock_storage
    def test_with_one_bucket(self):
        client = storage.Client()
        bucket = client.create_bucket("test-bucket-name")
        buckets = client.list_buckets()

        assert list(buckets) == [bucket]

    @mock_storage
    def test_with_max_results(self):
        client = storage.Client()
        client.create_bucket("test-bucket-name-n1")
        client.create_bucket("test-bucket-name-n2")

        assert len(list(client.list_buckets(max_results=1))) == 1

    @mock_storage
    def test_with_prefix(self):
        client = storage.Client()
        bucket_test = client.create_bucket("test-bucket-name")
        client.create_bucket("other-bucket-name")

        assert list(client.list_buckets(prefix="test")) == [bucket_test]
