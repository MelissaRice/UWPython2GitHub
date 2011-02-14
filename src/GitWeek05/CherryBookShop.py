'''
File: CherryBookShop.py
Last Revision: 13 February 2011
Assignment for Week 5: Write a dynamic website based on the bookdb data:
  1. Provide index page with list of books linking to detail page for each book
  2. Provide a detail page for each book
'''

import cherrypy
import os

configFilepath = os.path.join(os.path.dirname(__file__), 'CherryBookShop.conf')
print configFilepath

# let's pretend we're getting this information from a database somewhere
database = {
    'id1' : {'title' : 'CherryPy Essentials: Rapid Python Web Application Development',
             'isbn' : '978-1904811848',
             'publisher' : 'Packt Publishing (March 31, 2007)',
             'author' : 'Sylvain Hellegouarch',
           },
    'id2' : {'title' : 'Python for Software Design: How to Think Like a Computer Scientist',
             'isbn' : '978-0521725965',
             'publisher' : 'Cambridge University Press; 1 edition (March 16, 2009)',
             'author' : 'Allen B. Downey',
           },
    'id3' : {'title' : 'Foundations of Python Network Programming',
             'isbn' : '978-1430230038',
             'publisher' : 'Apress; 2 edition (December 21, 2010)',
             'author' : 'John Goerzen',
           },
    'id4' : {'title' : 'Python Cookbook, Second Edition',
             'isbn' : '978-0-596-00797-3',
             'publisher' : 'O''Reilly Media',
             'author' : 'Alex Martelli, Anna Ravenscroft, David Ascher',
           },
    'id5' : {'title' : 'The Pragmatic Programmer: From Journeyman to Master',
             'isbn' : '978-0201616224',
             'publisher' : 'Addison-Wesley Professional (October 30, 1999)',
             'author' : 'Andrew Hunt, David Thomas',
           },
}

baseURL = "http://block115397-xwp.blueboxgrid.com:8080/"

headerTemplate = '''
<html><head>
    <title>%s</title>
    <style type="text/css">
    body { background-color: #ccddff; color: #0000dd; }
    a:link {text-decoration: underline; color: #6622aa;}
    a:visited {text-decoration: underline;  color: #9900dd;}
    p.title{font:bold 25px/27px Georgia,serif;}
    p.author{font:italic 20px/22px Times,serif;}
    p.publisher{font: 15px/16px Times,serif;}
    p.isbn{font: 15px/16px Times,serif;}
    p.other{font: 15px/16px Times,serif; color: #9900bb;}
    </style>
</head>'''
bodyTemplate = "<body><h1>%s</h1>%s</body></html>"
class BookDB():
    def getBookData(self,bookID=None):
        if bookID == None:
            books = [dict(id=id, title=database[id]['title'],author=database[id]['author'],publisher=database[id]['publisher'],isbn=database[id]['isbn']) for id in database.keys()]
            return books
        else:
            if database.has_key(bookID):
                return dict(id=bookID, title=database[bookID]['title'],author=database[bookID]['author'],publisher=database[bookID]['publisher'],isbn=database[bookID]['isbn'])
            else:
                return None
    def title_info(self, id):
        return database[id]
    def index(self):
        bookList = "<ul>"
        books = self.getBookData()
        for book in books:
            url = baseURL + "book/" + book.get('id',"")
            bookList += '<li><a href="%s">%s</a> by %s</li>' % (url, book.get('title',""),book.get('author',""))
        bookList += "</ul>"
        output = headerTemplate % "Book List"
        output += bodyTemplate % ("Book List",bookList)
        return output
    index.exposed = True
    def book(self,id):
        output = headerTemplate
        book = self.getBookData(id)
        if book != None:
            output += '<p class="title">Title: %s</p>' % book.get('title',"")
            output += '<p class="author">Author: %s</p>' % book.get('author',"")
            output += '<p class="publisher">Publisher: %s</p>' % book.get('publisher',"")
            output += '<p class="isbn">ISBN: %s</p>' % book.get('isbn',"")
            output += '<a href="%s">%s</a>' % ("/","Back to book list")
        output += "</body></html>" 
        return output
    book.exposed = True
        

cherrypy.config.update({'server.socket_host': 'block115397-xwp.blueboxgrid.com',
                        'server.socket_port': 8080,
                       })
# 208.85.148.123

root = BookDB()    
cherrypy.tree.mount(root, '/', configFilepath)
cherrypy.tree.mount(root.book, '/book/')

cherrypy.quickstart(root)
