import tornado.ioloop
import tornado.template
import tornado.web
from mongoengine import *
from card_schema import *
import os
import uimodules
import urllib
import subprocess
import pipes

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/html/main.html")

class SearchCardHandler(tornado.web.RequestHandler):
    def get(self):
        print "get search request"
    def post(self):
        print "search request"
        query = self.get_argument('query');
        c = Card.objects(name=query);
        if c is None or len(c) <= 0:
            print "no results"
            self.write("Card not found. You should add it instead!")
            return
        self.write("Found")
        self.flush()

class CreateCardHandler(tornado.web.RequestHandler):
    def get(self):
        print "what?"
        c = Card(name="test", desc="test desc", total_cost=(0, 0, 0, 1, 1, 1), ccost=1, image_path="http://localhost:8888")
        c.save()
    def post(self):
        print "post request"
        cname = self.get_argument('name')
        cdesc = self.get_argument('desc', default="")
        costs = self.request.arguments.get('cost[]')
        img_url = self.get_argument('img_url', default="")
        flavor_text = self.get_argument('flavor_text', default="")
        
        total_cost =[] 
        cost_dict = {}
        for c in costs:
            if type(c) == int:
                cost_dict['colorless'] = cost_dict.get(c, 0) + 1
            else:
                cost_dict[str(c).lower()] = cost_dict.get(str(c).lower(), 0) + 1

        colors = ['b','g','r','w','u','colorless']

        for color in colors:
            if color not in cost_dict:
                cost_dict[color] = 0

        for key, val in cost_dict.items():
            total_cost.append(val)
        
        c = Card.objects(name=cname);

        if len(c) > 0:
            self.write("%s already exists" %cname)
            self.flush()
            return
        c = Card(name=cname, 
                lowername=cname.lower(),
                desc=cdesc, 
                lowerdesc=cdesc.lower(),
                total_cost=total_cost,
                ccost=cost_dict['colorless'],
                bcost=cost_dict['b'], 
                gcost=cost_dict['g'],
                rcost=cost_dict['r'],
                wcost=cost_dict['w'],
                ucost=cost_dict['u'],
                image_path=img_url,
                flv=flavor_text,
                lowerflv=flavor_text.lower())

        c.save()

        #this needs to be done properly ...
        #if we ever launch :p
        print "retriving image from url ..."
        f = open('static/cards/%s.jpg' %cname,'wb')
        f.write(urllib.urlopen(img_url).read())
        f.close()
       
        print "done downloading image ..."
        #print "saving image to mongodb ..."

        """file_location = pipes.quote("cards/%s" %cname)
        print "debug-----"
        print file_location
        print "------"
        print ("mongofiles -d XMTG put %s" %file_location)
        save_process = subprocess.Popen("mongofiles -d XMTG put %s" %file_location, stdout=subprocess.PIPE)
        save_process.communicate()[0]
        """

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
    (r"/api/searchCards", SearchCardHandler),
    (r"/static/*", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)


if __name__ == "__main__":
        print "XMTG listening on 8888"
        connect('XMTG')
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

