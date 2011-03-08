ReadMe.txt for Week08 mlrice UWPython2010 Assignment
====================================================

1. The first part of the assignment was to port last week's django project to another database. 
   I ported from postgres to MySQL and it was a simple matter of changing the database settings
   in settings.py for the django project and using dumpdata (with the old settings) and loaddata
   with the new settings to transfer the data from the old database to the new one (after creating
   a new database in MySQL). The new settings file is provided here; the old one was provided last 
   week. The webserver is running at the same location as last week.
   
2. The second part of the assignment was to make two scripts which communicate through a redis 
   datastore. I like redis very well, and expect to use it in some projects, so I'm very pleased
   that you suggested it. I've made a very crude start on some data handling classes for redis.
   This is not yet accessible via the web but I have some small test scripts to demonstrate. So
   far only string values are supported but I intend to support the other datatypes in my classes,
   which will evovle as I get a better idea of how best to use Redis and what to use it for....
   
   The three files included for the assignment are:
   RedisStuff.py: class definitions:
       RedisObject will be an abstract base class providing encapsulation of all redis commands
       Person is a class for encapsulating information about people (to be stored under keys of
          the form person:<personID>:<fieldName> such as person.8.last.name or person.8.birthday
   RedisTestRunA.py: demonstrates using the Person class to create some people data and store it
       in the redis datastore.
   RedisTestRunB.py: demonstrates using retrieving data from the redis datastore into Person objects
       and then displaying that data.
       
3. The answers to the questions are:
   Redis currently supports these datatypes:
     string: a binary-safe string
     list: a list of values associated to a key
     set: an unsorted collection of values
     sorted set: a sorted collection of values
     hash: a hash (I haven't played with this one yet)
   JSON data is formatted as a string which uses notation like python nested dictionaries
   Like python, redis has a selection of data types with suitable tools associated to each data type.
   Unlike python:
     - redis supports binary-safe strings for the keys and the values 
     - redis identifies the different datatype solely via the names of methods which access them.
       for instance, rpush accesses lists only, zadd access ordered sets only.
     - redis has a list object which is implemented as a linked list as opposed to the python list 
       which is more of an array structure. The redis list is accessed with stack-type methods like
       lpush, lpop, rpush, rpop (except you have access to both the head and tail, unlike a stack).
     - redis does not seem to nest data structures. The equivalent of nesting seems to accomplished
       through the structure of the keys which are conventionally structured like object.id.field.
       