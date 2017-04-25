import sys
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
next_id = 0
profile_keys = []
#profile_record = {type = '', id = '', access = '', secret = ''}

def getsProfileKeys():
    global next_id
    path = expanduser('~')
    path += '/.cloudifier/keys'
    print path
    fil = None
    try:
        fil = open(path)
    except:
        print(sys.exc_info())
        print("Failed to fetch cloud accessing keys!")
        sys.exit(0)

    #profile_record = {rtype = '', rid = '', access = '', secret = ''}
    mrtype = None
    maccess = None
    msecret = None

    # This code really depends on the correctness of cloudifier/keys file
    for line in fil:
        if 'type' in line:
            # This is an AWS record
            if 'AWS' in line:
                mrtype = 'AWS'
            elif 'Azure' in line:
                mrtype = 'Azure'
        elif 'access' in line:
            maccess = line.split()[1].strip()
        elif 'secret' in line:
            msecret = line.split()[1].strip()
        elif 'end' in line:
            profile_record = {'rtype': mrtype, 'rid': next_id, 'access': maccess, 'secret': msecret}
            profile_keys.append(profile_record)
            next_id += 1
        else:
            continue
    return

