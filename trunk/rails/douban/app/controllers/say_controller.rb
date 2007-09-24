#require 'engine'
load 'engine.rb'

class SayController < ApplicationController
    def hello
    end

    def index
    end

    def get_songs_info
	@address = params[:address]
	puts "adress is #{@address}"
        @album, @player, @songs, @album_img_url = fetch_album_from_douban(@address)
	@songs_info = []
	@songs.each { |song|
	    song_url, lrc_url, song_type = get_song_url_from_baidu( valid_song_name(song), @player ) 
	    @songs_info << [song, song_url, lrc_url, song_type]
	}        
	render :partial => 'songs_list', :object => @songs_info
    end

    def query
	@address = params[:address]
	puts "adress is #{@address}"
        @album, @player, @songs, @album_img_url = fetch_album_from_douban(@address)
	@songs_info = []
	@songs.each { |song|
	    #song_url, lrc_url, song_type = get_song_url_from_baidu( valid_song_name(song), @player ) 
	    #puts song_url, lrc_url, song_type
	    song_url, lrc_url, song_type = nil, nil, nil
	    @songs_info << [song, song_url, lrc_url, song_type]
	}        
    end

    private
    def check_adress(address)
	true
    end
    


end


