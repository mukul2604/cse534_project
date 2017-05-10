#!/usr/bin/python
import ops
import sys
import getopt
import socket

SERVERHOST = '127.0.0.1'
SERVERPORT = 7070

def printsHelp():
    print("Usage: python cf.py <command> <parameters>")
    print("Examples:")
    print("\tpython cf.py --add <filename>")
    print("\tpython cf.py --add <filename> --imp")
    print("\tpython cf.py --rem <filename>")
    print("\tpython cf.py --download <filename>")
    print("\tpython cf.py --list")
    print("\tpython cf.py --list --segragate")
    print("\tpython cf.py --show-added")
    return 0

def main(argv):
    filename = ''
    command = 0
    segragate = False
    important = False

    try:
        opts, args = getopt.getopt(argv,"a:r:d:lsgi",["add=","remove=","download=","list","show-added","segragate","imp"])
    except getopt.GetoptError:
        printsHelp()
        sys.exit(-1)
    for opt, arg in opts:
        if opt in ("-a", "--add"):
            filename = arg
            command = 0
        elif opt in ("-r", "--remove"):
            filename = arg
            command = 1
        elif opt in ("-l", "--list"):
            important = True
            command = 2
        elif opt in ("-s", "--show-added"):
            command = 3
        elif opt in ("-d", "--download"):
            filename = arg
            command = 4
        elif opt in ("-g", "--segragate"):
            segragate = True
        elif opt in ("-i", "--imp"):
            important = True
        else:
            printsHelp()
            sys.exit(0)

    if ((command == 0) or (command == 1) or (command == 4)) and filename == '':
        print("Filename required with add, remove and download")
        sys.exit(0)

    # Commands
    # 0: add | 1: remove | 2: list |
    # 3: show-added | 4: download

    # COMMAND | FILENAME | SEGRAGATE | IMPORTANT
    command_str = ''
    command_str += str(command)
    command_str += '|'
    if command != 2: # Send null filename in list
        command_str += str(filename)
    command_str += '|'
    if segragate:
        command_str += '1'
    else:
        command_str += '0'
    command_str += '|'
    if important:
        command_str += '1'
    else:
        command_str += '0'

    received = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVERHOST, SERVERPORT))
        sock.sendall(command_str)
        received = sock.recv(1024)
    except Exception as e:
        print ("ERROR: Failed to connect to " + SERVERHOST + ". Reason: " + str(e))
    finally:
        sock.close()

    if received == 'OK':
        pass
    else:
        print(received)
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        printsHelp()
    else:
        main(sys.argv[1:])
    sys.exit(0)
