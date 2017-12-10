import pymysql
import os

VALUES = []

def getConfig():
    if VALUES==[]:
        with open( os.path.join(os.path.dirname(__file__), "dbconfig.txt") )as f:
            for line in f:
                VALUES.append(line.rstrip())
        f.close()

def getConnection():
    getConfig()
    return pymysql.connect(host='localhost',
                       user=VALUES[0],		#change database username here
                       password=VALUES[1], #Change your password here
                       db=VALUES[2], #Change the local server database here
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
def getLocalFolder():
    getConfig()
    return VALUES[3]