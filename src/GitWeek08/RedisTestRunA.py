'''
File: RedisTestRunA.py
Author: Melissa Rice
Last Revision: 7 March 2011
Purpose: First crude hack at writing some stuff to a redis data store.
'''

from RedisStuff import *

if usingRedis:
    rServer = redis.Redis("localhost")
else:
    rServer = "dummy"
    
person1Data = {
    'salutation':'Dr.',
    'first.name':'Avram',
    'middle.names':'Noam',
    'last.name':'Chomsky',
    'nick.name':'Noam',
    'birthday':'1928-12-07',
    #'addresses':'set',
    #'phones':'set',
    }

person2Data = {
    'salutation':'Ms.',
    'first.name':'Arundhati',
    'last.name':'Roy',
    'birthday':'1961-11-24',
    #'addresses':'set',
    #'phones':'set',
    }

person3Data = {
    'salutation':'Dr.',
    'first.name':'Albert',
    'last.name':'Einstein',
    'birthday':'1879-03-14',
    #'addresses':'set',
    #'phones':'set',
    }

people = []

person1 = Person(rServer,person1Data)
people.append(person1)

person2 = Person(rServer,person2Data)
people.append(person2)

person3 = Person(rServer,person3Data)
people.append(person3)

for person in people:
    print "Storing person: %s" % person.fullName()
    person.show()
    person.store()

'''
# check TypeError for invalid keys
print "Testing error trapping for invalid field:"
try:
    person3 = Person(rServer,person3Data)
except Exception, err:
    print err
'''


