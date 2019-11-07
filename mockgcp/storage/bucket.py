from six.moves.urllib.parse import urlsplit

from google.cloud.exceptions import NotFound
from google.cloud.storage._helpers import _validate_name
from google.cloud.storage.acl import BucketACL
from google.cloud.storage.acl import DefaultObjectACL

from google.cloud.storage.constants import COLDLINE_STORAGE_CLASS
from google.cloud.storage.constants import DUAL_REGION_LOCATION_TYPE
from google.cloud.storage.constants import (
    DURABLE_REDUCED_AVAILABILITY_LEGACY_STORAGE_CLASS,
)
from google.cloud.storage.constants import MULTI_REGIONAL_LEGACY_STORAGE_CLASS
from google.cloud.storage.constants import MULTI_REGION_LOCATION_TYPE
from google.cloud.storage.constants import NEARLINE_STORAGE_CLASS
from google.cloud.storage.constants import REGIONAL_LEGACY_STORAGE_CLASS
from google.cloud.storage.constants import REGION_LOCATION_TYPE
from google.cloud.storage.constants import STANDARD_STORAGE_CLASS


class Bucket:
    """A class representing a Bucket on Cloud Storage.

    :type client: :class:`google.cloud.storage.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the bucket (which requires a project).

    :type name: str
    :param name: The name of the bucket. Bucket names must start and end with a
                 number or letter.

    :type user_project: str
    :param user_project: (Optional) the project ID to be billed for API
                         requests made via this instance.
    """

    _MAX_OBJECTS_FOR_ITERATION = 256
    """Maximum number of existing objects allowed in iteration.

    This is used in Bucket.delete() and Bucket.make_public().
    """

    STORAGE_CLASSES = (
        STANDARD_STORAGE_CLASS,
        NEARLINE_STORAGE_CLASS,
        COLDLINE_STORAGE_CLASS,
        MULTI_REGIONAL_LEGACY_STORAGE_CLASS,
        REGIONAL_LEGACY_STORAGE_CLASS,
        DURABLE_REDUCED_AVAILABILITY_LEGACY_STORAGE_CLASS,
    )
    """Allowed values for :attr:`storage_class`.

    Default value is :attr:`STANDARD_STORAGE_CLASS`.
    """

    _LOCATION_TYPES = (
        MULTI_REGION_LOCATION_TYPE,
        REGION_LOCATION_TYPE,
        DUAL_REGION_LOCATION_TYPE,
    )
    """Allowed values for :attr:`location_type`."""

    def __init__(self, client, name=None, user_project=None):
        name = _validate_name(name)
        self.name = name
        self._client = client
        self.blobs = []
        # self._acl = BucketACL(self)
        # self._default_object_acl = DefaultObjectACL(self)
        # self._label_removals = set()
        # self._user_project = user_project

        # Attributes from _PropertyMixin parent class
        # self._properties = {}
        # self._changes = set()

    def create(
        self,
        client=None,
        project=None,
        location=None,
        predefined_acl=None,
        predefined_default_object_acl=None,
    ):
        raise NotImplementedError
