'''
Week2LabA1.py
last revised: 21 January 2011
author: Melissa Rice (UWNetID: mlrice)
purpose: quick test of urllib2 library
         assignment: use urllib2 to download and save a url: 
         http://briandorsey.info/uwpython/week01/email_vm.py
'''

import urllib2

urlString = 'http://briandorsey.info/uwpython/week01/email_vm.py'
outputFilename = 'C:/A/eclipse/projects/InternetProgrammingLabs/src/Week02/Week02LabA1-Output.txt'

url = urllib2.urlopen(urlString)
metadata = url.info()
urlAddress = url.geturl()
content = url.readlines()
output = "The url object: %s " % url
output += "\n===> url address (url.geturl()): %s " % urlAddress 
output += "\n===> url metadata (url.info()): %s " % metadata
output += "\n===> url content: "
output += ''.join(content)
print output
outFile = open(outputFilename,'w')
outFile.write(output)
outFile.close()

''' Output of this code is:
The url object: <addinfourl at 44204200 whose fp = <socket._fileobject object at 0x0292B5F0>> 
===> url address (url.geturl()): http://briandorsey.info/uwpython/week01/email_vm.py 
===> url metadata (url.info()): Server: nginx
Date: Sat, 22 Jan 2011 06:21:36 GMT
Content-Type: application/octet-stream
Content-Length: 891
Last-Modified: Wed, 12 Jan 2011 18:28:19 GMT
Connection: close
Accept-Ranges: bytes
 
===> url content: import smtplib
from pprint import pprint

def send_email(from_addr, to_addrs, subject, message, debug = False):

    template = """From: %s
To: %s
Subject: %s

"""
    headers = template % (from_addr, to_addrs, subject)

    if debug:
        print '#### debugging on'
        print headers + message
        print
        pprint(locals())
        print '#### '
    s = smtplib.SMTP('mail.blueboxgrid.com')
    if debug:
        s.set_debuglevel(1)
    s.ehlo()
    if debug:
        print '#### sendmail()'
    s.sendmail(from_addr, to_addrs, headers + message)
    s.close()

if __name__ == '__main__':
    failed_addrs = send_email( 'Darth Vader <darth@deathstar.com>',
                         'briandorsey@gmail.com',
                         "I'm your father.",
                         'message body',
                         True)
    print failed_addrs

                         


'''







