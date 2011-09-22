import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

import xml2html

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
	
	def get(self):
		(byArtist, byAlbum, byGenre, bySong) = xml2html.GenHTMLFiles()
		
		albums = list()
		
		for album in byAlbum:
			artist_name, album_name = album.split(":")
			temp = {}
			temp[ 'artist' ] = artist_name
			temp[ 'album' ] = album_name
			albums.append( temp )
		
		self.render( 'index.html', albums=albums )

def main():
	settings = {
		"template_path": os.path.join(os.path.dirname(__file__), "templates"),
		"static_path": os.path.join(os.path.dirname(__file__), "static"),
		"css_path": os.path.join(os.path.dirname(__file__), "css")		
	}

	tornado.options.parse_command_line()
	application = tornado.web.Application([
		(r"/", MainHandler),
	], **settings)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()