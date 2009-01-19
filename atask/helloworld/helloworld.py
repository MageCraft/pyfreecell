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
    content = db.StringProperty(multiline=True)



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
           task_node.setAttribute('id', str(task.key().id()))
           task_node.setAttribute('content', task.content)
           tasks_node.appendChild(task_node)
       trace(doc.toxml())
       self.response.headers['Content-Type'] = 'text/xml'
       self.response.out.write(doc.toxml())

class Add(webapp.RequestHandler):
    def post(self):
        task = Task()
        task.content = self.request.get('content');
        task.put()
        self.response.out.write('id=%s'%(task.key()))


class Delete(webapp.RequestHandler):
    def post(self):
        pass

class Update(webapp.RequestHandler):
    def post(self):
        pass
        


class MainPage(webapp.RequestHandler):
  def get(self):
      
      if user:
          path = os.path.join(os.path.dirname(__file__), 'html/index.html')
          template_values = {
                  'current_user': user.nickname(),
          }
          self.response.out.write(template.render(path, template_values))
      else:
          self.redirect(users.create_login_url(self.request.uri))
          
      
application = webapp.WSGIApplication(
                                     [
                                      ('/', MainPage),
                                      ('/login', Login),
                                      ('/list', List),
                                      ('/add', Add),
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

