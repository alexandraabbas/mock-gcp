import uuid


class StorageBackend:
    def __init__(self, project=None):
        if project is None:
            project = "test-project-" + str(uuid.uuid1())
        self.project = project
        self.buckets = {}
        self.blobs = {}


backend = StorageBackend()
