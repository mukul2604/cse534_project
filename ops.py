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

