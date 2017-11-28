import pymysql

def getConnection():
	return pymysql.connect(host='localhost',
                       user='root',		#change database username here 	
                       password='billzxy', #Change your password here
                       db='pricosha', #Change the local server database here 
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)