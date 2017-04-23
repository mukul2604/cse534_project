import sys
import ops
import thread
import SocketServer
from aws_ops import aws_operations
from azure_ops import azure_operations


#****************#
# TUNABLE PARAMS #
#****************#
SERVERPORT = 7070  # Default port on which the server listens
MAX_THREADS = 100



#****************#
# DO NOT FIDDLE  #
#****************#

profile_keys = ops.getsProfileKeys()
#threadreturns = [] # threads can update their own index element for ret status
next_tid = 0
#for i in range(MAX_THREADS):    # Ask mukul
#    threadreturns.append(0)


def getsNetworkProfile():
    # I check the network stats and return the index of the
    # profile_keys array that you should use as your cloud provider
    # Right now I am not implemented so I return 0
    # TODO
    return 0



# Add remove the full path of the file from ~/.cloudifier/path_db file
def db_file_add(path):
    # TODO
    print 'Add: ' + str(path)
    return 0


# Add remove the full path of the file from ~/.cloudifier/path_db file
def db_file_remove(path):
    # TODO
    print 'Remove: ' + str(path)
    return 0


# The code that runs as a separate thread
# We want to handle the case where an upload of 500 MB file can
# continue in background while CLI and the server are free to
# accept more requests
def handle_request(tname, tnum, command, path, seg, imp):
    global profile_keys

    # User might give relative or abs path
    # Convert everything to absolute
    properpath = ops.getsPathFromUsergarbage(path)

    obj = None
    pf = None
    idx = 0
    loop = 0
    if (imp == 1):
        loop = len(profile_keys)
        idx = 0
    else:
        loop = 1
        idx = getsNetworkProfile()

    while loop > 0:
        loop -= 1

        # Get the proper cloud's object
        pf = profile_keys[idx]
        if pf['rtype'] == 'AWS':
            # Lets not make AWS or Azure connections here
            # Lets make them in their respective classes
            # as handling here would be messy. Pass the
            # profile_keys itself so that class constr can make connections
            obj = aws_operations(profile_keys, idx, properpath)
        else:
            obj = aws_operations(profile_keys, 0, properpath) #<<<<<< TODO

        # Run the appropriate operation
        if (command == 0):
            db_file_add(properpath)
            obj.put(properpath)
        elif (command == 1):
            db_file_remove(properpath)
            obj.delete(properpath)
        else:
            # TODO more ops
            continue
    return 0

# Can this string be safely converted to int?
def isInteger(n):
    try:
        int(n)
        return True
    except:
        return False

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global next_tid
        resp = 'OK'
        imp = -1
        command = -1
        segragate = -1

        # In linux, the max path length could be 4096 bytes
        self.data = self.request.recv(4200).strip()
        words = self.data.split('|')

        #<<<<<<<<
        print("Command: " + words[0])
        print("Filename: " + words[1])
        print("Segragate: " + words[2])
        print("Important file: " + words[3])
        print(' ')
        #<<<<<<<<

        next_tid += 1
        threadname = 'request_' + str(next_tid)

        if (isInteger(words[0])):
            command = int(words[0])
        if (isInteger(words[2])):
            segragate = int(words[2])
        if (isInteger(words[3])):
            imp = int(words[3])

        try:
            thread.start_new_thread(handle_request,
            (threadname, next_tid % MAX_THREADS, command, words[1], segragate, imp))
        except Exception as e:
            print('ERROR: Could not start server thread. ' + str(e))
            resp = 'Request failed: ' + str(e)
        self.request.sendall(resp)
        return 0


def main():
    # Start the server thread
    print("Starting the server")
    server = SocketServer.TCPServer(('0.0.0.0', SERVERPORT), MyTCPHandler)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    main()
    sys.exit(0)
