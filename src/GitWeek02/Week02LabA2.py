'''
Week02LabA2.py
last revised: 21 January 2011
author: Melissa Rice (UWNetID: mlrice)
purpose: quick test of urllib2 library
         assignment: write a program which reads a text file
         with a single URL on each line and attempts to save
         each to a file. 
'''

import urllib2

inputFilename = 'C:/A/eclipse/projects/InternetProgrammingLabs/src/Week02/urls.txt'
outputFilenameBase = 'C:/A/eclipse/projects/InternetProgrammingLabs/src/Week02/url'

urlsFile = open(inputFilename)
urls = urlsFile.readlines()
j = 0
print
for url in urls:
    j += 1
    urlObject = urllib2.urlopen(url)
    metadata = urlObject.info()
    urlAddress = urlObject.geturl()
    content = urlObject.readlines()
    content = ''.join(content)
    outFilename = outputFilenameBase + str(j) + ".html"
    print "Saving contents of %s" % urlAddress
    print "To file: %s " % outFilename 
    print "Sanitized url: %s " % urllib2.quote(urlAddress)
    print "Metadata for this file is: %s \n\n" % metadata
    outFile = open(outFilename,'w')
    outFile.write(content)
    outFile.close()


''' Output of this code is:

Saving contents of http://briandorsey.info/uwpython/week01/email_vm.py
To file: C:/A/eclipse/projects/InternetProgrammingLabs/src/Week02/url1.html 
Sanitized url: http%3A//briandorsey.info/uwpython/week01/email_vm.py 
Metadata for this file is: Server: nginx
Date: Sat, 22 Jan 2011 06:38:45 GMT
Content-Type: application/octet-stream
Content-Length: 891
Last-Modified: Wed, 12 Jan 2011 18:28:19 GMT
Connection: close
Accept-Ranges: bytes
 


Saving contents of http://www.melissarice.info/index.html
To file: C:/A/eclipse/projects/InternetProgrammingLabs/src/Week02/url2.html 
Sanitized url: http%3A//www.melissarice.info/index.html 
Metadata for this file is: Server: Sun-ONE-Web-Server/6.1
Date: Sat, 22 Jan 2011 06:06:48 GMT
Content-type: text/html;charset=ISO-8859-1
Connection: close
 


'''
