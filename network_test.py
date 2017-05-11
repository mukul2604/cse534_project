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

flag = False

if (len(sys.argv)>1):
    flag = True

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
        if flag:
            print ""
        if (row['rtype']=='AZURE'):
            try:
                if (flag):
                    print "Bucket Name: ", str(row['bucketname'])

                block_blob_service = None
                block_blob_service = BlockBlobService(account_name=row['accesskey'], account_key=row['secretkey'])

                start_time = time.time()
                block_blob_service.create_blob_from_path(
                row['bucketname'],
                outfile,
                filename
                )
                end_time = time.time()
                result.append (end_time - start_time)
                if (flag):
                    print "Response Time: " + str(result[index])
                index = index +1
            except Exception as e:
                print str(e)
                result.append(sys.maxsize)
                index = index +1
                print "Error Connecting to", row['rtype'], " bucket: ", row['bucketname']

        elif (row['rtype']=='AWS'):
            try:
                if (flag):
                    print "Bucket Name: ", str(row['bucketname'])
                
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
                k.set_contents_from_filename(filename)
                end_time = time.time()

                result.append (end_time - start_time)
                if (flag):
                    print "Response Time: " + str(result[index])
                index = index +1
            except:
                result.append(sys.maxsize)
                index = index +1
                print "Error Connecting to", row['rtype'], " bucket: ", row['bucketname']

#    min_value=min(result)
#    min_index=result.index(min_value)
#    print min_index

    net_profiles = [i[0] for i in sorted(enumerate(result), key=lambda x:x[1])]
    print "Profile Indices: ", str(net_profiles)
    return net_profiles

def main():
    getNetworkProfile()
    return 0

if __name__ == "__main__":
    main()
    sys.exit(0)
