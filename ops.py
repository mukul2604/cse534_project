import os
import sys
import csv
from os.path import expanduser

# Outline for defining operations on cloud obj stores
class operations(object):
    'Base class of operations to be inherited by AWS_operations and Azure_operations'
    cloudprofile = None
    cloudprovider = None
    path = None

    def __init__(self, profile, provider, fn):
        self.cloudprofile = profile
        self.cloudprovider = provider
        self.path = fn

    def setProvider(self, provider):
        self.cloudprovider = provider
        return 0

    def setProfile(self, profile):
        self.cloudprofile = profile
        return 0

    def setPath(self, fn):
        self.path = fn
        return 0

    def getProvider(self):
        return self.cloudprovider

    def getProfile(self):
        return self.cloudprofile

    def getPath(self):
        return self.path

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def checkExists(self):
        pass


## Parse the CSV with cloud keys into an array of dicts
def getsProfileKeys():
    profile_keys = []
    path = expanduser('~')
    path += '/.cloudifier/keys.csv'
    fil = None
    try:
        fil = open(path)
    except:
        print(sys.exc_info())
        print("Failed to fetch cloud accessing keys!")
        sys.exit(0)

    properties = ['rtype',
                  'accesskey',
                  'secretkey',
                  'bucketname']

    filreader = csv.DictReader(fil)
    for row in filreader:
        prec = {'rtype': '', 'access': '', 'secret': '', 'bucket': ''}
        for vname in properties:
            if row[vname]:
                prec[vname] = row[vname]
            else:
                print("Warning: Missing " + vname + " in record.")
        profile_keys.append(prec)

    fil.close()
    return profile_keys


## Gets keyname from path
# TODO Full path should be keyname. Minus the slash '/'
# Because we are dumping in same bucket. Cloud services dont warn.
# They overwrite.
def getsKeyNameFromPath(fn):
    fn = fn.strip()
    words = fn.split('/')
    return words[-1]

## Gets dir from path
def getsDirFromPath(fn):
    fn = fn.strip()
    words = fn.split('/')
    words = words[:-1]
    pth = '/'
    for k in words:
        if (k is not None) and (k != ''):
            pth += k
            pth += '/'
    return pth

# User can send relative or absolute path
# Convert all to absolute
def getsPathFromUsergarbage(fn):
    if (fn is None) or (fn == ''):
        return ''
    fn = fn.strip()
    if fn[0] == '/':
        return fn
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return dir_path + '/' + fn
