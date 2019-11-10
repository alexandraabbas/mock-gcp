from mockgcp.storage.backend import mock_storage
from mockgcp.storage.client import Client
from mockgcp.storage.bucket import Bucket

from google.cloud import storage
from google.cloud.exceptions import NotFound

import pytest
import sys


@mock_storage
def test_bucket_constructor():
    client = storage.Client()
    assert isinstance(client, Client)

    bucket = client.bucket("test-bucket-name-v1")

    assert isinstance(bucket, Bucket)
    assert bucket.name == "test-bucket-name-v1"


@mock_storage
def test_bucket_constructor_with_invalid_name():
    with pytest.raises(ValueError):
        client = storage.Client()
        bucket = client.bucket("test-bucket-name-")


@mock_storage
def test_get_bucket_with_existing_bucket_name():
    client = storage.Client()
    bucket = client.create_bucket("test-bucket-name-v2")

    assert client.get_bucket("test-bucket-name-v2") is bucket


@mock_storage
def test_get_bucket_with_non_existing_bucket_name():
    with pytest.raises(NotFound):
        client = storage.Client()
        buckets = list(client.list_buckets())
        print([bucket.name for bucket in buckets])
        client.get_bucket("test-bucket-name-v2")
