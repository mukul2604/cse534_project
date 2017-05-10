import boto
from boto.s3.key import Key
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
        self.conn_obj = S3Connection(profiles[index]['accesskey'], profiles[index]['secretkey'])

        # TODO <<<<<<
        # More sophesticated code. If bucketname is empty then new random name
        # create that bucket and update keys.csv accordingly
        # <<<<<<

        # If this is the first access to this profile then create the bucket
        # else create_bucket will raise exception. Then you get() this bucket.
        try:
            self.bucket_obj = self.conn_obj.create_bucket(profiles[index]['bucketname'])
        except:
            self.bucket_obj = self.conn_obj.get_bucket(profiles[index]['bucketname'])
        return


    def get(self):
        if (self.path is None) or (self.path == ''):
            # We are trying to list everything - eg. for ls command
            print('The following objects are available in the cloud:')
            for item in self.bucket_obj.list():
                sitem = str(item)
                sitem = sitem[1:-1]
                words = sitem.strip().split(',')
                pretty_item = words[1]
                print(pretty_item)
            print(' ')
        else:
            k = Key(self.bucket_obj)
            k.key = getsKeyNameFromPath(self.path)
            k.get_contents_to_filename(getsKeyNameFromPath(self.path))
        return 0

    def put(self):
        keyname = getsKeyNameFromPath(self.path)
        k = Key(self.bucket_obj)
        k.key = keyname
        k.set_contents_from_filename(self.path)
        return 0

    def delete(self):
        keyname = getsKeyNameFromPath(self.path)
        k = Key(self.bucket_obj)
        k.key = keyname
        k.delete()
        return 0


    def checkExists(self):
        print("AWS check exists")

