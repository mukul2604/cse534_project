import boto
import datetime
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import time
from boto.s3.connection import Location
#print '\n'.join(i for i in dir(Location) if i[0].isupper())

f1 = open('/home/salman/Downloads/rootkey.csv', 'r')
a_key_array = f1.read()
a_key = a_key_array.splitlines()
access_key = a_key[0].split("AWSAccessKeyId=")[1]
security_key = a_key[1].split("AWSSecretKey=")[1]

c = S3Connection(access_key, security_key)
#b = c.get_bucket('salman91') # substitute your bucket name here
b = c.get_bucket('testtokyo534') # substitute your bucket name here
bucket_location = b.get_location()
#print bucket_location
if bucket_location:
    conn = boto.s3.connect_to_region(bucket_location,  aws_access_key_id=access_key, aws_secret_access_key=security_key)
    b = conn.get_bucket('testtokyo534')

#c = S3Connection(access_key, security_key)
#c = boto.s3.connect_to_region('APNortheast')
#b = c.get_bucket('testtokyo534') # substitute your bucket name here
k = Key(b)
k.key = '1Mb.txt'
start_time = time.time()
#k.set_contents_from_string('This is a test of S')
k.set_contents_from_filename('1Mb.txt')
end_time = time.time()

print end_time - start_time

