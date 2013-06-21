import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time
from tornado.options import define, options
from pymongo import MongoClient
import gridfs
from indexer.Rank import QueryAnalysis, Ranker

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    ''' Application router and settings'''
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/search", SearchHandler),
            (r"/cache", CacheHandler),
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
    db = MongoClient().poky
    ranker = Ranker()
    qa = QueryAnalysis()

    def get(self):
        start_time = time.time()
        query = self.get_argument("q")
        doc_ids = self.ranker.rank(self.qa.analysis(query))
        # term = self.db.terms.find_one({"word": query})
        # if term is None:
            # doc_ids = []
        # else:
            # doc_ids = [node["doc_id"] for node in term["posting"]]
        documents = [self.db.documents.find_one({"_id": doc_id}) for doc_id in doc_ids]
        # documents.sort(key=lambda e: e["pagerank"], reverse=True)
        self.render("search.html", documents=documents, query=query, time=time.time()-start_time)


class CacheHandler(tornado.web.RequestHandler):
    ''' Page Cache'''
    db = MongoClient().poky
    fs = gridfs.GridFS(db)

    def get(self):
        url = self.get_argument("url")
        document = self.db.documents.find_one({"url": url})
        if document:
            self.set_header("Content-Type", "text/html")
            self.write(self.fs.get(document["body"]).read())
        else:
            self.redirect('/')


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
