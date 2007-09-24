#!/usr/bin/env ruby
require 'rubygems'
require 'mechanize'
require 'hpricot'
require 'uri'
require 'iconv'

MUSIC_TYPES = { '0' => 'mp3', '1' => 'rm', '2'=>'wma' }

(MP3, RM, WMA) = (0..2).to_a
music_types = ('mp3', 'rm', 'wma')

$agent = WWW::Mechanize.new
#set proxy
$agent.set_proxy('wwwgate0-ch.mot.com', '1080', 'e2533c', 'Frank78524$')
#set user-agent
$agent.user_agent_alias='Windows IE 6'

def parse_player(player_string)
    if player_string =~ /表演者: (.+)/
	tmp = $1
	players = tmp.split(/\s\/\s/)
	players[0]
    else
	nil
    end
end

def fetch_album_from_douban(url)
    page = $agent.get url
    #puts page.body
    album  = page.search("//form[@id='ssform']/h1").first.inner_text
    player = page.search("//span.pl2").first.inner_text
    player = parse_player(player)
    rows = page.search("//table.olts//tr")[1..-1]

    #album image url
    path = page.search("//div.fil//img").first.attributes["src"]
    album_img_url = URI::HTTP.build( {:host => URI.parse(url).host, :path => path} ).to_s
    #puts rows.size
    songs = []
    rows.each { |row|
	songs << row.search("/td").first.inner_text
    }
    #puts album, player, songs, album_img_url
    return album, player, songs, album_img_url
end

def utf8_to_gb2312(ustr)
    Iconv.conv('gb2312', 'UTF-8', ustr)
end

def get_song_valid_url( song, player, try_count=5, music_types=(MP3,WMA) )
    song_url, lrc_url, song_size = nil, nil, nil
    failed_urls = []
    dup_failed_count = 0
    dup_failed_count_max = 10
    count = 0
    while count < try_count:
	song_url, lrc_url, mtype = get_song_url_from_baidu(song, player, lrc_url)
	if not song_url:
	    puts "can't find the song by baidu mp3 search engine, song: #{song}, player:#{player}" 
	    break
	end
	if failed_urls.index(song_url)
	    puts 'duplicated url and failed already'
	    dup_failed_count += 1
	    if dup_failed_count == dup_failed_count_max
		puts 'reach the max try count, failed'
		break
	    else
		next
	    end
	end
	if not music_types.index(mtype)
	    puts 'music type is not required'
	    failed_urls << song_url
	    next
	res = test_url( song_url )
	if not res
	    failed_urls << song_url
	else
	    song_size = 
	end




end

def get_song_url_from_baidu(song, player)
    song = utf8_to_gb2312 song
    player = utf8_to_gb2312 player
    url = "http://box.zhangmen.baidu.com/x?op=12&count=1&title=#{song}$$#{player}$$$"
    url = URI.escape url
    #puts url
    xml = $agent.get url
    #puts xml.body
    doc = Hpricot(xml.body)
    song_url, lrc_url, song_type = nil, nil, nil
    encode = doc.search("//encode").inner_text
    decode = doc.search("//decode").inner_text
    #puts encode, decode
    if encode == 'nothing'
      puts 'failed to find the song by baidu'
    else
      song_url = URI.join URI.escape(encode), URI.escape(decode)
      type = doc.search("//type").inner_text
      lrcid = doc.search("//lrcid").inner_text.to_i
      lrc_url = "http://box.zhangmen.baidu.com/bdlrc/%d/%d.lrc" % [lrcid/100,  lrcid]
      song_type = MUSIC_TYPES[type] 
    end    
    return song_url, lrc_url, song_type
end

def valid_song_name(song_name)
    song_name.gsub(/\s?(\(|（).+$/, '')
end
    

def test
    src_urls = [ 'http://www.douban.com/subject/2134548',
                'http://www.douban.com/subject/2131595/'               
              ]
    src_urls.each { |src_url|
      album, player, songs, album_img_url = fetch_album_from_douban src_url
      puts album, player, album_img_url    
      songs_info = []
      songs.each { |song|
          song_url, lrc_url, song_type = get_song_url_from_baidu( valid_song_name(song), player ) 
          puts song_url, lrc_url, song_type
          songs_info << [song_url, lrc_url, song_type]
      }
    }
end

def test2
    URI.join('http://www.feeling3000.com/pages/../mediafile/blogmusic/7~~79woYAQ~pGjM$.mp3', URI.escape('�������׸�.mp3'))
end

def test1
    song_url, lrc_url, song_type = get_song_url_from_baidu 'それぞれに', '中孝介'
    puts song_url, lrc_url, song_type
end

def test3
    s = ["小星星 （feat 阿里山桃花村姐妹）", "真昼の花火 (正午的烟火)"]
    s.each { |e|
	puts valid_song_name(e)
    }
end

def test4
    src_url = 'http://www.douban.com/subject/2138438/'
    fetch_album_from_douban src_url
end

if $0 == __FILE__
    test4
end
