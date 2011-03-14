'''
File: C:\A\eclipse\projects\GAE-Tests\src\relink\relink.py
Author: Melissa Rice 
Last Revision: Sunday 13 March 2011 at 15:18
Purpose: This is the main script handler for the relinkmlr application.
Application URL: http://relinkmlr.appspot.com 
Application Features: The application assists in managing links by providing these features: 
   * Links (URLs) may be stored along with:
      - shortDescription: this is the clickable displayed text of the link.
      - longDescription: a paragraph describing the contents of the page linked to.
      - poster: google gmail name of the person who added the link.
      - postDate: automatically added datetime when the link was added.
      - tags: classifying the link's contents according to user-defined tags.
   * Tags may be store along with:
      - tagName: Alphabetic-only (no space) short name for the tag (main display label).
      - tagDescription: describing the intent of the tag, in case it is not clear.
   * Sorting:
      - links may be sorted alphabetically by shortDescription.
      - links may be sorted reverse chronologically (newest first) by postDate.
      - tags are automatically sorted alphabetically by tagName.
   * Filtering:
      - the set of links tagged with a particular tag can be displayed on a page.
Features in development:
      
'''

debugLevel = 1

# NB: Python version is 2.5 on the appengine site!
import cgi, os, sys, datetime

# change django version before importing the other google.appengine packages (v0.96 is default)
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson as json

# The Datastore Model =========================================================

class Link(db.Model):
    poster = db.UserProperty()
    url = db.LinkProperty(required=True)
    postDate = db.DateTimeProperty(auto_now_add=True)
    shortDescription = db.StringProperty(multiline=False,required=True)
    longDescription = db.StringProperty(multiline=True)
        
class Tag(db.Model):
    tagName = db.StringProperty(multiline=False,required=True)
    tagDescription = db.StringProperty(multiline=False)    

class LinkTag(db.Model):
    tag = db.ReferenceProperty(
        Tag,
        required=True,
        collection_name='links')
    link = db.ReferenceProperty(
        Link,
        required=True,
        collection_name='tags')

# The Request Handlers ========================================================
                
