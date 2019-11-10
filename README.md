# mock-gcp | Mock GCP Services

![Python Version](https://img.shields.io/badge/python-3.7-blue)
![Supported GCS Version](https://img.shields.io/badge/gcs-v1.22.0-brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A library that allows to mock out GCP services in unit tests.

## Intro

## List of supported services

| Service Name  | Decorator     | Development status          |
| ------------- | ------------- | --------------------------- |
| Cloud Storage | @mock_storage | basic endpoints implemented |

## Usage

Let's say you have the following function to test.

```python
from google.cloud import storage

def create_bucket_if_doesnt_exist(bucket_name):
    client = storage.Client()

    if client.lookup_bucket(bucket_name) is None:
        return client.create_bucket(bucket_name)
    else:
        return None
```

To test this function with `mock-gcp` use the `@mock_storage` decorator which will mock out all API calls in the background.

```python
from google.cloud import storage
from mockgcp.storage.backend import mock_storage

@mock_storage
def test_create_bucket_if_doesnt_exist_when_bucket_exists():
    client = storage.Client()
    # Firts, need to create a bucket in our virtual Google Cloud project
    client.create_bucket("test-bucket")

    assert create_bucket_if_doesnt_exists("test-bucket") is None
```

## Install

```bash
pip install mock-gcp
```

_Not yet working..._
