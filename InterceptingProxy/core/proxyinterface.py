from core.proxyhandler import ProxyRequestHandler, ThreadingHTTPServer

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
        self.httpd = self.ServerClass(server_address, self.HandlerClass)
        self.httpd.serve_forever()

    def start_intercept(self):
        self.HandlerClass.mode = 'Intercepting'

    def start_sniffing(self):
        self.HandlerClass.mode = 'Sniffing'

    def get_srequest(self):
        return self.HandlerClass

    def modify(self, request1):
        self.HandlerClass.request = request1
        self.HandlerClass.do_GET(self.HandlerClass, True)

        #self.HandlerClass.request_handler(self, req, req_body)

    def ownmodify(self, request_line, headers):
        req_body, conn = self.HandlerClass.make_ownreq(self, request_line, headers)
        res, res_body, res_body_plain = self.HandlerClass.make_ownres(conn)
        self.print_response(self, res, res_body_plain)

    def close(self):
        self.httpd.shutdown()

    def get_req(self):
        return self.HandlerClass.reqlist

    def get_res(self):
        return self.HandlerClass.reslist

