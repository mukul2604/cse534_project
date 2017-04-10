import getopt as g, sys

def main():
    try:
        opts, args = g.getopt(sys.argv[1:], "ho:i", ["help", "output="])
    except g.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print some error like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    insensitive = False
    for o, a in opts:
        if o == "-i":
            insensitive = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
            print output
        else:
            print "unhandled option"
    # ...

def usage():
    print "Usage:"
    print "-i for insensitive files"

def c_connect():
    print getopt.getopt(['-i', '-aws', '-azure'], 'ab:c:')

if __name__ == "__main__":
    main()



