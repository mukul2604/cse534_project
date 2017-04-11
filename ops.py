import sys
import csv
from os.path import expanduser

# Outline for defining operations on cloud obj stores
class operations(object):
    'Base class of operations to be inherited by AWS_operations and Azure_operations'
    cloudprofile = None
    cloudprovider = None
    filename = None

    def __init__(self, profile, provider, fn):
        self.cloudprofile = profile
        self.cloudprovider = provider
        self.filename = fn

    def setProvider(self, vider):
        self.cloudprovider = vider
        return 0

    def setProfile(self, profile):
        self.cloudprofile = profile
        return 0

    def setFilename(self, fn):
        self.filename = fn
        return 0

    def getProvider(self):
        return self.cloudprovider

    def getProfile(self):
        return self.cloudprofile

    def getFilename(self):
        return self.filename

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def checkExists(self):
        pass


## Cloud profiles key handling

def getsProfileKeys():
    profile_keys = []
    path = expanduser('~')
    path += '/.cloudifier/keys'
    fil = None
    try:
        fil = open(path)
    except:
        print(sys.exc_info())
        print("Failed to fetch cloud accessing keys!")
        sys.exit(0)

    properties = ['rid',
                  'rtype',
                  'accesskey',
                  'secretkey',
                  'bucketname']

    filreader = csv.DictReader(fil)
    for row in filreader:
        prec = {'rid': '', 'rtype': '', 'access': '', 'secret': '', 'bucket': ''}
        for vname in properties:
            if row[vname]:
                prec[vname] = row[vname]
            else:
                print("Warning: Missing " + vname + " in record.")
        profile_keys.append(prec)

    fil.close()
    return profile_keys

