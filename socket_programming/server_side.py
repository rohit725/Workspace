import socket

s = socket.socket()
print 'Socket successfully created.'

port = 12345

s.bind(('', port))
print 'Socket binded to %s' % (port)
s.listen(5)
print 'Socket is listening...'

while True:
	c, addr = s.accept()
	print 'got connection from ', addr
	c.send('Thank you for connecting')
	c.close()
