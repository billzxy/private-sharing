import pymysql
import os



def getConfig():
    values = []
    with open( os.path.join(os.path.dirname(__file__), "dbconfig.txt") )as f:
        for line in f:
            values.append(line.rstrip())
    f.close()
    return values

def getConnection():
    values = getConfig()
    return pymysql.connect(host='localhost',
                       user=values[0],		#change database username here
                       password=values[1], #Change your password here
                       db=values[2], #Change the local server database here
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
def getLocalFolder():
    values = getConfig()
    return values[3]