import logging

import tornado.ioloop
import tornado.web

import raven

import config

logger = logging.getLogger(__name__)

class AppHandler(tornado.web.RequestHandler):

    client = raven.Client(config.SentryDSN)

    def write_error(self, status_code, **kwargs):
        exc = kwargs["exc_info"]
        self.client.captureException(exc)
        self.set_status(500)
        self.finish("Server Error 500")

class MainHandler(AppHandler):
    def get(self):
        self.write("Hello, world")

class ErrorRaiseHandler(AppHandler):
    def get(self, error_name):
        if not error_name:
            raise Exception("Error: Hello, world")
        else:
            raise Exception("%s" % error_name)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/err/([a-z0-9]*)", ErrorRaiseHandler),
], debug=config.DEBUG)

if __name__ == "__main__":
    try:
        protocol, host, port = config.PROTOCOL, config.HOST, config.PORT
        print "Serving... %s://%s:%s" % (protocol, host, port)
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print "<EXIT> - KeyboardInterrupt"
