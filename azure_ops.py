from ops import operations

class azure_operations(operations):
    'Defines ops for Azure'

    def __init__(self, cfile, fn):
        operations.__init__(self, cfile, "Azure", fn)

    def get(self):
        print("Azure get")

    def put(self):
        print("Azure put")

    def delete(self):
        print("Azure delete")

    def checkExists(self):
        print("Azure check exists")

