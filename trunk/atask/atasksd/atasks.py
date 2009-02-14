#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

from xml.dom import minidom
from xml.dom.minidom import parse

import logging

trace=logging.debug

client_name='xatasks'
client_versions_file='version.xml'
client_releases_dir='releases'

def current_client_versions():
    f=open(client_versions_file)
    dom=parse(f)
    root = dom.documentElement
    bvNode=root.getElementsByTagName('base_version')[0]
    cvNode=root.getElementsByTagName('current_version')[0]
    return bvNode.firstChild.data, cvNode.firstChild.data


def current_client():
    bv, cv = current_client_versions()
    client_package_name=client_name+'-'+cv
    release_dir=client_releases_dir + '/' + client_package_name 
    client_package_url=release_dir + '/' + client_package_name+'.air'
    client_package_release_note=release_dir + '/' + 'release_note.txt'
    return client_package_name, client_package_url, client_package_release_note



class CheckUpdate(webapp.RequestHandler):
    def get(self):
        cv = self.request.get('currentVersion')
        needUpdate = False
        update_url = None
        cnote = None
        if cv:
            bv, lv = current_client_versions()
            if lv != cv:
                needUpdate = True
                cn, update_url, cnote = current_client()
        self.response.out.write('needUpdate=%s&updateURL=%s&updateRelNote=%s&latestVersion=%s' % 
                (str(needUpdate).lower(), update_url, cnote, lv) )

class Task(db.Model):
    done = db.BooleanProperty(default=False)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    email=db.StringProperty()


class List(webapp.RequestHandler):
    def get(self):
       email = self.request.get('email').lower()       
       trace(email)
       tasks = Task.gql("WHERE email = :1 ORDER BY date", email)
       doc = minidom.Document()
       tasks_node = doc.createElement('tasks')
       doc.appendChild(tasks_node)
       for task in tasks:
           task_node = doc.createElement('task')
           task_node.setAttribute('key', str(task.key()))
           task_node.setAttribute('content', task.content)
           task_node.setAttribute('done', str(task.done).lower())
           tasks_node.appendChild(task_node)
       trace(doc.toxml())
       self.response.headers['Content-Type'] = 'text/xml'
       self.response.out.write(doc.toxml())

class Add(webapp.RequestHandler):
    def post(self):
        task = Task()
        task.content = self.request.get('content');
        task.email = self.request.get('email');
        task.put()
        self.response.out.write('key=%s' % (str(task.key())) )


class Delete(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key');
        trace(key);
        task = db.get(db.Key(key));
        trace(task.content);
        task.delete()
        self.response.out.write('deleted')
        
class Update(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key');
        content = self.request.get('content')
        doneStr = self.request.get('done')
        trace(key) 
        trace(content)
        trace(doneStr)
        done = True
        if doneStr == 'false':
            done = False
        task = db.get(db.Key(key));
        trace(task.content);
        task.content = content
        task.done = done
        task.put()
        self.response.out.write('updated')
        


class MainPage(webapp.RequestHandler):
  def get(self):
      user = users.get_current_user()
      html1=''
      if user:
          tasks = None
          if users.is_current_user_admin():
              tasks = Task.gql("ORDER BY date")
          else:
              tasks = Task.gql("WHERE email = :1 ORDER BY date", user.email())
          html1 = '''<table border>
          <tr><th>task</th><th>date</th><th>done</th><th>email</th></tr>
          '''
          for task in tasks:
              html1 += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (task.content, task.date.isoformat(), str(task.done), task.email)
          html1 += '</table>'    
          html1 += '''<p><a href=%s>Logout</a></p>''' % (users.create_logout_url('/'))
      else:
          html1 = '''<p><a href="%s">Sign In</a></p>''' % (users.create_login_url('/'))

      cname,curl,crelnote=current_client()
      html = '''<html>
      <body>
      <p>Happy Chinese New Year!</p>
      <p><a href="%s">%s</a></p>
      <p><a href="%s">release note</a></p>
      %s
      </body>
      </html>
      ''' % (curl, cname, crelnote, html1) 
      self.response.out.write(html)
          
      
application = webapp.WSGIApplication(
                                     [
                                      ('/', MainPage),
                                      ('/list', List),
                                      ('/add', Add),
                                      ('/delete', Delete),
                                      ('/update', Update),
                                      ('/checkupdate', CheckUpdate),
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()


