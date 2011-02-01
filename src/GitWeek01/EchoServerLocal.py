'''
EchoServerLocal.py
last revised: 14 January 2011
purpose: basic server-side socket demonstration to run on localhost and echo 
         back what the client sends, plus some information about the sockets.
         The script is carefully documented to make the syntax and usage clear.
         The companion script EchoClientLocal.py runs the client socket. Run
         this script first before running the client.
'''
import socket, os

# host should be a fully-qualified domain name or an IP address for the server socket; 
# use an IP address for deterministic behavior; otherwise behavior depends on the DNS 
# resolution. These special values of host: '' ==>  INADDR_ANY and 
# '<broadcast>' ==> INADDR_BROADCAST work for IPv4 but not IPv6. Also, some documentation
# I read suggested that usages such as host = '127.0.0.1' or host = 'localhost' would not
# result in the port being visible to an outside machine. Clearly that is not relevant here
# since this is a local demo, but if it were to be a problem the recommended solution is to
# use gethostbyname or gethostbyaddr like this: host = socket.gethostbyname('127.0.0.1'). 
host = '127.0.0.1' # or 'localhost' both work on the local machine (confirmed)

# port is the port on which the server socket will communicate. This script uses a 
# random non-privileged port (>1024) so it doesn't need admin privilege to run. 
port = 5050 

# The domainType should be one of these (where AF stands for address family): 
# * AF_INET  for an IPv4 INET socket
# * AF_INET6 for an IPv6 INET socket
# * AF_UNIX  for a local socket using a file 
# Note: There are also similar PF_* constants, where PF stands for protocol family.
# In some cases these have the same values as the corresponding AF_* constants but
# best to read the man page for socket(2) if more information is required.
domainType = socket.AF_INET

# The socketType should be one of these:
# * SOCK_STREAM: a connection-oriented socket for a TCP stream 
# * SOCK_DGRAM: a connectionless socket for UDP datagram transmission 
# * SOCK_RAW: a raw socket (a low-level socket interface)
# * SOCK_RDM: for reliable datagrams 
# * SOCK_SEQPACKET: sequential transfer of records over a connection 
# Note: stream and datagram socket types are by far the most commonly used.
socketType = socket.SOCK_STREAM

# The format of socketID depends on the domain type. For AF_INET, it is a tuple of 
# host and port. socketID is the argument to the bind method. 
serverSocketID = (host,port)

# backlog is the maximum number of requests that the server will queue before it refuses
# additional requests; 5 is apparently a typical value.
backlog = 5 

# bufferSize is the maximum amount of data the socket will receive at once. A smallish
# power of two is generally a good choice. If the amount of data sent to the server is
# more than this then it must be collected with multiple calls to socket.recv but this
# can be tricky to manage, especially if both server and client are trying to do ad hoc
# buffering because it seems easy to get them deadlocked (especially if setblocking is 
# true). So it seems best to size the buffer adequately for the task or to write a 
# properly buffered set of socket drivers.
bufferSize = 4096

# The socket method creates the socket of the appropriate type but does not bind it
# to an address:port; this is done next by the bind method. The protocol argument is
# left off when it is zero; otherwise it would be the third argument to the socket method.
serverSocket = socket.socket(domainType, socketType)
 
# The bind method accepts a socket ID (format dependent on domain type) and binds the
# socket to that location: (host,port) in this case for an IPv4 domain.
serverSocket.bind(serverSocketID)
 
# The listen method puts the socket into listening mode where it listens for requests, 
# and refuses additional requests if the number queued is already equal to backlog. 
serverSocket.listen(backlog) 

# The following is the request-servicing loop. This one runs as an infinite loop so you
# have to kill the process to close the socket. For convenience, the script prints its
# process id with instructions for killing it.
processID = os.getpid()
print "This process runs a server socket that does not exit until the process is killed."
print "To kill this process on a unix machine, use: kill -9 %s" % processID
print "On Windows, open the task manager and kill process number %s" % processID
while 1: 
    # When the listening socket (serverSocket) receives a request from a client it creates  
    # a new client socket (clientSocket) and returns the client socket object and the   
    # address (clientSocketID) which the client socket is bound to.
    (clientSocket, clientSocketID) = serverSocket.accept()
    # The recv method receives data (up to the limit bufferSize bytes) from the client  
    # socket and echoes back the received data together with some information about the
    # sockets involved.  
    data = clientSocket.recv(bufferSize)
    # If the data is not null, the server confirms the data and socket info to the client.
    if data: 
        reply  = "Thanks for sending this data: %s\n" % data
        reply += "Client socket is at host = %s on port = %s: \n" % clientSocketID
        reply += "Server socket is at host = %s on port = %s: \n" % serverSocketID
        reply += "Server socket has buffer size %s bytes and maximum backlog of %s requests.\n" % (bufferSize,backlog)
        bytes = clientSocket.send(reply)
        # print "%s bytes of data sent to client."  % bytes
    # Once the request is served, the connection to the client is closed by closing the
    # client socket. The serverSocket remains in listening mode until the process is killed.
    clientSocket.close()
