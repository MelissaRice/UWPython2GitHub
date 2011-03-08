'''
File: RedisStuff.py
Author: Melissa Rice
Last Revision: 7 March 2011
Purpose: First crude hack at classes to support interaction with Redis.
'''

usingRedis = True

if usingRedis:
    import redis

        
class RedisObject(object):
    Counters = {}
    DataStore = {}
    '''
    RedisObject is an abstract base class providing a foundation for objects which will
    interact with a redis datastore.
    '''
    def __init__(self,redisServer):
        '''
        Constructor
        '''
        if usingRedis:
            self.redisServer = redisServer
    def sanitizeValue(self,value):
        # write something here...
        return value
    def getID(self,type):
        type = type.replace(" ","") # sanitize better...
        idKey = ".".join(['next',type,'id'])
        if usingRedis:
            id = self.redisServer.incr(idKey)
        else:
            if RedisObject.Counters.has_key(type):
                RedisObject.Counters[type] += 1
            else:  
                RedisObject.Counters[type] = 1
            id = RedisObject.Counters[type]
        return id
    def storeString(self,key,value):
        # sanitize key or value here??
        if usingRedis:
            self.redisServer.set(key,value)
        else:
            RedisObject.DataStore[key] = value
    def storeAny(self, key, type, value):
            if type == 'string':
                self.storeString(key,value)
            elif type == '??':
                pass
            else:
                pass
    def getAny(self, type, id, fieldKey):
        key = ":".join([type,str(id),fieldKey])
        if usingRedis:
            value = self.redisServer.get(key)
        else:
            value = RedisObject.DataStore.get(key,None)
            print "looking for key %s and found: %s" % (key, value)
        return value

class Person(RedisObject):
    name = 'person'
    validKeys = {'salutation':'string',
                 'first.name':'string',
                 'nick.name':'string',
                 'middle.names':'string',
                 'last.name':'string',
                 'suffix':'string',
                 'birthday':'string',
                 'addresses':'set',
                 'phones':'set',
                 }
    def __init__(self, redisServer, dataDict=None):
        self.data = {}
        self.redisServer = redisServer
        if dataDict == None:
            dataDict = {}
        for key, value in dataDict.items():
            if self.isValidKey(key):
                self.data[key] = self.sanitizeValue(value)
            else:
                errorMessage = "The Person object has no key called %s\n" % str(key)
                errorMessage += "while instantiating from this data dictionary: %s\n" % repr(dataDict)
                raise KeyError, errorMessage
    def isValidKey(self,key):
        if key in Person.validKeys.keys():
            return True
        else:
            return False
    def store(self):
        id = self.getID('person')
        baseKey = ":".join(['person',str(id)])
        for fieldKey, value in self.data.items():
            type = Person.validKeys[fieldKey]
            key = ":".join([baseKey,fieldKey])
            self.storeAny(key, type, value)
    def retrieve(self,id):
        found = False
        for fieldKey in Person.validKeys:
            if Person.validKeys[fieldKey] == 'string':
                value = self.getAny('person',str(id),fieldKey)
                self.data[fieldKey] = value
                print "    found: %s = %s" % (fieldKey,value)
                found = True
        return found
    def fullName(self):
        name = self.data.get('first.name',"")
        name += " " + self.data.get('last.name',"")
        return name
    def show(self):
        print "Data for person...."
        for fieldKey, keyType in Person.validKeys.items():
            if keyType == 'string':
                value = self.data.get(fieldKey,"not set")
                print "%s = %s" % (fieldKey, value)
        print "=================================="
