import sqlite3
import os
import getpass

class Database(object):
    conn = None
    querycreatetable1 = '''
    CREATE TABLE "Request" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`method`	TEXT NOT NULL,
	`host`	TEXT NOT NULL,
	`path`	TEXT NOT NULL,
	`http_version`	TEXT NOT NULL,
	`headers`	TEXT NOT NULL,
	`body`	TEXT
)
    '''

    querycreatetable2 = '''
    CREATE TABLE "Response" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`http_version`	TEXT NOT NULL,
	`status`	TEXT NOT NULL,
	`reason`	TEXT NOT NULL,
	`headers`	TEXT NOT NULL,
	`body`	TEXT
) 
    '''
    querycreatetable3 = '''
    CREATE TABLE "HTTPTransaction" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`id_request`	INTEGER UNIQUE,
	`id_response`	INTEGER UNIQUE,
	FOREIGN KEY(`id_request`) REFERENCES 'Request' ( 'id' ) ON DELETE SET NULL,
	FOREIGN KEY(`id_response`) REFERENCES 'Response'('id') ON DELETE SET NULL
)
    '''
    username = getpass.getuser()
    namefile = 'purp.sqlite'
    default_path = '/home/'+username+'/.purp/purp.sqlite'

    exist = False

    def __init__(self, path = '/home/'+username+'/.purp/'):
        self.verifydir(path)
        self.fullpath = path + self.namefile
        self.exist =  os.path.isfile(self.fullpath)


    def verifydir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def existing(self):
        self.exist = os.path.isfile(self.fullpath)


    def insertrequest(self,request):
        self.existing()
        if self.exist is True:
            try:
                with sqlite3.connect(self.fullpath) as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO Request (method, host , path, http_version, headers, body) VALUES (?, ?, ?, ?, ?, ?)',
                                (request[0], request[1], request[2], request[3], request[4], request[5] ))
                    #cur.commit()
            except Exception as e:
                print(e)
        if self.exist is False:
            try:
                with sqlite3.connect(self.fullpath) as con:
                    cur = con.cursor()
                    cur.execute(self.querycreatetable1)
                    cur.execute(self.querycreatetable2)
                    cur.execute(self.querycreatetable3)
                    cur.execute(
                        'INSERT INTO Request (method, host , path, http_version, headers, body) VALUES (?, ?, ?, ?, ?, ?)',
                        (request[0], request[1], request[2], request[3], request[4], request[5]))
                    #cur.commit()
            except Exception as e:
                print(e)

    def insertresponse(self, response):
        self.existing()
        if self.exist is True:
            try:
                with sqlite3.connect(self.fullpath) as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO Response (http_version, status, reason, headers, body) VALUES (?, ?, ?, ?, ?)',
                                (response[0], response[1], response[2], response[3], response[4]))
                    #cur.commit()
            except Exception as e:
                print(e)
        if self.exist is False:
            try:
                with sqlite3.connect(self.fullpath) as con:
                    cur = con.cursor()
                    cur.execute(self.querycreatetable1)
                    cur.execute(self.querycreatetable2)
                    cur.execute(self.querycreatetable3)
                    cur.execute(
                        'INSERT INTO Response (http_version, status, reason, headers, body) VALUES (?, ?, ?, ?, ?)',
                        (response[0], response[1], response[2], response[3], response[4]))
                    #cur.commit()
            except Exception as e:
                print(e)

    def inserttrans(self):
        self.existing()
        req = 'Request'
        res = 'Response'
        if self.exist is True:
            try:
                with sqlite3.connect(self.fullpath) as con:
                    cur = con.cursor()
                    cur.execute('select seq from sqlite_sequence where name=?', (req,))
                    id_req =cur.fetchone()[0]
                    cur.execute('select seq from sqlite_sequence where name=?', (res,))
                    id_res = cur.fetchone()[0]
                    cur.execute('INSERT INTO HTTPTransaction (id_request, id_response) VALUES (?, ?)',
                                (id_req, id_res))
                    #cur.commit()
            except Exception as e:
                print(e)
        if self.exist is False:
            try:
                with sqlite3.connect(self.fullpath) as con:
                    cur = con.cursor()
                    cur.execute(self.querycreatetable1)
                    cur.execute(self.querycreatetable2)
                    cur.execute(self.querycreatetable3)
                    cur.execute('select seq from sqlite_sequence where name=?', (req,))
                    id_req = cur.fetchone()[0]
                    cur.execute('select seq from sqlite_sequence where name=?', (res,))
                    id_res = cur.fetchone()[0]
                    cur.execute('INSERT INTO HTTPTransaction (id_request, id_response) VALUES (?, ?)',
                                (id_req, id_res))
                    #cur.commit()
            except Exception as e:
                print(e)