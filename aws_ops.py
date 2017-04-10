import boto
import ops
class aws_operations(ops.operations):
    'Defines ops for AWS'

    def __init__(self, cfile, fn):
        ops.operations(cfile, "AWS", fn)

    def put(self):
        print("Hello A")

