from ops import operations
from azure.storage.blob import BlockBlobService



class AzureOperations(operations):
    """Defines ops for Azure"""
    block_blob_service = None

    def __init__(self):
        operations.__init__(self, profile, "Azure", filename)
        conf_file = open(cfile, "r")
        config = {}

        for line in conf_file:
            k, v = line.strip().split('=')
            config[k.strip()] = v.strip()
        account_name = config['account_name']
        access_key   = config['access_key']
        self.block_blob_service = BlockBlobService(account_name= account_name, account_key= access_key)

    def find_bucket_name(self):
        return bucket_name


    def get(self):
        # find some api or do we need to pass bucket name exclusively as given in the example.
        bucket_name = find_bucket_name()
        content = self.block_blob_service.get_blob_to_path(bucket_name, self.filename + 'blob', self.filename)
        print("Azure get")
        return content

    def put(self):
        bucket_name = find_bucket_name()
        self.block_blob_service.create_blob_from_path(
            bucket_name,  # container  should user provide the name
            self.filename + 'blob',  # to be uploaded object
            self.filename,   # real file path
        )
        print("Azure put")

    def delete(self):
        self.block_blob_service.delete_blob('mycontainer', self.filename + 'blob')
        print("Azure delete")

    def create(self):
        # create container

    def checkExists(self):
        print("Azure check exists")

