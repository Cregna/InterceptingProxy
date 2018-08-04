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
    print("\n")

def ls():
    reqlist = p.get_req()
    for x in reqlist:
        x.print_req()

def lsr():
    reslist = p.get_res()
    for x in reslist:
        x.print_res()

mydict = {
    "exit": exitprogram,
    "help": help,
    "ls": ls,
    "lsr": lsr
}


class Interpreter(object):
    def __init__(self, text):
        self.text = text

    def didfunc(self):
        found = False
        for key in mydict:
            if key == self.text:
                mydict[self.text]()
                found = True
        if(not found):
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
