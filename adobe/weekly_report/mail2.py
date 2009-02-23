import smtplib
from xml.dom import minidom
from xml.dom.minidom import parse

import sys

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from datetime import date, timedelta
import calendar
from string import Template



def createhtmlmail2(html, text, subject, sender, recipient):
    msgRoot = MIMEText(html, 'html')
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = recipient

    return msgRoot.as_string()




def createhtmlmail1(html, text, subject, sender, recipient):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = recipient

    msgAlernative = MIMEMultipart('alernative')
    msgRoot.attach(msgAlernative)

    msgHtml = MIMEText(html, 'html')
    msgAlernative.attach(msgHtml)

    msgTxt = MIMEText(text)
    msgAlernative.attach(msgTxt)

    return msgRoot.as_string()

def load_mail(this_week=True):
    mail_file='weekly_report.xml'
    html_temp_file='weekly_report_template.html'
    html_temp = Template(open(html_temp_file).read())
    f = open(mail_file)
    xml = parse(mail_file)
    root = xml.documentElement
    root_title = root.getAttribute('title')
    items = root.getElementsByTagName('item')
    print len(items)
    if this_week:
        html_body = '<h2>%s</h2>' % (root_title+get_this_week())
    else:
        html_body = '<h2>%s</h2>' % (root_title+get_last_week())

    text = root_title + '\n\n\n'
    indent = '  '
    for item in items:
        item_title = item.getAttribute('title')
        print item.nodeName, item_title
        html_body += '<h3>%s</h3>' % item_title
        text += item_title + '\n'
        default = None
        if item.hasAttribute('default'):
            default=item.getAttribute('default')
        if item.firstChild:
            content = item.firstChild.data.strip()
            if content:
                l = content.split('\n')
                html_body += '<ol>'
                for li in l:
                    html_body += '<li>%s</li>' % li.strip()
                    text += indent + li.strip() + '\n'
                html_body += '</ol>'
            else:
                if not default:
                    print 'Error!'
                    print 'There must have content under %s' % item_title
                    sys.exit(1)
                else:
                    content = default
                    html_body += '<ul>'
                    html_body += '<li>%s</li>' % content
                    text += indent + content + '\n'
                    html_body += '</ul>'
        text += '\n'
    print html_body
    print text
    return html_temp.substitute(title=root_title, body=html_body), text

def get_last_week():
    today = date.today()
    calendar.setfirstweekday(calendar.MONDAY)
    weekday = today.weekday()
    print weekday
    delta = timedelta(weekday)
    this_monday = today - delta
    last_monday = this_monday - timedelta(7)
    last_friday = last_monday + timedelta(4)
    return '(%s --- %s)' % (str(last_monday), str(last_friday))



def get_this_week():
    today = date.today()
    calendar.setfirstweekday(calendar.MONDAY)
    weekday = today.weekday()
    print weekday
    delta = timedelta(weekday)
    this_monday = today - delta
    this_friday = this_monday + timedelta(4)
    print str(this_monday), str(this_friday)
    return '(%s --- %s)' % (str(this_monday), str(this_friday))



def main(this_week=True):
    server = smtplib.SMTP('inner-relay-1.corp.adobe.com')

    html, text = load_mail(this_week)
    if this_week:
        subject = 'Weekly Report' + get_this_week()
    else:
        subject = 'Weekly Report' + get_last_week()

    html1='''<html><body><h1>Hello</h1></body></html>'''

    msg = createhtmlmail2(html, text, subject, 'xzheng', 'xzheng')

    server.set_debuglevel(1)

    server.sendmail('xzheng', 'xzheng', msg)




if __name__ == '__main__':
    #print get_this_week()
    #print get_last_week()
    #print getWeek()
    #html,txt = load_mail()
    #print html
    this_week = True
    if len(sys.argv) == 2 and sys.argv[1] == '-l':
        this_week = False

    main(this_week)


