import smtplib
from xml.dom import minidom
from xml.dom.minidom import parse

import sys

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from datetime import date, timedelta
import calendar



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

def load_mail():
    mail_file='weekly_report.xml'
    f = open(mail_file)
    xml = parse(mail_file)
    root = xml.documentElement
    root_title = root.getAttribute('title')
    items = root.getElementsByTagName('item')
    print len(items)
    html = '<html><head><title>Weekly Report</title></head><body>' 
    html += '<h2>%s</h2>' % (root_title+getWeek())
    text = root_title + '\n\n\n'
    indent = '  '
    for item in items:
        item_title = item.getAttribute('title')
        print item.nodeName, item_title
        html += '<h3>%s</h3>' % item_title
        text += item_title + '\n'
        default = None
        if item.hasAttribute('default'):
            default=item.getAttribute('default')
        if item.firstChild:
            content = item.firstChild.data.strip()
            if content:
                l = content.split('\n')
                for li in l:
                    html += '<li>%s</li>' % li.strip()
                    text += indent + li.strip() + '\n'
            else:
                if not default:
                    print 'Error!'
                    print 'There must have content under %s' % item_title
                    sys.exit(1)
                else:
                    content = default
                    html += '<li>%s</li>' % content
                    text += indent + content + '\n'
        text += '\n'
    html += '</body></html>'
    print html
    print text
    return html, text


def getWeek():
    today = date.today()
    calendar.setfirstweekday(calendar.MONDAY)
    weekday = today.weekday()
    print weekday
    delta = timedelta(weekday)
    this_monday = today - delta
    this_friday = this_monday + timedelta(4)
    print str(this_monday), str(this_friday)
    return '(%s --- %s)' % (str(this_monday), str(this_friday))



def main():
    server = smtplib.SMTP('inner-relay-1.corp.adobe.com')

    html, text = load_mail()
    subject = 'Weekly Report' + getWeek()

    html1='''<html><body><h1>Hello</h1></body></html>'''

    msg = createhtmlmail2(html, text, subject, 'xzheng', 'xzheng')

    server.set_debuglevel(1)

    server.sendmail('xzheng', 'xzheng', msg)




if __name__ == '__main__':
    #print getWeek()
    main()




