import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/search" method="get">'
                   '<input type="text" name="q">'
                   '<input type="submit" value="Search">'
                   '</form></body></html>')


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("q"))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/search", SearchHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
