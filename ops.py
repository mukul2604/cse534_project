class operations:
    'Base class of operations to be inherited by AWS_operations and Azure_operations'
    cloudprofile = None
    cloudprovider = None
    filename = None

    def __init__(self, cfile, cvider, fn):
        self.cloudprofile = cfile
        self.cloudprovider = cvider
        self.filename = fn

    def setProvider(vider):
        self.cloudprovider = vider
        return 0

    def setProfile(profile):
        self.cloudprofile = profile
        return 0

    def setFilename(fn):
        self.filename = fn
        return 0

    def getProvider():
        return self.cloudprovider

    def getProfile():
        return self.cloudprofile

    def getFilename():
        return self.filename

    def get():
        pass

    def put():
        pass

    def delete():
        pass

    def checkExists():
        pass

