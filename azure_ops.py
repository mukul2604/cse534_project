from ops import operations
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
        content = self.block_blob_service.get_blob_to_path(self.bucket_name,
                                                           self.path + 'blob',
                                                           self.path)
        print("Azure get")
        return content

    def put(self):
        self.block_blob_service.create_blob_from_path(
            self.bucket_name,  # container  should user provide the name
            self.path + 'blob',  # to be uploaded object
            self.path,   # real file path
        )
        print("Azure put")
        return 0

    def delete(self):
        self.block_blob_service.delete_block(self.bucket_name, self.path + 'blob')
        print("Azure delete")
        return 0

    def create(self):
        # create container
        return 0

    def checkExists(self):
        print("Azure check exists")
        return 0
