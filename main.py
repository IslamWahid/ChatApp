#! /usr/bin/python3
from tornado import web,ioloop
from handlers.socket import WSHandler

class MainHandler(web.RequestHandler):
    def get(self):
        self.render("./templates/index.html")

app = web.Application([
		(r"/", MainHandler),
        (r"/ws", WSHandler)
        ],static_path='static',debug=True)

app.listen(8888)
ioloop.IOLoop.current().start()
