#!/usr/bin/python
import os
import sys
import Queue
import paramiko
import datetime
import multiprocessing 

DATASTOREHOST = "localhost"
#The user we are using to log into the remote systems.
SYNCUSER = "jw"
#Number of threads to use.
MAXTHREADS = 5

queue = Queue.Queue()

class Server:
  """Server Class for executing a task"""

  def __init__(self, endPointString):
    splitString = endPointString.split(',')
    self.host = splitString[0]
    self.user = splitString[1]

  def run(self):
    """ Uses Paramiko to log into a remote system and iniate a SCP transfer of
        apache logs to a remote machine.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      ssh.connect(self.host, username=self.user)
      stdin, stdout, stderr = ssh.exec_command("scp /var/log/httpd/access_log \
        "+ SYNCUSER +"@"+ DATASTOREHOST +":~/logs/`hostname`/ \
        access-`date +%Y-%m-%d`.log")
      print '%s - Data Push completed for: %s via %s' % ( datetime.datetime.now(),
        self.host, os.getpid())
    except:
      print '%s - Error: %s - for: %s' % ( datetime.datetime.now(),
        sys.exc_info()[0], self.host)

def loadFile():
  if not sys.argv and not sys.argv[1]:
    print "Please specify an input file like endpoints.txt"
    sys.exit()
  else:
    try:
      file = sys.argv[1]
    except IndexError:
      print "Please specify a file that contains the server information"
      sys.exit()
    try:
      endpointList = open(file, 'rb')
      for line in endpointList:
        if line.count(',') != 1:
          print "Line %d is malformed: should be Host,User" % (endpointList.tell())
        else:
          queue.put(line.rstrip('\n'))
    except IOError:
      print "The file specified does not exist!"

def runJob():
    server = Server(queue.get())
    server.run()

def main():
    loadFile()
    for i in range(MAXTHREADS):
      p = multiprocessing.Process(target=runJob)
      p.start()
      p.join()


if __name__ == "__main__":
  main()
