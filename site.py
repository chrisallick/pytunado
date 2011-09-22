import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

import xml2html

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class MainHandler( tornado.web.RequestHandler ):

	def get(self):
		(byAlbum, bySong) = xml2html.GenHTMLFiles()

		songs = {}
		for k, v in bySong.iteritems():
			if v not in songs:
				songs[v] = list()
			songs[v].append(k)

		albums = list()
		for album in byAlbum:
			artist_name, album_name = album.split(":")
			temp = {}
			temp[ 'artist' ] = artist_name
			temp[ 'album' ] = album_name
			temp[ 'songs' ] = songs[ album_name ]
			albums.append( temp )
		
		self.render( 'index.html', albums=albums )

class PlayAlbumHandler( tornado.web.RequestHandler ):
	
	def get( self ):
 		album = self.get_argument( 'album', None )

		if album:
			runCmd( 'osascript -e \'tell application "iTunes" to play (get item 1 of (get every track of playlist "Library" whose album is "%s"))\'' % album)
			self.write("success!")

class PlaySongHandler( tornado.web.RequestHandler ):

	def get( self ):
 		song = self.get_argument( 'song', None )

		if song:
			runCmd( "osascript -e \"tell application \\\"iTunes\\\" to play (get item 1 of (get every track of playlist \\\"Library\\\" where name is \\\"%s\\\"))\"" % song )
			self.write("success!")

def runCmd( cmd ):
	os.system( cmd )
	
def main():
	settings = {
		"template_path": os.path.join(os.path.dirname(__file__), "templates"),
		"static_path": os.path.join(os.path.dirname(__file__), "static")
	}

	tornado.options.parse_command_line()
	application = tornado.web.Application([
		(r"/", MainHandler),
		(r"/playalbum", PlayAlbumHandler),
		(r"/playsong", PlaySongHandler)
	], **settings)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()