'''
AdditionClient.py
last revised: 17 January 2011
author: Melissa Rice (UWNetID: mlrice)
purpose: client-side socket demo which poses an addition problem to the 
         companion server-side socket, which performs the addition and 
         returns the answer. The addition problem should be posed as an
         infix string expression containing only addition operators, 
         numbers, and unary minus for negative numbers. By default, both 
         client and server run on localhost but this can be changed by 
         changing the serverHost variable.
'''

import socket 

# remote server host is 'block115379-pwc.blueboxgrid.com'

# serverHost: the IP or fully-qualified domain name where the addition server is running
serverHost = 'localhost'
# serverPort: the port on which the addition server is listening 
serverPort = 50050
# the maximum string length which can be sent to the addition server
bufferSize = 4096
# the addition problem to send to the addition server (as an infix string or 'quit' to
# shut down the addition server)
additionString = "4 + 3 + -5" # should equal 2
# creation of the server socket as a stream (TCP) socket over IPv4
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# connect to the addition server
serverSocket.connect((serverHost,serverPort))
# send the addition problem if not too large
if len(additionString) < bufferSize: 
    serverSocket.send(additionString)
    sum = serverSocket.recv(bufferSize)
    print "Server performed this sum: " + additionString + " = " + sum
else:
    print "The addition string is too long. Please use at most 4096 characters."
serverSocket.close() 

