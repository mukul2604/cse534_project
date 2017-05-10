CLIs
====

CLI to add, remove files from our system
----------------------------------------
The idea is to not give control to the user which cloud his data is going to.
That detail is useless for the user particularly if we are claiming to manage
data storage based on network conditions.

cf add <filename>
cf remove <filename>
cf add -i <filename>
cf add --imp <filename>


CLI Show namespace
------------------
List that flat file


CLI to view current namespace - Basically ls like command
---------------------------------------------------------
The command will be implemented such that it will go to the cloud
and list the buckets intensionally. Do not display from a local copy.

This should show the entire namespace
cf ls
Remove dups


This should list the entire namespace segragated by which cloud profile has what
This will be useful for the demo
cf ls -s
cf ls --seg
Show all files in all clouds


Network
=======
IP addrs - Endpoint
Ping time -------- inconsistent
Upload download -----
Client server model for CLI
Server contacts cloud only when CLI reqs
Server periodically updates from list of files



TODO
====

Must
----
CLI runs then exits
Who will our CLI ask the network stats from:
        A running process - Who starts it? What happens if it crashed?
        Read from a file that a background process keeps updating - Synchronization


Fetch file from cloud
Fetch imp from nearest cloud


Nice to have
------------
Automatic background running server which updates files on the cloud or resurects them
