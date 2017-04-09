import os, sys
import cloudify
from cloudify import services, access_key, secure_key

def c_connect():
    global access_key, secure_key
    for i in range(0,len(services)):
        f1 = open(access_key[i], 'r')
        a_key = f1.read()
        f2 = open(secure_key[i], 'r')
        s_key = f2.read()
        f1.close()
        f2.close()

        if (services[i] == 'AZURE'):
            connect_azure(a_key, s_key)
        elif (services[i] == 'AWS'):
            connect_aws(a_key, s_key)

def connect_azure(access_key, secure_key):
    print "Connecting AZURE services:"
    print access_key
    print secure_key

def connect_aws(access_key, secure_key):
    print "Connecting AWS services"
    print access_key
    print secure_key


def main():
    c_connect()

if __name__=="__main__":
   main()
