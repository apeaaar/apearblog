from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from app import fapp
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler,Application



class RedirectHandler(RequestHandler):
    """http转https"""
    def prepare(self):
        self.redirect(url='https://' + self.request.host + self.request.uri)
        remote_ip = self.request.remote_ip
        print(remote_ip)

application = HTTPServer(WSGIContainer(fapp))
https_cert_file = "cert/cert.pem"
https_key_file = "cert/cert.key"
server = HTTPServer(application,ssl_options={"certfile":https_cert_file,"keyfile":https_key_file})
server.listen(443)
http_server = Application([(r".*", RedirectHandler)])
http_server.listen(80)  # 监听80端口
print(r"start server......    启动服务......")
IOLoop.instance().start()
