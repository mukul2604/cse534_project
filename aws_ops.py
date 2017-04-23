import boto
from boto.s3.connection import S3Connection
from ops import operations, getsKeyNameFromPath

class aws_operations(operations):
    'Defines ops for AWS'

    conn_obj = None
    bucket_obj = None

    def __init__(self, profile, fn):
        # profile: Index of profile_keys array. Basically the index
        #          with which we can search all other details
        # fn     : Full file path followed by path name
        operations.__init__(self, profile, "AWS", fn)
        conn_obj = S3Connection(GKEYS[profile]['accesskey'], GKEYS[profile]['secretkey'])
        bucket_obj = conn_obj.create_bucket(GKEYS[profile]['bucketname'])

    def get(self):
        print("AWS get")

        if fn is None:
            # We are trying to list everything - eg. for ls command
            print bucket_obj.list()
        else:
            keyname = getsKeyNameFromPath(fn)


    def put(self):
        print("AWS put")

    def delete(self):
        print("AWS delete")

    def checkExists(self):
        print("AWS check exists")

