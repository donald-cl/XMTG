import tornado.ioloop
import tornado.template
import tornado.web
from mongoengine import *
import card_schema
import os
import uimodules

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class MainHandler(tornado.web.RequestHandler):
    def init_html(self):
        t = tornado.template.Template("<html><div id='main'>{{vnum}}</div></html>")
        content_html = t.generate(vnum="0.0")
        self.write(content_html)
    def get(self):
        self.write("XMTG ")
        self.init_html()
        Entry = Entry()

settings = {
    "ui_modules": uimodules,
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}
application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/static/*", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)


if __name__ == "__main__":
        print "XMTG listening on 8888"
        connect('XMTG')
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

