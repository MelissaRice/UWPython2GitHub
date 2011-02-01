import time
import datetime

print """<html>
<head><title>Current Time</title></head>
<body>
<p>
<font size="5">"""

print "Here is the time: %s" % time.time()
print "and again: %s" % datetime.datetime.now()

print """</font>
</p>
</body>
</html>
"""
