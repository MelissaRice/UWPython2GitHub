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
   The three files included are:
   RedisStuff.py: class definitions:
       RedisObject will be an abstract base class providing encapsulation of all redis commands
       Person is a class for encapsulating information about people (to be stored under keys of
          the form person:<personID>:<fieldName> such as person.8.last.name or person.8.birthday
   RedisTestRunA.py: demonstrates using the Person class to create some people data and store it
       in the redis datastore.
   RedisTestRunB.py: demonstrates using retrieving data from the redis datastore into Person objects
       and then displaying that data.
       
       