class RelinkHome(webapp.RequestHandler): # Main script handler for relinkmlr app
    def get(self):
        recentLinksQuery = Link.all().order('-postDate')
        recentLinks = recentLinksQuery.fetch(25)
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 

        template_values = {
            'links': recentLinks,
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Links(webapp.RequestHandler):
    def get(self):
        urlArgs = self.request.path.split("/")
        type = urlArgs[1]
        tags = Tag.all()
        if type == 'links-alpha':
            links = Link.all().order('shortDescription')
            mainHead = "Links in Alphabetical Order"
        elif type == 'links-chronos':
            links = Link.all().order('-postDate')
            mainHead = "Links in Reverse Chronological Order"
        else:
            links = Link.all().order('-postDate')
            mainHead = "Links in Reverse Chronological Order"
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in'
        template_values = {
            'tags': tags,
            'links': links,
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
            'mainHead': mainHead,
        }

        path = os.path.join(os.path.dirname(__file__), 'links.html')
        self.response.out.write(template.render(path, template_values))

class LinkDetail(webapp.RequestHandler):
    def get(self):
        urlArgs = self.request.path.split("/")
        linkID = int(urlArgs[2])
        link = Link.get_by_id(linkID)         
        tags = Tag.all()
        checkedTagNames = []
        uncheckedTagNames = []
        taggings = LinkTag.all().filter('link =',link)
        for tagging in taggings:
            checkedTagNames.append(tagging.tag.tagName)
        for tag in tags:
            if tag.tagName not in checkedTagNames:
                uncheckedTagNames.append(tag.tagName)
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in'
        template_values = {
            'link': link,
            'tags': tags,
            'checkedTagNames': checkedTagNames,
            'uncheckedTagNames': uncheckedTagNames,
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        path = os.path.join(os.path.dirname(__file__), 'linkEdit.html')
        self.response.out.write(template.render(path, template_values))


class Tags(webapp.RequestHandler):
    def get(self):
        tags = Tag.all()
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 

        template_values = {
            'tags': tags,
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        path = os.path.join(os.path.dirname(__file__), 'tags.html')
        self.response.out.write(template.render(path, template_values))

class Tagged(webapp.RequestHandler):
    def get(self):
        parts = self.request.path.split("/")
        tagName = parts[2]
        tags = Tag.all().filter('tagName =',tagName)
        links = []
        for tag in tags:
            taggings = LinkTag.all().filter('tag =',tag)
            for tagging in taggings:
                links.append(tagging.link)
                #print tagging.link.key()
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 
        template_values = {
            'links': links,
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
            'tagName': tagName,
            'tags': tags,
        }

        path = os.path.join(os.path.dirname(__file__), 'tagged.html')
        self.response.out.write(template.render(path, template_values))


class AddLink(webapp.RequestHandler):
    def post(self):
        link = Link(
            url=self.request.get('url'),
            shortDescription=self.request.get('short'), 
            poster=users.get_current_user()
            )
        if self.request.get('long'):
            link.longDescription = self.request.get('long')
        link.put()
        tagging = None
        for tag in Tag.all():
            if self.request.get(tag.tagName):
                tagging = LinkTag(link=link,tag=tag)
        if tagging:
            tagging.put()
        self.redirect('/links-chronos/')
    

class UpdateLink(webapp.RequestHandler):
    def post(self):
        parts = self.request.path.split("/")
        linkID = int(parts[2])
        link = Link.get_by_id(linkID)
        link.url=self.request.get('url')
        link.shortDescription=self.request.get('short') 
        if self.request.get('long'):
            link.longDescription = self.request.get('long')
        link.put()
        for tag in Tag.all():
            if self.request.get(tag.tagName):
                taggings = LinkTag.all().filter('link =',link).filter('tag =',tag)
                if not taggings.count():
                    tagging = LinkTag(link=link,tag=tag)
                    tagging.put()
            else:
                taggings = LinkTag.all().filter('link =',link).filter('tag =',tag)
                for tagging in taggings:
                    tagging.delete()
        
        self.redirect('/links-chronos/')
    

class AddTag(webapp.RequestHandler):
    def post(self):
        tag = Tag(tagName=self.request.get('name'))
        if self.request.get('description'):
            tag.tagDescription = self.request.get('description')
        tag.put()
        self.redirect('/tags')
    
class Tasks(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 

        template_values = {
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        path = os.path.join(os.path.dirname(__file__), 'tasks.html')
        self.response.out.write(template.render(path, template_values))

class Admin(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 

        template_values = {
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, template_values))

class Export(webapp.RequestHandler):
    def post(self):
        parts = self.request.path.split("/")
        exportType = parts[3]
        targetTemplate = "export-" + exportType + ".txt" 
        #print >> sys.stderr, targetTemplate
        tags = Tag.all()
        links = Link.all()
        linkTags = LinkTag.all()
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 
        tab = "\t"
        CR = ""
        template_values = {
            'tab': tab,
            'CR': CR,
            'tags': tags,
            'links': links,
            'linkTags': linkTags,
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        path = os.path.join(os.path.dirname(__file__), targetTemplate)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(template.render(path, template_values))

class Import(webapp.RequestHandler):    
    def post(self):
        dtFormat = "%Y-%m-%d-%H:%M:%S"
        parts = self.request.path.split("/")
        importType = parts[3]
        rawData = self.request.get("fileToImport",None)
        if rawData == None:
            return self.error(400) # "No file uploaded for import"
        linkData = []
        tagData = []
        linkTagData = []
        if importType == "json":
            data = json.loads(rawData)
            for obj in data:
                id = obj.get('pk',None)
                type = obj.get('model',None)
                fields = obj.get('fields',None)
                if type == 'relink.Link':
                    poster = fields.get('poster',None)
                    user = users.User(poster)
                    if user:
                        poster = user
                    else:
                        poster = None
                    url = fields.get('url',None)
                    dateString = fields.get('postDate',None)
                    postDate = datetime.datetime.strptime(dateString, dtFormat)
                    shortDescription = fields.get('shortDescription',None)
                    longDescription = fields.get('longDescription',None)
                    link = Link(poster=poster,url=url,postDate=postDate,shortDescription=shortDescription,longDescription=longDescription)
                    existingLink = Link.all().filter('url = ', url).filter('poster = ', poster)
                    if not existingLink.count():
                        link.put()
                elif type == 'relink.Tag':
                    tagName = fields.get('tagName',None)
                    tagDescription = fields.get('tagDescription',None)
                    tag = Tag(tagName=tagName,tagDescription=tagDescription)
                    existingTag = Tag.all().filter('tagName = ', tagName)
                    if not existingTag.count():
                        tag.put()
                elif type == 'relink.LinkTag':
                    tagName = fields.get('tagName',None)
                    url = fields.get('url',None)
                    poster = fields.get('poster',None)
                    user = users.User(poster)
                    if user:
                        poster = user
                    else:
                        poster = None
                    tag = Tag.all().filter('tagName = ', tagName)
                    link = Link.all().filter('url = ', url).filter('poster = ', poster)
                    if link.count() and tag.count():
                        tagKey = tag[0].key()
                        linkKey = link[0].key()
                        linkTag = LinkTag.all().filter('tag = ',tagKey).filter('link = ',linkKey)
                        if not linkTag.count():
                            linkTag = LinkTag(link=linkKey,tag=tagKey)
                            linkTag.put()
                else:
                    pass                              
        elif importType == "csv":
            pass
        else:
            pass
        linkTags = LinkTag.all()
        user = users.get_current_user()
        if user:
            loginURL = users.create_logout_url(self.request.uri)
            loginAction = 'Logout'
            currentLogin = 'Logged in as ' + user.nickname()
        else:
            loginURL = users.create_login_url(self.request.uri)
            loginAction = 'Login'
            currentLogin = 'Not currently logged in' 

        template_values = {
            'loginURL': loginURL,
            'loginAction': loginAction,
            'currentLogin': currentLogin,
        }

        self.redirect('/admin')


# Mapping URLs to Request Handlers ============================================

# this instantiates a WSGI application which maps the urls to handlers 
application = webapp.WSGIApplication([
    ('/', RelinkHome),
    ('/addLink', AddLink),
    ('/updateLink.*', UpdateLink),
    ('/links.*', Links),
    ('/link.*', LinkDetail),
    ('/addTag', AddTag),
    ('/tags', Tags),
    ('/tags/', Tags),
    ('/tag/.*', Tagged),
    ('/admin/tasks', Tasks),
    ('/admin/export.*', Export),    
    ('/admin/import.*', Import),    
    ('/admin.*', Admin),    
    ], debug=debugLevel)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
        
              