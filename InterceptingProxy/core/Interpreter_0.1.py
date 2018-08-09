import readline
import proxy
import threading
import editor
from http.server import BaseHTTPRequestHandler
from io import BytesIO

p = proxy.Proxy()

def with_color(c, s):
    return "\x1b[%dm%s\x1b[0m" % (c, s)


class Mycompleter(object):
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        try:
            return self.matches[state]
        except IndexError:
            return None

class HTTPRequest(BaseHTTPRequestHandler):
    lock = threading.Lock()

    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()


    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


def exitprogram():
    print("Sto uscendo..\n")
    p.close()
    exit()


def help():
    print("\nList of command: ")
    for key in mydict:
        print("-" + key)
    for key in mydict2:
        print('-' + key)


def ls():
    reqlist = p.get_req()
    for x in reqlist:
        x.print_req()


def lsr():
    reslist = p.get_res()
    for x in reslist:
        x.print_res()


def printres():
    reqlist = p.get_req()
    reslist = p.get_res()
    titles = ['ID', 'Method', 'Host', 'path', 'R-Code']
    print('{:<4s}{:<10s}{:<30s}{:<40s}{:<30s}'.format(titles[0], titles[1], titles[2], titles[3], titles[4]))
    for x in range(len(reqlist)):
        lenhost = len(reqlist[x].host) + 8
        path = ((str(reqlist[x].path[lenhost: lenhost + 35]) + '...') if len(reqlist[x].path) - lenhost > 30 else reqlist[x].path[lenhost:])
        print('{:<4}{:<10s}{:<30s}{:<40s}{:<30s}'.format(str(reqlist[x].id), str(reqlist[x].command), str(reqlist[x].host), path, str(reslist[x].status) + ' ' + str(reslist[x].reason)  ))
    print('\n')


def intercept():
    p.start_intercept()


def sniffing():
    p.start_sniffing()


def modify(number):
    number = int(number)
    reqlist = p.get_req()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        strreq = editor.edit(contents= reqlist[number - 1].__str__().encode())
        request = HTTPRequest(strreq)
        p.modify(request)

def requestpost(number):
    number = int(number)
    reqlist = p.get_req()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        p.requestpost(reqlist[number-1])

def printa(val = '10'):
    reqlist = p.get_req()
    reslist = p.get_res()
    titles = ['ID', 'Method', 'Host', 'path', 'R-Code']
    print('{:<4s}{:<10s}{:<30s}{:<40s}{:<30s}'.format(titles[0], titles[1], titles[2], titles[3], titles[4]))
    for x in range(len(reqlist)):
        if x > (len(reqlist)  - int(val) - 1):
            lenhost = len(reqlist[x].host) + 8
            path = ((str(reqlist[x].path[lenhost: lenhost + 35]) + '...') if len(reqlist[x].path) - lenhost > 30 else reqlist[x].path[lenhost:])
            print('{:<4}{:<10s}{:<30s}{:<40s}{:<30s}'.format(str(reqlist[x].id), str(reqlist[x].command),
                                                             str(reqlist[x].host), path,
                                                             str(reslist[x].status) + ' ' + str(reslist[x].reason)))
    print('\n')

def printsingle(number):
    number = int(number)
    reqlist = p.get_req()
    reslist = p.get_res()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        print(with_color(33, reqlist[number - 1].__str__()))
        print(with_color(32, reslist[number -1].__str__()))


mydict = {
    "exit": exitprogram,
    "help": help,
    'p': printa,
}

mydict2 = {
    'i': printsingle,
    'p': printa,
    'm': modify
}


class Interpreter(object):
    def __init__(self, text):
        self.text = text

    def didfunc(self):
        found = False
        for key in mydict:
            command = self.text.split(' ')
            if key == self.text:
                if len(command) == 1:
                    mydict[self.text]()
                    found = True
                else:
                    print('too many argument')
        for key2 in mydict2:
            if command[0] == key2:
                if len(command) == 2:
                    mydict2[command[0]](command[1])
                    found = True
                elif(command[0] != 'p'):
                        print('Too many argument')
        if not found:
            print("Command not found, use help for a list of command")


def sproxy():
    p.start()


def inte():
    while True:
        try:
            text = ""
            completer = Mycompleter(mydict)
            readline.set_completer(completer.complete)
            readline.parse_and_bind("tab: complete")
            text = input('Interpreter > ')
        except KeyboardInterrupt:
            pass
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        interpreter.didfunc()


def main():
    try:
        t = threading.Thread(target=sproxy)
        t2 = threading.Thread(target=inte)
        t.start()
        t2.start()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
