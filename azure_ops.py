from ops import operations
from ops import getsKeyNameFromPath
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess


class azure_operations(operations):
    """Defines ops for Azure"""
    block_blob_service = None
    bucket_name = None

    def __init__(self, profiles, index, path):
        operations.__init__(self, profiles, "Azure", path)

        account_name = profiles[index]['accesskey']
        access_key = profiles[index]['secretkey']
        self.block_blob_service = BlockBlobService(account_name=account_name, account_key=access_key)
        self.bucket_name = profiles[index]['bucketname']

        try:
            self.block_blob_service.create_container(self.bucket_name, public_access=PublicAccess.Container)
        except Exception:
            pass

    def get(self):
        ret = ''
        if (self.path is None) or (self.path == ''):
            generator = self.block_blob_service.list_blobs(self.bucket_name)
            for blob in generator:
                ret += blob.name + "\n"
        else:
            path = getsKeyNameFromPath(self.path)
            self.block_blob_service.get_blob_to_path(self.bucket_name,
                                                           path,
                                                           path)
            ret += 'Download Done'

        return ret

    def put(self):
        path = getsKeyNameFromPath(self.path)
        self.block_blob_service.create_blob_from_path(
            self.bucket_name,  # container  should user provide the name
            path,  # to be uploaded object
            path,   # real file path
        )
        return "Put Done"

    def delete(self):
        path = getsKeyNameFromPath(self.path)
        self.block_blob_service.delete_block(self.bucket_name, path)
        return "Delete Done"

    def create(self):
        # create container
        return "Done"

    def checkExists(self):
        print("Azure check exists")
        return "Done"
