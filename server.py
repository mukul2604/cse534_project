import os
import sys
import ops
import time
import thread
import SocketServer
import network_test
from os.path import expanduser
from aws_ops import aws_operations
from azure_ops import AzureOperations

#****************#
# TUNABLE PARAMS #
#****************#
SERVERPORT = 7070  # Default port on which the server listens
MAX_THREADS = 100  # How many parallel requests can be handled
homepath = expanduser('~')
PATHDB = homepath + '/.cloudifier/path_db' # Where is the DB of added files
TWAIT_TIMER = 1 # How long to wait for a thread (sec)

#****************#
# DO NOT FIDDLE  #
#****************#

profile_keys = ops.getsProfileKeys()
threadreturns = [] # threads can update their own index element for ret status
next_tid = 0
for i in range(MAX_THREADS):
    threadreturns.append('OK')


def getsNetworkProfile():
    profile_keys_idx = network_test.getNetworkProfile()
    print (profile_keys_idx)
    return profile_keys_idx[0]


# Add remove the full path of the file from ~/.cloudifier/path_db file
def db_file_add(ppath):
    path = ops.getsKeyNameFromPath(ppath)
    fil = open(PATHDB, 'a')
    fil.write(path)
    fil.write('\n')
    fil.close()
    return 0


# Add remove the full path of the file from ~/.cloudifier/path_db file
def db_file_remove(ppath):
    path = ops.getsKeyNameFromPath(ppath)
    fil = open(PATHDB, 'r+')
    cfil = open(PATHDB + '_1', 'w+')
    for line in fil:
        if path not in line:
            cfil.write(line)
    fil.close()
    cfil.close()
    os.system('rm ' + PATHDB)
    os.system('mv ' + PATHDB + '_1 ' + PATHDB)
    return 0


# The code that runs as a separate thread
# We want to handle the case where an upload of 500 MB file can
# continue in background while CLI and the server are free to
# accept more requests
def handle_request (tname, tnum, command, path, seg, imp):
    global profile_keys
    global threadreturns

    # User might give relative or abs path
    # Convert everything to absolute
    properpath = ops.getsPathFromUsergarbage(path)

    obj = None
    pf = None
    idx = 0
    loop = 0
    tmsg = ''

    # imp = 1 implies that we have to run the op for
    # all the clouds
    if (imp == 1):
        loop = len(profile_keys)
    else:
        loop = 1
        idx = getsNetworkProfile()

    while loop > 0:
        # Get the proper cloud's object
        pf = profile_keys[idx]

        # If segregated listing in requested, do it
        if seg == 1:
            tmsg += pf['rtype'] + ' profile ' + str(idx) + ':\n'

        if pf['rtype'] == 'AWS':
            # Lets not make AWS or Azure connections here
            # Lets make them in their respective classes
            # as handling here would be messy. Pass the
            # profile_keys itself so that class constr can make connections
            obj = aws_operations(profile_keys, idx, properpath)
        else:
            obj = aws_operations(profile_keys, 0, properpath) #<<<<<< TODO

        # Run the appropriate operation
        try:
            ret = ''
            if (command == 0):
                # Add file
                db_file_add(properpath)
                ret = obj.put()
            elif (command == 1):
                # Remove file
                db_file_remove(properpath)
                ret = obj.delete()
            elif (command == 2):
                # List everything
                ret = obj.get()
            elif (command == 3):
                # show added
                fil = open(PATHDB, 'r+')
                for line in fil:
                    line = line.strip()
                    ret += line
                    ret += '\n'
                fil.close()
            elif (command == 4):
                #download
                ret = obj.get()
            else:
                pass
            tmsg += ret + '\n'
        except Exception as e:
            tmsg += str(e) + '\n'

        # If the file is important, we loop
        # over every cloud available to us
        loop -= 1
        if (imp == 1):
            idx += 1

    print ("\nResponse for thread " + str(tnum) + ":\n" + tmsg)
    threadreturns[tnum] = ''
    threadreturns[tnum] = tmsg
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
        global threadreturns
        global next_tid
        resp = 'OK'
        imp = -1
        command = -1
        segragate = -1

        # In linux, the max path length could be 4096 bytes
        self.data = self.request.recv(4200).strip()
        words = self.data.split('|')

        print('================================')
        print("Command: " + words[0])
        print("Filename: " + words[1])
        print("Segragate: " + words[2])
        print("Important file: " + words[3])

        next_tid += 1
        threadname = 'request_' + str(next_tid)

        if (isInteger(words[0])):
            command = int(words[0])
        if (isInteger(words[2])):
            segragate = int(words[2])
        if (isInteger(words[3])):
            imp = int(words[3])

        this_thread_id = next_tid % MAX_THREADS
        try:
            thread.start_new_thread(handle_request,
            (threadname, this_thread_id, command, words[1], segragate, imp))
        except Exception as e:
            print('ERROR: Could not start server thread. ' + str(e))
            resp = 'Request failed: ' + str(e)
        time.sleep(TWAIT_TIMER)
        print('================================\n')
        self.request.sendall(threadreturns[this_thread_id])
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
