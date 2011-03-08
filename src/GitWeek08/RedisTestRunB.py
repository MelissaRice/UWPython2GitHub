'''
File: RedisStuff.py
Author: Melissa Rice
Last Revision: 7 March 2011
Purpose: First crude hack at reading some stuff from a redis data store.
'''

from RedisStuff import *

if usingRedis:
    rServer = redis.Redis("localhost")
else:
    rServer = "dummy"
    
people = []

if usingRedis:
    nPeople = int(rServer.get('next.person.id')) + 1
else:
    nPeople = 2
    
print "There is data stored for %s people in the redis data store. Retrieving that now...." 
    
for pID in range(1,nPeople):
    person = Person(rServer)
    found = person.retrieve(pID)
    if found:
        print "Person with id %s is %s" % (pID,person.fullName()) 
        person.show()
    
