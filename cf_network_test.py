import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.s3.connection import Location


import time
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import csv

filename='1Mb.txt'

f1 = open('/home/salman/cse534_project/keys/azure_accesskey.csv', 'r')
a_key_array = csv.DictReader(f1, delimiter=',')

rows = list(a_key_array)

result=[]
index=0
for row in rows:
    if (row['account_type']=='AZURE'):
        print row['container_name']
        block_blob_service = BlockBlobService(account_name=row['account_name'], account_key=row['access_key'])

        start_time = time.time()
        block_blob_service.create_blob_from_path(
        row['container_name'],
        filename,
        filename
        )
        end_time = time.time()
        result.append (end_time - start_time)
        print result[index]
        index = index +1

    elif (row['account_type']=='AWS'):
        print row['container_name']    
        c = S3Connection(row['access_key'], row['security_key'])
        b = c.get_bucket(row['container_name']) # substitute your bucket name here
        bucket_location = b.get_location()
        #print bucket_location
        if bucket_location:
            conn = boto.s3.connect_to_region(bucket_location,  aws_access_key_id=row['access_key'], aws_secret_access_key=row['security_key'])
            b = conn.get_bucket(row['container_name'])

        k = Key(b)
        k.key = filename
        start_time = time.time()
        k.set_contents_from_filename(filename)
        end_time = time.time()

        result.append (end_time - start_time)
        print result[index]
        index = index +1

max_value=max(result)
max_index=result.index(max_value)
print max_index
