import readline
import threading
import editor
from inspect import signature
from colors import red,green,blue,cyan,yellow, bold, white, magenta
from InterceptingProxy.core.proxyinterface import Proxy
import email
import subprocess
import tempfile
import getpass
from InterceptingProxy.core.database import Database

pat = ''

p = Proxy()

banner = """
 ______________
< I'm a purp!!! >
 --------------
        \               ___
         \           .-'   `'.
                    /         \\
                    |         ;
                    |         |           ___.--,
           _.._     |0) ~ (0) |    _.---'`__.-( (_.
    __.--'`_.. '.__.\    '--. \_.-' ,.--'`     `""`
   ( ,.--'`   ',__ /./;   ;, '.__.'`    __
   _`) )  .---.__.' / |   |\   \__..--""  ""--.,_
  `---' .'.''-._.-'`_./  /\ '.  \ _.-~~~````~~~-._`-.__.'
        | |  .' _.-' |  |  \  \  '.               `~---`
         \ \/ .'     \  \   '. '-._)
          \/ /        \  \    `=.__`~-.
          / /\         `) )    / / `"". \\
    , _.-'.'\ \        / /    ( (     / /
     `--~`   ) )    .-'.'      '.'.  | (
            (/`    ( (`          ) )  '-;
             `      '-;         (-'

                """

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

def exitprogram():
    print("Sto uscendo..\n")
    p.close()
    exit()


def help():
    print("""Global commands:
    help                                Print this help menu
    exit                                Exit Purp
    p					Print the last 10 info
    p <option value>			Print the last value info
    i <option value>			Print the value request and response
    m <option value>			Modify the value request and show the response	
	""")

def ls():
    reqlist = p.get_req()
    for x in reqlist:
        x.print_req()

response_code_color = {
    '1': blue,
    '2': green,
    '3': yellow,
    '4': red,
    '5': cyan
}

method_color ={
    "GET": cyan,
    "POST": yellow,
    "HEAD": green,
    "PUT": blue,
    "DELETE": red,
    "CONNECT": yellow,
    "OPTIONS": cyan,
    "TRACE": magenta,
    "CONNECT": white

}

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
        print('{:<4}{:<10s}{:<30s}{:<40s}'.format(str(reqlist[x].id), str(reqlist[x].command), str(reqlist[x].host), path))
        print(response_code_color[str(reslist[x].status[1])]('{:<30s}'.format(str(reslist[x].status) + ' ' + str(reslist[x].reason))))
    print('\n')


def intercept():
    p.start_intercept()


def parse_http(reqtxt):
    request_line, headers_alone = reqtxt.split('\r\n', 1)
    message = email.message_from_string(headers_alone)
    headers = dict(message.items())
    return request_line, headers


def modify(number):
    number = int(number)
    reqlist = p.get_req()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        strreq = editor.edit(contents= reqlist[number - 1].__str__().encode())
        request_line, headers = parse_http(strreq.decode())
        p.ownmodify(request_line, headers)

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
    print(bold('{:<6s}{:<10s}{:<40s}{:<40s}{:<20s}'.format(titles[0], titles[1], titles[2], titles[3], titles[4])))
    for x in range(len(reqlist)):
        if x > (len(reqlist)  - int(val) - 1):
            lenhost = len(reqlist[x].host) + 8
            path = ((str(reqlist[x].path[lenhost: lenhost + 35]) + '...') if len(reqlist[x].path) - lenhost > 30 else reqlist[x].path[lenhost:])
            print('{:<6}'.format(str(reqlist[x].id)), end="")
            print(method_color[str(reqlist[x].command)] ('{:<10s}'.format(str(reqlist[x].command))), end="")
            print('{:<40s}{:<40s}'.format(str(reqlist[x].host), path), end="")
            print(response_code_color[str(reslist[x].status)[0]](
                '{:<20s}'.format(str(reslist[x].status) + ' ' + str(reslist[x].reason))))

    print('\n')

def printsingle(number):
    number = int(number)
    reqlist = p.get_req()
    reslist = p.get_res()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        print(yellow(reqlist[number - 1].__str__()))
        print(green(reslist[number -1].__str__()))

def less(number):
    number = int(number)
    reqlist = p.get_req()
    reslist = p.get_res()
    transaction = reqlist[number - 1].__str__() + reslist[number -1].__str__()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        tmp = tempfile.NamedTemporaryFile()
        filename = tmp.name
        with open(filename, mode='wb') as f:
            f.write(transaction.encode())
        command = 'less ' + filename
        subprocess.call(command, shell=True)


mydict = {
    'less': less,
    "exit": exitprogram,
    "h": help,
    "help": help,
    'p': printa,
    'print': printa,
    'inspect': printsingle,
    'i': printsingle,
    'modify': modify,
    'm': modify
}

mydict2 = {
    'inspect': printsingle,
    'i': printsingle,
    'print': printa,
    'p': printa,
    'modify': modify,
    'm': modify,
    'less': less
}


class Interpreter(object):
    def __init__(self, text):
        self.text = text

    def didfunc(self):
        found = False
        for key in mydict:
            command = self.text.split(' ')
            if key == command[0]:
                sig = signature(mydict[command[0]])
                params = sig.parameters
                if command[0] == key:
                    if (command[0] == 'p' or command[0] == 'print'):
                        if len(command) == 1:
                            mydict[command[0]]()
                        else:
                            mydict[command[0]](command[1])
                    elif len(params) == len(command) -1:
                        if len(params) == 0:
                            mydict[command[0]]()
                        else:
                            mydict[command[0]](command[1])
                    found = True
                else:
                    print('Error')
        if not found:
            print("Command not found, use help for a list of command")

def setpath():
    global pat
    if pat == 'default':
        username = getpass.getuser()
        namefile = 'purp.sqlite'
        path = '/home/'+username+'/.purp/purp.sqlite'
        p.setpath(path)
    if pat != 'default':
        p.setpath(pat)

def sproxy():
    p.start()


def inte():
    print(bold(banner))
    print('\n***Sniffing mode***\n')
    while True:
        try:
            text = ""
            completer = Mycompleter(mydict)
            readline.set_completer(completer.complete)
            readline.parse_and_bind("tab: complete")
            text = input('>>> ')
        except KeyboardInterrupt:
            pass
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        interpreter.didfunc()


class Starting(object):

    def start(mode = 'sniffing', path = 'default'):
        global pat
        pat = path
        if mode == 'sniffing':
            try:
                t = threading.Thread(target=sproxy)
                t2 = threading.Thread(target=inte)
                t.start()
                setpath()
                t2.start()
            except KeyboardInterrupt:
                exit()
        if mode == 'intercepting':
            setpath()
            print(bold(banner))
            print('\n***Intercepting mode***\n')
            print("Waiting for incoming request from browser...")
            t = threading.Thread(target=sproxy)
            t.start()
            intercept()

