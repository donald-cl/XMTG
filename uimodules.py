import tornado.web

class Entry(tornado.web.UIModule):
    def render(self, entry, show_comments=False):
        return self.render_string(
            "main.html", entry=entry, show_comments=show_comments)
