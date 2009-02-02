#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

from xml.dom import minidom

import logging

trace=logging.debug


class Task(db.Model):
    done = db.BooleanProperty(default=False)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)



class Login(webapp.RequestHandler):
    def post(self):
        user = self.request.get('user');
        passwd = self.request.get('password');
        self.response.out.write('user=%s, password=%s'%(user, passwd))

class List(webapp.RequestHandler):
    def get(self):
       doc = minidom.Document()
       tasks = Task.all()
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
        trace(key, content, doneStr);
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
      self.response.out.write('Happy Chinese New Year!')
          
      
application = webapp.WSGIApplication(
                                     [
                                      ('/', MainPage),
                                      ('/login', Login),
                                      ('/list', List),
                                      ('/add', Add),
                                      ('/delete', Delete),
                                      ('/update', Update),
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()


