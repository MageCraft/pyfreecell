#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import re
import string
import smtplib
import getopt
import time
import calendar

CR_SEPARATOR = "YYY\n"
FIELD_SEPARATOR = "ZZZ"
ENCLOSURE_SEPARATOR = "abcxyzabcxyz"
ENCLOSURE_FIELD_SEPARATOR = "aabbccxxyyzz"

CR_FIELD_NAME = "Identifier"
DDTS_QUERY_FIELDS_URL = 'http://gsm-web.pcs.mot.com/synergy/mmins_crs/GSM/cgi-bin/raw_query_wfields.pl'
DDTS_QUERY_ENV_URL = 'http://gsm-web.pcs.mot.com/synergy/mmins_crs/GSM/cgi-bin/raw_query_enclosures2.pl'

EMAIL_CRR_TEAM = 'e6322c,e13452,crq483,e7915c'
MESSAGING_CRR_TEAM = 'e2533c,dhj476,pfv638,gvr476,e2701c,jgmn78,frnq74,e7261c'

projects = 'lj_email,lj_messaging'
programs = 'LJ07.4,LJ07.2,LJ07.2.1,LJ07.1.1'
ENC_LIST = 'CAAComments'

query_string_fmt = "(Project in (%s)) AND \
(Status NOT IN ('C','D','T','V','R','I')) AND \
(((cr_type = 'defect') AND ((severity in ('1', '2')) or (severity ='3' AND priority = '1'))) or (cr_type IN ('upmerge'))) AND \
(Program in (%s)) AND \
(Analysis_de in (%s))"

fields = 'Identifier, Analysis_de, Project, Description, Status_full_name, CR_type, Severity, Priority, Tracked_by'

DEBUG = False
SEND_NOTIFY_EMAIL = False

def log(msg):
    if DEBUG:
        print msg

def make_query_str(str):
    l = str.split(',')
    return  ",".join([ "'%s'" % (e,) for e in l ])

def quote(str):
    return str.replace(' ', '%20')

def query_cr_fields(query_string, fields):
    url_to_get = DDTS_QUERY_FIELDS_URL + '?' + 'Where=%s&fields=%s' % ( quote(query_string), quote(fields) )
    log(url_to_get)
    res = urllib2.urlopen(url_to_get)
    content = res.read()
    if content[:4] == 'at->':
        log('error, check your query string')
        sys.exit(1)
    #content.replace('\n','')
    l = content[:-3].split(CR_SEPARATOR)
    l1 = []
    cr_list = []
    cr_index = fields.split(', ').index(CR_FIELD_NAME)
    for i in l:
        l2 = i.split(FIELD_SEPARATOR)[:-1]
        cr_list.append(l2[cr_index])
        l1.append(l2)
    return l1, cr_list


def query_cr_enc(cr_list, enc_list=ENC_LIST):
    crs_q = quote(','.join(cr_list))
    enc_list_q = quote(enc_list)
    url_to_get = DDTS_QUERY_ENV_URL + '?' + 'crs=%s&enclosures=%s' % (crs_q, enc_list_q)
    log(url_to_get)
    res = urllib2.urlopen(url_to_get)
    content = res.read()
    #log(content)
    if content[:4] == 'at->':
        log('error, check your query string')
        sys.exit(1)
    content = content[len('<pre>') : -len('</pre>')-1]
    content = content.strip()
    #log(content)
    l1 = content.split(ENCLOSURE_SEPARATOR)
    enc_info_map = {}
    enc_list_l = enc_list.split(',')
    for cr in cr_list:
        enc_info_map[cr] = [''] * len(enc_list_l)
    #log('\n***************************************\n'.join(l1))
    for i in l1:
        if i != '':
            s = i.strip()
            fields = s.split(ENCLOSURE_FIELD_SEPARATOR)
            fields = map(string.strip, fields)
            #log(fields)
            cr, enc_field, content = fields
            ix = enc_list_l.index(enc_field)
            enc_info_map[cr][ix] = re.sub('\n+', '\n', content)
    #log(enc_info_map)
    return enc_info_map
    

Today, Pre_work_day = range(2)

def is_caa_updated(caa, date=Pre_work_day):
    possible_day_fmts = None
    if date == Today:
        year,month,day = time.localtime()[:3]
        possible_day_fmts = get_possible_caa_date_fmt(year,month,day)
    elif date == Pre_work_day:
        year,month,day = get_previous_work_day()
        possible_day_fmts = get_possible_caa_date_fmt(year,month,day)
    for fmt in possible_day_fmts:
        if caa.find(fmt) != -1:
            return True
    return False



