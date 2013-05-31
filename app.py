import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    ''' Application router and settings'''
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/search", SearchHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    ''' Homepage handler'''
    def get(self):
        self.render("home.html")


class SearchHandler(tornado.web.RequestHandler):
    ''' Search page handler'''
    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("q"))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
