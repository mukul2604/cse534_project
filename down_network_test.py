import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.s3.connection import Location


import time
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import csv

import os
import sys

def getNetworkProfile():
    filename='1Mb.txt'
    key_path = os.path.expanduser('~/.cloudifier/keys.csv')

    f1 = open(key_path, 'r')
    a_key_array = csv.DictReader(f1, delimiter=',')

    rows = list(a_key_array)

    result=[]
    index=0
    for row in rows:
        outfile = str(row['rtype']) + "_10MB_" + str(row['bucketname'])
#        print outfile
        if (row['rtype']=='AZURE'):
            print row['bucketname']
            try:
                block_blob_service = None
                block_blob_service = BlockBlobService(account_name=row['accesskey'], account_key=row['secretkey'])

                start_time = time.time()
                block_blob_service.get_blob_to_path(
                row['bucketname'],
                outfile,
                outfile
                )
                end_time = time.time()
                result.append (end_time - start_time)
                print result[index]
                index = index +1
            except:
                result.append(sys.maxsize)
                index = index +1
                print "Error Connecting to", row['rtype'], " bucket: ", row['bucketname']

        elif (row['rtype']=='AWS'):
            print row['bucketname']   
            try:
                c = S3Connection(row['accesskey'], row['secretkey'])
                b = c.get_bucket(row['bucketname']) # substitute your bucket name here
        
                bucket_location = b.get_location()
                #print bucket_location
                if bucket_location:
                    conn = boto.s3.connect_to_region(bucket_location,  aws_access_key_id=row['accesskey'], aws_secret_access_key=row['secretkey'])
                    b = conn.get_bucket(row['bucketname'])

                k = Key(b)
                k.key = outfile
                start_time = time.time()
                k.get_contents_to_filename(outfile)
                end_time = time.time()

                result.append (end_time - start_time)
                print result[index]
                index = index +1
            except:
                result.append(sys.maxsize)
                index = index +1
                print "Error Connecting to", row['rtype'], " bucket: ", row['bucketname']

#    min_value=min(result)
#    min_index=result.index(min_value)
#    print min_index

    net_profiles = [i[0] for i in sorted(enumerate(result), key=lambda x:x[1])]
    print net_profiles
    return net_profiles

def main():
    getNetworkProfile()
    return 0

if __name__ == "__main__":
    main()
    sys.exit(0)
