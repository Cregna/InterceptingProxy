from InterceptingProxy.core.proxyhandler import ProxyRequestHandler, ThreadingHTTPServer
import os
import signal
from InterceptingProxy.core.database import Database

class Proxy(object):
    def __init__(self):
        self.HandlerClass = ProxyRequestHandler
        self.ServerClass = ThreadingHTTPServer
        self.protocol = "HTTP/1.1"
        self.httpd = None

    def start(self):
        port = 8080
        server_address = ('localhost', port)
        self.HandlerClass.protocol_version = self.protocol
        try:
            self.httpd = self.ServerClass(server_address, self.HandlerClass)
            self.httpd.serve_forever()
        except OSError:
            print('Port already in use! please kill the process on port 8080\nTry the command "fuser -k 8080/tcp"')
            os.kill(os.getpid(), signal.SIGTERM)

    def q(self):
        return self.HandlerClass.q

    def setpath(self, path):
        self.HandlerClass.pathdb = path

    def start_intercept(self):
        self.HandlerClass.mode = 'Intercepting'

    def start_sniffing(self):
        self.HandlerClass.mode = 'Sniffing'

    def get_srequest(self):
        return self.HandlerClass

    def ownmodify(self, request_line, headers):
        req_body, conn = self.HandlerClass.make_ownreq(self.HandlerClass, request_line, headers)
        res, res_body, res_body_plain = self.HandlerClass.make_ownres(self.HandlerClass, conn)
        self.HandlerClass.print_response(self, res, res_body_plain)

    def close(self):
        self.httpd.shutdown()



    def get_req(self):
        return self.HandlerClass.reqlist

    def get_res(self):
        return self.HandlerClass.reslist



