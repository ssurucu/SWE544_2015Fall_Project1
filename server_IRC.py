import socket

s = socket.socket()
host = socket.gethostname()
port = 55778
s.bind((host, port))

s.listen(5)
while True:
   c, addr = s.accept()
   print 'Got connection from', addr
   c.send('Now you are connected!Go on and socialize with your friends')
   c.close()