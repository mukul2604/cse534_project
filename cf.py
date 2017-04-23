#!/usr/bin/python
import sys
import getopt
from ops import getsProfileKeys
from aws_ops import aws_operations
from azure_ops import azure_operations

profile_keys = getsProfileKeys()


def printsHelp():
    print("Usage: python cf.py <command> <parameters>")
    print("Examples:")
    print("\tpython cf.py --add <filename>")
    print("\tpython cf.py --add <filename> --imp")
    print("\tpython cf.py --rem <filename>")
    print("\tpython cf.py --list")
    print("\tpython cf.py --list --segragate")
    print("\tpython cf.py --show-added")
    return 0

def main(argv):
    global profile_keys
    filename = ''
    command = 0
    segragate = False
    important = False

    try:
        opts, args = getopt.getopt(argv,"a:r:lsgi",["add=","remove=","list","show-added","segragate","imp"])
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
            command = 2
        elif opt in ("-s", "--show-added"):
            command = 3
        elif opt in ("-g", "--segragate"):
            segragate = True
        elif opt in ("-i", "--imp"):
            important = True
        else:
            printsHelp()
            sys.exit(0)

    if ((command == 0) or (command == 1)) and filename == '':
        print("Filename required with add or remove")
        sys.exit(0)

    #<<<<<<<<
    print command
    print filename
    print segragate
    print important



    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        printsHelp()
    else:
        main(sys.argv[1:])
    sys.exit(0)
