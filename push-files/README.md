File Pusher
======================

Purpose:
======================
This script will log into the systems in the endpoints.txt file and copy logs from /var/log/httpd to a remote data store via a queue and workers.

Usage:
======================
Modify the endpoints.txt to include a list of boxes that you want to push files from.
Update the username you would like to use to sync files with.
For testing create a ssh key and add the pub key to your authorized_keys.
You should accept the server key into your known_hosts first.
endpoints.txt should be formed at host,username

Example:
======================
python file-pusher.py endpoints.txt

Bugs:
======================
It looks like it iterates over the list of servers twice.
I should probably move some of the variables into argsv to make it more flexible.

I don't know how to use join properly so the script will not exit after all the work has been done.
