'''
File: Week02LabB.py
last revised: 21 January 2011
original author: Wilhelm Fitzpatrick (rafial@well.com) 30 minute webserver August 3rd, 2002
author of modifications: Melissa Rice (UWNetID: mlrice)
purpose: Exploration of a very basic webserver; assignment was to add code which serves
         the current time as an html page in response to a request for the /time url.
'''

# Original Header
# ws30 -- the thirty minute web server
# author: Wilhelm Fitzpatrick (rafial@well.com)
# date: August 3rd, 2002
# version: 1.0
#
# Written after attending a Dave Thomas talk at PNSS and hearing about
# his "write a web server in Ruby in one hour" challenge.
#
# Actual time spent:
#  30 minutes reading socket man page
#  30 minutes coding to first page fetched
#   3 hours making it prettier & more pythonic
#
# updated for UW Internet Programming in Python, by Brian Dorsey
#

import os, socket, sys, datetime

diagnostics = True
defaults = ['127.0.0.1', '8080']
mime_types = {'.jpg' : 'image/jpg', 
             '.gif' : 'image/gif', 
             '.png' : 'image/png',
             '.html' : 'text/html', 
             '.pdf' : 'application/pdf'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""

DIRECTORY_LINE = '<a href="%s">%s</a><br>'


TIME_DISPLAY =\
"""<html>
<head><title>Current Time</title></head>
<body>
<p>
<font size="8">It is currently %s.\n
Thanks for checking the time server.</font>
</p>
</body>
</html>
"""

def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method = None
    while True:
        line = stream.readline()
        #print line
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
    return uri

def list_directory(uri):
    entries = os.listdir('.' + uri)
    entries.sort()
    if diagnostics:
        print "preparing a directory list for directory %s with entries..." % uri
        print repr(entries)
    string = DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))
    return string

def get_file(path):
    f = open(path)
    try: 
        return f.read()
    finally: 
        f.close()

def get_content(uri):
    print 'fetching:', uri
    try:
        path = '.' + uri
        if diagnostics:
            print "Path is " + path
        if path == "./time":
            dt = datetime.datetime.now()
            timeDate = dt.strftime("%I:%M%p on %A %d %B %Y ")
            currentTime = TIME_DISPLAY % timeDate
            if diagnostics:
                print "Received time request."
                print "   Reporting current time as: %s" % currentTime
            return(200, 'text/html', currentTime)
        elif os.path.isfile(path):
            if diagnostics:
                print "Processing a file."
            return (200, get_mime(uri), get_file(path))
        elif os.path.isdir(path):
            if diagnostics:
                print "Processing a directory."
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri))
            else:
                if diagnostics:
                    print "Processing a redirect."
                return (301, uri + '/')
        else: return (404, uri)
    except IOError, e:
        return (404, e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    print "web server starting on host %s on port %s" % (host,port)
    if diagnostics:
        print "%s args: %s" % (nargs,repr(args))
    server = server_socket(host, int(port))
    try:
        while True:
            stream = listen (server)
            request = get_request(stream)
            if diagnostics:
                print "handling this request: %s " % request
            content = get_content(request)
            if diagnostics:
                print "preparing this content: %s " % repr(content)
            send_response(stream, content)
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

