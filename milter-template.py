## To roll your own milter, create a class that extends Milter.
#  See the pymilter project at http://bmsi.com/python/milter.html
#  based on Sendmail's milter API
#  This code is open-source on the same terms as Python.

## Milter calls methods of your class at milter events.
## Return REJECT,TEMPFAIL,ACCEPT to short circuit processing for a message.
## You can also add/del recipients, replacebody, add/del headers, etc.

import Milter
from io import StringIO, BytesIO
import time
import email
import sys
from socket import AF_INET, AF_INET6
from Milter.utils import parse_addr
from multiprocessing import Process as Thread, Queue

#from guppy import hpy
#hp = hpy()



logq = Queue(maxsize=4)

class myMilter(Milter.Base):

  def __init__(self):  # A new instance with each new connection.
    self.id = Milter.uniqueID()  # Integer incremented with each call.

  # each connection runs in its own thread and has its own myMilter
  # instance.  Python code must be thread safe.  This is trivial if only stuff
  # in myMilter instances is referenced.
  @Milter.noreply
  def connect(self, IPname, family, hostaddr):
    # (self, 'ip068.subnet71.example.com', AF_INET, ('215.183.71.68', 4720) )
    # (self, 'ip6.mxout.example.com', AF_INET6,
    #	('3ffe:80e8:d8::1', 4720, 1, 0) )
    self.IP = hostaddr[0]
    self.port = hostaddr[1]
    if family == AF_INET6:
      self.flow = hostaddr[2]
      self.scope = hostaddr[3]
    else:
      self.flow = None
      self.scope = None
    self.IPname = IPname  # Name from a reverse IP lookup
    self.H = None
    self.fp = None
    self.receiver = self.getsymval('j')
    self.log("connect from %s at %s" % (IPname, hostaddr) )

    return Milter.CONTINUE


  ##  def hello(self,hostname):
  def hello(self, heloname):
    # (self, 'mailout17.dallas.texas.example.com')
    #self.H = heloname
    self.log("HELO %s" % heloname)
    #if heloname.find('.') < 0:	# illegal helo name
    #  # NOTE: example only - too many real braindead clients to reject on this
    #  self.setreply('550','5.7.1','Sheesh people!  Use a proper helo name!')
    #  return Milter.REJECT

    return Milter.CONTINUE

  ##  def envfrom(self,f,*str):
  def envfrom(self, mailfrom, *str):
    self.F = mailfrom
    self.R = []  # list of recipients
    self.fromparms = Milter.dictfromlist(str)	# ESMTP parms
    self.user = self.getsymval('{auth_authen}')	# authenticated user
    self.log("mail from:", mailfrom, *str)
    # NOTE: self.fp is only an *internal* copy of message data.  You
    # must use addheader, chgheader, replacebody to change the message
    # on the MTA.
    self.fp = BytesIO()
    self.canon_from = '@'.join(parse_addr(mailfrom))
    #self.fp.write('From %s %s\n' % (self.canon_from,time.ctime()))
    return Milter.CONTINUE


  ##  def envrcpt(self, to, *str):
  @Milter.noreply
  def envrcpt(self, to, *str):
    rcptinfo = to,Milter.dictfromlist(str)
    self.R.append(rcptinfo)

    return Milter.CONTINUE


  @Milter.noreply
  def header(self, name, hval):
    self.fp.write((name + ": " + hval + "\n").encode()) # add header to buffer
    return Milter.CONTINUE

  @Milter.noreply
  def eoh(self):
    self.fp.write(b"\n")				# terminate headers
    return Milter.CONTINUE

  @Milter.noreply
  def body(self, chunk):
    #self.before = hp.heap()
    self.fp.write(chunk)
    return Milter.CONTINUE

  def eom(self):
    self.fp.seek(0)
    if self.fp:
      self.fp.close()
      del self.fp
      self.fp = None
    #msg = email.message_from_file(self.fp)
    # many milter functions can only be called from eom()
    # example of adding a Bcc:
    #self.addrcpt('<%s>' % 'spy@example.com')
    return Milter.ACCEPT

  def close(self):
    # always called, even when abort is called.  Clean up
    # any external resources here.
    #print(self.before)
    #if self.fp:
      #self.fp.close()
      #del self.fp
      #self.fp = None

    return Milter.CONTINUE

  def abort(self):
    # client disconnected prematurely
    #del self.fp
    return Milter.CONTINUE

  ## === Support Functions ===

  def log(self,*msg):
    logq.put((msg,self.id,time.time()))

def background():
  while True:
    t = logq.get()
    if not t: break
    msg,id,ts = t
    print("%s [%d]" % (time.strftime('%Y%b%d %H:%M:%S',time.localtime(ts)),id),
        end=None)
    # 2005Oct13 02:34:11 [1] msg1 msg2 msg3 ...
    for i in msg: print(i,end=None)
    print()
    sys.stdout.flush()

## ===

def main():
  bt = Thread(target=background)
  bt.start()
  #socketname = "/home/stuart/pythonsock"
  socketname = 'inet:8801@0.0.0.0'
  timeout = 600
  # Register to have the Milter factory create instances of your class:
  Milter.factory = myMilter
  flags = Milter.CHGBODY + Milter.CHGHDRS + Milter.ADDHDRS
  flags += Milter.ADDRCPT
  flags += Milter.DELRCPT
  Milter.set_flags(flags)       # tell Sendmail which features we use
  #Milter.setdbg(3)
  Milter.settimeout(10)
  Milter.set_exception_policy(0)
  print("%s milter startup" % time.strftime('%Y%b%d %H:%M:%S'))
  sys.stdout.flush()
  Milter.runmilter("pythonfilter",socketname,timeout)
  logq.put(None)
  bt.join()
  print("%s bms milter shutdown" % time.strftime('%Y%b%d %H:%M:%S'))

if __name__ == "__main__":
  main()