def get_possible_caa_date_fmt(year,month,day):
    fmts = []
    mon_name, mon_abbr = calendar.month_name[month], calendar.month_abbr[month]
    fmts.append('%d/%02d/%02d' % (year, month, day)) #2008/04/09
    fmts.append('%02d/%02d/%d' % (month, day, year)) #04/09/2008
    fmts.append('%s %d, %d' % (mon_name, day, year)) #April 11,2008
    fmts.append('%s %d, %d' % (mon_abbr, day, year)) #Apr 11,2008
    return fmts


def get_previous_work_day(tm=time.time()):
    #year, month, day, hour, minute, second, wday, yday, dst = time.localtime(tm)
    wday = time.localtime(tm)[-3]
    pass_day = 1
    if wday == 0: pass_day = 3
    pw_day_time = tm - pass_day * 24 * 3600
    year, month, day = time.localtime(pw_day_time)[:3]
    return year, month, day

def count_cr_by_analysis_de(cr_info_list):
    ade_map = {}
    for info in cr_info_list:
        cr, ade = info[:2]
        ade_map.setdefault(ade,[]).append(cr)
    return ade_map

def get_user_input():
    msg = 'Do you want to send the notify email? [NO]'
    answer = raw_input(msg)
    if answer in ('Yes', 'Y', 'YES', 'yes'):
        return True
    return False

def check_cr_caacomments(projects, programs, analysis_de, check_date=Pre_work_day):
    query_string = query_string_fmt % ( make_query_str(projects), make_query_str(programs), make_query_str(EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM), ) 
    fs = "Identifier, Analysis_de, Status_full_name"
    info_list, cr_list = query_cr_fields(query_string, fs)
    enc_info_map = query_cr_enc(cr_list, 'CAAComments')
    caa_error_l = []
    for info in info_list:
        cr = info[0]
        caa = enc_info_map[cr][0]
        if not caa or not is_caa_updated(caa, check_date):
            caa_error_l.append(info+[caa])
    msg = ''
    if check_date == Pre_work_day: msg = 'on last work day, %d.%d.%d' % get_previous_work_day()
    elif check_date == Today: msg = 'today, %d.%d.%d' % time.localtime()[:3]
    print 'Following are CRs which didn\'t update the CAAComments ' + msg
    for i in caa_error_l:
        print '\t'.join(i[:-1])
        print i[-1]
        if SEND_NOTIFY_EMAIL or get_user_input():
            mail = 'hi,\nPlease update the CAAComments for following CR:\n%s\nThanks' % (i[0])
            send_email('e2533c@motorola.com', '%s@motorola.com' % (i[1],), mail)
        print '\n'


def check_cr_due_date(projects, programs, analysis_de):
    query_string = query_string_fmt % ( make_query_str(projects), make_query_str(programs), make_query_str(EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM), ) 
    fs = "Identifier, Analysis_de, Status_full_name, Analysis_due_date, Due_date"
    info_list, cr_list = query_cr_fields(query_string, fs)
    a_due_error_l = []
    due_error_l = []
    for info in info_list:
        #log(info)
        state, a_due_date, due_date = info[2:]
        if a_due_date in ('','NULL'):
            a_due_error_l.append(info)
        if state in ('Working', 'Resloved') and due_date in ('','NULL'):
            due_error_l.append(info)
    return a_due_error_l, due_error_l


#check analysis_due_date, due_date
def check_cr_validity():
    a_due_error_l, due_error_l = check_cr_due_date(projects, programs, EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM)
    
    def show_info(ll):
        for i in ll:
            print '\t'.join(i)

        
    if a_due_error_l:
        print 'Following are the CRs without analysis_due_date filled'
        show_info(a_due_error_l)
        if SEND_NOTIFY_EMAIL or get_user_input():
            d = count_cr_by_analysis_de(a_due_error_l)
            for key in d.keys():
                mail = 'hi,\nPlease fill the "Analysis Due Date" for following CR:\n%s\nThanks' % ('\n'.join(d[key]), )
                send_email('e2533c@motorola.com', '%s@motorola.com' % (key,), mail)
        
    if due_error_l:
        print 'Following are the CRs without due_date filled'
        show_info(due_error_l)
        d = count_cr_by_analysis_de(due_error_l)
        if SEND_NOTIFY_EMAIL or get_user_input():
            d = count_cr_by_analysis_de(due_error_l)
            for key in d.keys():
                mail = 'hi,\nPlease fill the "Due Date" for following CR:\n%s\nThanks' % ('\n'.join(d[key]), )
                send_email('e2533c@motorola.com', '%s@motorola.com' % (key,), mail)



