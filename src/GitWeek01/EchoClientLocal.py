'''
EchoClientLocal.py
last revised: 14 January 2011
purpose: basic client socket demo running on local server and sending data 
         to a server socket and printing what is sent and what is received. 
         See EchoServerLocal.py for more extensive documentation.
'''

import socket 

# host = 'block115379-pwc.blueboxgrid.com'
host = '127.0.0.1' 
port = 5050
size = 4096
data = "whatever"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
s.send(data) 
print "Client socket sent this data to server socket: " + data
data = s.recv(size)
print "Client socket received this data from server socket: \n" + data
s.close() 
