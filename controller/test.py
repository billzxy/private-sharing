import pymysql.cursors

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='billzxy', #
                       db='aliyuncrm',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
	
query = 'SELECT * FROM customer'
cursor.execute(query)
	#stores the results in a variable	
data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
cursor.close()
print(data)