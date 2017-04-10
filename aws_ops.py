import boto
from ops import operations

class aws_operations(operations):
    'Defines ops for AWS'

    def __init__(self, profile, fn):
        operations.__init__(self, profile, "AWS", fn)

    def get(self):
        print("AWS get")

    def put(self):
        print("AWS put")

    def delete(self):
        print("AWS delete")

    def checkExists(self):
        print("AWS check exists")

