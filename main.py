import tornado.ioloop
import tornado.template
import tornado.web
from mongoengine import *
from card_schema import *
import os
import uimodules

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class CreateCardHandler(tornado.web.RequestHandler):
    def get(self):
        print "what?"
        c = Card(name="test", desc="test desc", total_cost=(0, 0, 0, 1, 1, 1), ccost=1, image_path="http://localhost:8888")
        c.save()
    def post(self):
        print "post request"
        cname = self.get_argument('name')
        cdesc = self.get_argument('desc', default="")
        costs = self.get_argument('cost[]')
        img_url = self.get_argument('img_url', default="")
        flavor_text = self.get_argument('flavor_text', default="")
        c = Card.objects(name=cname);
        if len(c) > 0:
            self.write("%s already exists" %cname)
            self.flush()
            return
        c = Card(name=cname, desc=cdesc, total_cost=[costs], ccost=1, image_path=img_url, flv=flavor_text)
        c.save()
        print "Add Card was successful"
        print self.request.arguments

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
    (r"/api/addCard", CreateCardHandler),
    (r"/static/*", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)


if __name__ == "__main__":
        print "XMTG listening on 8888"
        connect('XMTG')
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