'''
Redis Command Line Examples
$ ./redis-cli set mykey "my binary safe value"
OK
$ ./redis-cli get mykey
my binary safe value
$ ./redis-cli set counter 100
OK
$ ./redis-cli incr counter
(integer) 101
$ ./redis-cli incr counter
(integer) 102
$ ./redis-cli incrby counter 10
(integer) 112
$ ./redis-cli rpush messages "Hello how are you?"
OK
$ ./redis-cli rpush messages "Fine thanks. I'm having fun with Redis"
OK
$ ./redis-cli rpush messages "I should look into this NOSQL thing ASAP"
OK
$ ./redis-cli lrange messages 0 2
1. Hello how are you?
2. Fine thanks. I'm having fun with Redis
3. I should look into this NOSQL thing ASAP
$ ./redis-cli incr next.news.id
(integer) 1
$ ./redis-cli set news:1:title "Redis is simple"
OK
$ ./redis-cli set news:1:url "http://code.google.com/p/redis"
OK
$ ./redis-cli lpush submitted.news 1
OK
$ ./redis-cli sadd myset 1
(integer) 1
$ ./redis-cli sadd myset 2
(integer) 1
$ ./redis-cli sadd myset 3
(integer) 1
$ ./redis-cli smembers myset
1. 3
2. 1
3. 2
$ ./redis-cli sismember myset 3
(integer) 1
$ ./redis-cli sismember myset 30
(integer) 0
$ ./redis-cli sadd news:1000:tags 1
(integer) 1
$ ./redis-cli sadd news:1000:tags 2
(integer) 1
$ ./redis-cli sadd news:1000:tags 5
(integer) 1
$ ./redis-cli sadd news:1000:tags 77
(integer) 1
$ ./redis-cli sadd tag:1:objects 1000
(integer) 1
$ ./redis-cli sadd tag:2:objects 1000
(integer) 1
$ ./redis-cli sadd tag:5:objects 1000
(integer) 1
$ ./redis-cli sadd tag:77:objects 1000
(integer) 1
$ ./redis-cli smembers news:1000:tags
1. 5
2. 1
3. 77
4. 2
$ ./redis-cli sinter tag:1:objects tag:2:objects tag:10:objects tag:27:objects
... no result in our dataset composed of just one object ;) ...
$ ./redis-cli zadd hackers 1940 "Alan Kay"
(integer) 1
$ ./redis-cli zadd hackers 1953 "Richard Stallman"
(integer) 1
$ ./redis-cli zadd hackers 1965 "Yukihiro Matsumoto"
(integer) 1
$ ./redis-cli zadd hackers 1916 "Claude Shannon"
(integer) 1
$ ./redis-cli zadd hackers 1969 "Linus Torvalds"
(integer) 1
$ ./redis-cli zadd hackers 1912 "Alan Turing"
(integer) 1
$ ./redis-cli zrange hackers 0 -1
1. Alan Turing
2. Claude Shannon
3. Alan Kay
4. Richard Stallman
5. Yukihiro Matsumoto
6. Linus Torvalds
$ ./redis-cli zrevrange hackers 0 -1
1. Linus Torvalds
2. Yukihiro Matsumoto
3. Richard Stallman
4. Alan Kay
5. Claude Shannon
6. Alan Turing
$ ./redis-cli zrangebyscore hackers -inf 1950
1. Alan Turing
2. Claude Shannon
3. Alan Kay
$ ./redis-cli zremrangebyscore hackers 1940 1960
(integer) 2



'''


'''
Redis-Py examples
3
>>> r_server.set("name", "DeGizmo")
4
True
5
>>> r_server.get("name")
6
'DeGizmo'
>>> r_server.set("hit_counter", 1)
02
True
03
>>> r_server.incr("hit_counter")
04
2
05
>>> r_server.get("hit_counter")
06
'2'>>> r_server.rpush("members", "Adam")
True
>>> r_server.rpush("members", "Bob")
True
>>> r_server.rpush("members", "Carol")
True
>>> r_server.lrange("members", 0, -1)
['Adam', 'Bob', 'Carol']
>>> r_server.llen("members")
3
>>> r_server.lindex("members", 1)
'Bob'
07
>>> r_server.decr("hit_counter")
08
1
09
>>> r_server.get("hit_counter")
10
'1'
>>> r_server.rpop("members")
'Carol'
>>> r_server.lrange("members", 0, -1)
['Adam', 'Bob']
>>> r_server.lpop("members")
'Adam'
>>> r_server.lrange("members", 0, -1)
['Bob']
>>> r_server.delete("members")
True
>>> r_server.sadd("members", "Adam")
True
>>> r_server.sadd("members", "Bob")
True
>>> r_server.sadd("members", "Carol")
True
>>> r_server.sadd("members", "Adam")
False
>>> r_server.smembers("members")
set(['Bob', 'Adam', 'Carol'])
>>> r_server.sadd("story:5419:upvotes", "userid:9102")
True
>>> r_server.sadd("story:5419:upvotes", "userid:12981")
True
>>> r_server.sadd("story:5419:upvotes", "userid:1233")
True
>>> r_server.sadd("story:5419:upvotes", "userid:9102")
False
>>> r_server.scard("story:5419:upvotes")
3
>>> r_server.smembers("story:5419:upvotes")
set(['userid:12981', 'userid:1233', 'userid:9102'])
>>> r_server.zadd("stories:frontpage", "storyid:3123", 34)
True
>>> r_server.zadd("stories:frontpage", "storyid:9001", 3)
True
>>> r_server.zadd("stories:frontpage", "storyid:2134", 127)
True
>>> r_server.zadd("stories:frontpage", "storyid:2134", 127)
False
>>> r_server.zrange("stories:frontpage", 0, -1, withscores=True)
[('storyid:9001', 3.0), ('storyid:3123', 34.0), ('storyid:2134', 127.0)]
>>> frontpage = r_server.zrange("stories:frontpage", 0, -1, withscores=True)
>>> frontpage.reverse()
>>> frontpage
[('storyid:2134', 127.0), ('storyid:3123', 34.0), ('storyid:9001', 3.0)]
#given variables
#r_server   = our redis server
#user_id    = the user who voted on the story
#story_id   = the story which the user voted on
if r_server.sadd("story:%s" % story_id, "userid:%s" % user_id):
    r_server.zincrby("stories:frontpage", "storyid:%s" % story_id, 1)
if r_server.sadd("story:%s" % story_id, "userid:%s" % user_id):
"userid:%s" % user_id
r_server.zincrby("stories:frontpage", "storyid:%s" % story_id, 1)











'''
