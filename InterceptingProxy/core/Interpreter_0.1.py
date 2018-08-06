import readline
import proxy
import threading
import queue

p = proxy.Proxy()


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

def viewreq(number):
    number = int(number)
    reqlist = p.get_req()
    if number > len(reqlist):
        print('Wrong ID number')
    else:
        print(reqlist[number-1].print_req())



def viewres(number):
    number = int(number)
    reslist = p.get_res()
    if number > len(reslist):
        print('Wrong ID number')
    else:
        print(reslist[number-1].print_res())


mydict = {
    "exit": exitprogram,
    "help": help,
    "ls": ls,
    "lsr": lsr,
    "printres": printres
}

mydict2 = {
    'viewreq': viewreq,
    'viewres': viewres
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
                    print('too much argument')
        for key2 in mydict2:
            if command[0] == key2:
                if len(command) == 2:
                    mydict2[command[0]](command[1])
                    found = True
                else:
                    print('Too much Argument')
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
    t = threading.Thread(target=sproxy)
    t2 = threading.Thread(target=inte)

    t2.start()
    t.start()


if __name__ == '__main__':
    main()
