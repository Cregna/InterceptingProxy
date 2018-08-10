class Response(object):
    def __init__(self, id,  version, status, reason, header, set_cookie, body):
        self.id = id
        self.version = version
        self.status = status
        self.reason = reason
        self.header = header
        self.set_cookie = set_cookie
        self.body = body

#    def print_res(self):
#        print("\nRESPONSE number: " + str(self.id) + '\n' + str(self.version) + " " + str(self.status) + " " + str(self.reason) + "\nHEADER\n" + str(self.header) + "\n\nSET-COOKIE\n" + str(self.set_cookie) + "\nRESPONSE BODY\n" + str(self.body))

    def __str__(self):
        return str(self.version) + ' ' + str(self.status) + ' ' + str(self.reason) + "\r\n" + str(self.header) + '\r\n' + str(self.body)

