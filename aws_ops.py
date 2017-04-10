from ops import operations
import boto

class aws_operations(operations):
    'Defines ops for AWS'

    def __init__(self, cfile, fn):
        operations.__init__(self, cfile, "AWS", fn)

    def get(self):
        print("AWS get")

    def put(self):
        print("AWS put")

    def delete(self):
        print("AWS delete")

    def checkExists(self):
        print("AWS check exists")

