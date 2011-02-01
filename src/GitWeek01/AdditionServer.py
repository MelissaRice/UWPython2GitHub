'''
AdditionServer.py
last revised: 17 January 2011
author: Melissa Rice (UWNetID: mlrice)
purpose: server-side socket demo which accepts an addition problem from the 
         companion client-side socket, performs the addition and returns the 
         answer. The addition problem should be posed as an infix string 
         expression containing only addition operators, numbers, and 
         unary minus for negative numbers. By default, both client and server
         run on localhost but this can be changed by changing the serverHost
         variable. Sending the string 'quit' will shut down the server.
'''

import socket 

# To print diagnostic information as the socket handles requests, set to True:
diagnosticPrinting = True

# The server socket is uniquely identified by:
#   IP address (resolved from hostname by DNS as needed)
#   Port number
#   Protocol (here TCP over IPv4)
serverHost = 'localhost' 
serverPort = 50050 
serverSocketID = (serverHost,serverPort)
domainType = socket.AF_INET       # IPv4
socketType = socket.SOCK_STREAM   # stream-type (TCP) connection-oriented protocol

# The behavior of the server socket is controlled by the following two parameters:
maxBacklog = 5       # maximum number of queued requests before refusing any more
bufferSize = 4096    # maximum bytes received by a single recv command execution

# Server Socket Setup
# create socket for TCP connection over IPv4
serverSocket = socket.socket(domainType, socketType)
# bind server socket to serverSocketID = (serverHost,serverPort)
serverSocket.bind(serverSocketID)
# place server socket in listening mode with at most 5 queued requests allowed at once
serverSocket.listen(maxBacklog) 

# Request Service Loop (can be shut down by client with 'quit')
done = 0
error = ""
while not done: 
    (clientSocket, clientSocketID) = serverSocket.accept()
    infixString = clientSocket.recv(bufferSize)
    operands = infixString.split("+")
    try:
        #operands = map(float, operands.replace(" ",""))
        operands = [float(x.replace(" ","")) for x in operands]
    except:
        error = "Error. Please use only addition operators. For a-b use: a + -b."
    if error != "":
        if infixString.lower() == 'quit':
            reply = "Thank you and goodnight."
            done = True
        else:
            reply = error
    else:
        reply = str(sum(operands))
    replyBytes = clientSocket.send(reply)
    if diagnosticPrinting:
        print "Server socket listening on host %s on port %s." % serverSocketID
        print "Client socket contacted server from host %s on port %s." % clientSocketID
        print "Client sent this addition problem %s to which server replied %s." % (infixString,reply)
        print "Received string was %s bytes long and response was %s bytes long.\n" % (len(infixString),replyBytes)
    clientSocket.close()
serverSocket.close()
if diagnosticPrinting:
    print "Server socket was closed by client."