def send_email(fromaddr, toaddrs, mail):
    #toaddrs += ', e2533c@motorola.com'
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, toaddrs))
    msg = msg + mail
    #log(toaddrs)
    log(msg)

    server = smtplib.SMTP('remotesmtp.mot.com')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    

def output_to_csv(cr_info_list, out_fn='cr_status.csv'):
    content = ''
    header = enc_list.split(',') + fields.split(', ')
    def quote(e):
        if e == 'NULL': e=''
        str = re.sub('\n+','\n',e)
        str = re.sub('"', '""', str) #for excel csv, " should be escaped by add another " before.
        return '"%s"' % (str,)

    content += ",".join( map(quote, header) )
    content += '\n'
    for info in cr_info_list:
        content += ",".join( map(quote, info) )
        content += '\n'
    open(out_fn, 'w').write(content)

def report_cr_status():
    query_string = query_string_fmt % ( make_query_str(projects), make_query_str(programs), make_query_str(EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM), ) 
    info_list, cr_list = query_cr_fields(query_string, fields)
    enc_info_map = query_cr_enc(cr_list)
    cr_index = fields.split(', ').index(CR_FIELD_NAME)
    for index in range(len(info_list)):
        info = info_list[index]
        cr = info[cr_index]
        if enc_info_map.has_key(cr):
            info_list[index] = enc_info_map[cr] + info
        else:
            info_list[index] = [''] * len(enc_list.split(',')) + info
    output_to_csv(info_list)



def usage():
    print '''Usage: 
    %(me)s report [-d] 
    %(me)s checkcr [-e] [-d] 
    %(me)s checkcaa [-n] [-e] [-d] 
    %(me)s ut 

    report      generate the CR status report
        -d -- enable the debug log

    checkcr     check the CR "Analysis Due Date", "Due Date"
        -e -- send the notify email
        -d -- enable the debug log

    checkcaa    check the "CAAComments" for every CR
        -n -- check if the "CAAComments" updated today, defaultly check last work day
        -e -- send the notify email
        -d -- enable the debug log

    ut          do unittest
    ''' % { 'me' : sys.argv[0] }


def test():
    #log(query_string_fmt)
    #query_string = query_string_fmt % ( make_query_str(projects), make_query_str(programs), make_query_str(EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM), ) 
    #log(query_string)
    #log(make_query_str(EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM))
    global DEBUG
    year, month, day = get_previous_work_day()
    print year, month, day
    possible_date = get_possible_caa_date_fmt(year,month,day)
    print possible_date
    caa = '''
    '''
    re = is_caa_updated(caa, Pre_work_day)
    print re
    DEBUG = True
    check_cr_caacomments(projects, programs, EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM)

if __name__ == '__main__':
    if len(sys.argv) == 1 or not sys.argv[1] in ('report', 'checkcr', 'ut', 'checkcaa'):
        usage()
        sys.exit(1)
    cmd = sys.argv[1]
    cmd_params = sys.argv[2:]
    
    if cmd == 'report':
        try:
            opt_list, args = getopt.getopt(cmd_params, 'd')
        except getopt.GetoptError, msg:
            print msg
            usage()
            sys.exit(1)
        if not opt_list:
            DEBUG = False
        else:
            for opt, value in opt_list:
                if opt == '-d':
                    DEBUG = True
        print 'generating CR status report...'
        report_cr_status()
    elif cmd == 'checkcr':
        try:
            opt_list, args = getopt.getopt(cmd_params, 'de')
        except getopt.GetoptError, msg:
            print msg
            usage()
            sys.exit(1)
        if not opt_list:
            DEBUG = False
        else:
            for opt, value in opt_list:
                if opt == '-d':
                    DEBUG = True
                elif opt == '-e':
                    SEND_NOTIFY_EMAIL = True
        print 'checking CR "Analysis Due Date", "Due Date" ...'
        check_cr_validity()
    elif cmd == 'ut':
        test()
    elif cmd == 'checkcaa':
        try:
            opt_list, args = getopt.getopt(cmd_params, 'nde')
        except getopt.GetoptError, msg:
            print msg
            usage()
            sys.exit(1)
        check_date = Pre_work_day
        if not opt_list:
            DEBUG = False
        else:
            for opt, value in opt_list:
                if opt == '-d':
                    DEBUG = True
                elif opt == '-e':
                    SEND_NOTIFY_EMAIL = True
                elif opt == '-n':
                    check_date = Today
        print 'checking CR "CAAComments" ...'
        check_cr_caacomments(projects, programs, EMAIL_CRR_TEAM + ',' + MESSAGING_CRR_TEAM, check_date)
        


        
                






    




