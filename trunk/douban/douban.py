# -*- coding: utf-8 -*-

import sys,os
import socket
import urllib2, urllib
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import urlparse

socket_default_timeout = 10 #10s
socket.setdefaulttimeout(socket_default_timeout)

if not os.environ.has_key('http_proxy'):
    os.environ['http_proxy'] = 'http://e2533c:Frank78524#@wwwgate0-ch.mot.com:1080'

(MP3, RM, WMA) = range(3)
music_types = ('mp3', 'rm', 'wma')

def togb2312(ustr):
    #unicode => ascii(gb2312)
    if isinstance(ustr, unicode):
        return ustr.encode('gb2312','ignore')
    else:
        return ustr

def fromgb2312( str ):
    return str.decode('gb2312', 'ignore')

def test_url(song_url):
    default_timeout = socket.getdefaulttimeout()
    timeout = 3 #timeout is 2s
    socket.setdefaulttimeout(timeout)
    res = None
    try:
        song_url = urllib.quote(togb2312(song_url), ':/')
        print 'connect %s ...' % (song_url)
        res = urllib2.urlopen(song_url)
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach the server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        else:
            # everything is fine
            pass
    #restort the default timeout
    socket.setdefaulttimeout(default_timeout)
    return res

def get_song_url_from_baidu(song, player, lrc_url): 
    values = { 'op' : '12',
               'count' : '1',
               'title' : '%s$$%s$$$' % ( togb2312(song), togb2312(player) )
             }
    data = urllib.urlencode(values)
    url = 'http://box.zhangmen.baidu.com/x?' + data
    #print url
    xml = urllib2.urlopen( url )
    #print xml.read()
    soup = BeautifulStoneSoup(xml)
    encode = soup.find('encode').string
    decode = soup.find('decode').string
    song_url = urlparse.urljoin(encode, decode)
    #print song_url
    if lrc_url is None:
        lrcid = int(soup.find('lrcid').string)
        lrc_url = 'http://box.zhangmen.baidu.com/bdlrc/%d/%d.lrc' % (lrcid/100,  lrcid) 
    #print lrc_url
    type = soup.find('type').string
    return song_url, lrc_url, int(type)

def get_song_valid_url( song, player, try_count=5, music_types=(MP3, WMA) ):
    song_url, lrc_url = None, None
    song_size = None
    failed_urls = []
    count = 0
    while count < try_count:
        song_url, lrc_url, mtype = get_song_url_from_baidu(song, player, lrc_url)
        if song_url in failed_urls:
            print 'duplicated url and failed already'
            continue
        if mtype not in music_types:
            print 'music type is not required'
            failed_urls.append( song_url)
            continue
        res = test_url(song_url)
        if res is None:
            failed_urls.append( song_url )
            count += 1
        else:
            song_url = res.geturl() 
            song_url = fromgb2312( urllib.unquote( song_url ) )
            song_size = res.info().get('Content-length')
            main_type, sub_type = res.info().get('Content-type').split('/')
            #print main_type, sub_type
            if main_type.lower() == 'audio': 
                break
            else: 
                print 'mime type is %s/%s, error' % (main_type, sub_type)
                continue
    #print song_url, lrc_url, song_size, mtype
    return song_url, lrc_url, song_size, mtype

def gen_html(album, player, songs_info):
    html_templ = u'''<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <p><strong>专辑名称: %s</strong></p>
        <p><strong>演唱者: %s</strong></p>
        <p></p>
        <table>
            <tr>
            <th>歌曲名</th>
            <th>歌词</th>
            <th>大小</th>
            <th>类型</th>
            </tr>
            %s
        </table>
    </body>
    </html>'''
    html_songlist = u''
    for song in songs_info:
        song_name, song_url, lrc_url, song_size, mtype = song
        #print song_name, song_url, lrc_url, song_size
        if song_size is None: song_size = "invalid"
        mtype = music_types[mtype]
        s = u'''
        <tr>
            <td><a href="%s">%s</td>
            <td><a href="%s">歌词</a></td>
            <td>%s</td>
            <td>%s</td>
        </tr>'''
        html_songlist += s % ( song_url, song_name, lrc_url, song_size, mtype)
    title = '%s (%s)' % (album, player)
    return html_templ % ( title, album, player, html_songlist )

def output_html(html):
    #BeautifulSoup(html).prettify()
    output_file = 'test.html'
    open(output_file, 'w').write( html.encode('utf-8') )


def main():
    src_url = 'http://www.douban.com/subject/1439087/'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'user-agent' : user_agent }
    req = urllib2.Request(src_url, headers=headers)

    res = urllib2.urlopen( req )
    soup = BeautifulSoup(res) 

    album = soup.find('form', id='ssform').h1.string
    #print album
    player = soup.find('span', {'class':'pl2'}).string.split()[1]
    #print player

    rows  = soup.find('table', {'class':'olts'}).findAll('tr')[1:]
    songs = [ row.findAll('td')[0].string for row in rows ]
    songs_info=[]
    for song in songs:
        #print song
        song_url, lrc_url, song_size, song_type = get_song_valid_url( song, player )
        songs_info.append( (song, song_url, lrc_url, song_size, song_type) )
        #break
    html = gen_html(album, player, songs_info)
    output_html(html)

def test_gen_html():
    album = u'那一年'
    player = u'许巍'
    songs_info = []
    song_name = u'闪亮的瞬间'
    song_url = u'http://www.lhnx.com/source/music/许巍/闪亮的瞬间.mp3'
    lrc_url = 'http://box.zhangmen.baidu.com/bdlrc/230/23023.lrc'
    song_size = '4640882' 
    t = urllib.quote(togb2312(song_url), ':/')
    song_url = urllib.unquote(t)
    song_url = song_url.decode('gb2312')
    if isinstance(song_url, unicode): print 'unicode'
    print repr(song_url)
    song = ( song_name, song_url, lrc_url, song_size)
    songs_info.append( song )
    html = gen_html(album, player, songs_info)
    output_html(html)



if __name__ == '__main__':
    #test_gen_html()
    main()

