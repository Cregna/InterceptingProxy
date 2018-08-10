class Request(object):
    def __init__(self, id, command, host, path, request_version, header, query, cookie, body):
        self.id = id
        self.command = command
        self.host = host
        self.path = path
        self.request_version = request_version
        self.header = header
        self.query = query
        self.cookie = cookie
        self.body = body

#    def print_req(self):
#        print("\nREQUEST number:" + str(self.id) + '\n' + str(self.command) + " " + str(self.path) + " " + (self.request_version) + "\n\nHEADER\n\n" + str(self.header) + "\n\nQUERY-PARAMETER \n\n" + self.query + "\n\nCOOKIE\n\n" + self.cookie + "\n#\nBODY REQUEST\n\n"+ self.body)

    def __str__(self):
        return  str(self.command) + " " + str(self.path)+ " " + str(self.request_version) + '\r\n' + str(self.header) + '\r\n' + str(self.body) + '\r\n'
