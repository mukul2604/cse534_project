import boto
from boto.s3.connection import S3Connection
from ops import operations, getsKeyNameFromPath

class aws_operations(operations):
    'Defines ops for AWS'

    conn_obj = None
    bucket_obj = None

    def __init__(self, profiles, index, path):
        # profiles: reference to the array with cloud keys
        # index   : Index of the profile we want to use
        # path    : Full file path followed by path name
        operations.__init__(self, profiles, "AWS", path)
        conn_obj = S3Connection(profiles[index]['accesskey'], profiles[index]['secretkey'])
        bucket_obj = conn_obj.create_bucket(profiles[index]['bucketname'])

    def get(self):
        print("AWS get")

        if path is None:
            # We are trying to list everything - eg. for ls command
            print bucket_obj.list()
        else:
            keyname = getsKeyNameFromPath(path)


    def put(self):
        print("AWS put")

    def delete(self):
        print("AWS delete")

    def checkExists(self):
        print("AWS check exists")

