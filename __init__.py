from flask import Flask, render_template, request, session, url_for, redirect,jsonify
import pymysql.cursors

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='billzxy', #
                       db='pricosha',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def main():
	try:
		if(session["username"]):
			return redirect(url_for('feed'))
	except:
		return render_template('main.html')

@app.route('/loginAuth', methods=['POST'])
def loginAuth():
	content = request.get_json(silent=True)
	username = content['name']
	password = content['pass']

	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()

	if(data):
		session['username'] = username
		return jsonify("ok")
	else:
		return jsonify({"error":"Invalid login or username"})
		
@app.route('/registerAuth', methods=['POST'])
def registerAuth():
	content = request.get_json(silent=True)
	username = content['name']
	password = content['pass']
	firstname = content['fname']
	lastname = content['lname']

	cursor = conn.cursor()
	query = 'SELECT * FROM person WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		return jsonify({"error":"This user name already exists, please choose a different one!"})
	else:

		ins = 'INSERT INTO person VALUES(%s, %s, %s, %s)'
		cursor.execute(ins, (username, password, firstname, lastname))
		conn.commit()
		cursor.close()
		session['username']=username
		return jsonify("ok")

@app.route('/feed')
def feed():
	try:
		username = session['username']
		return render_template('feed.html', username=username)
	except:
		return redirect('/')


@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
	app.run('127.0.0.1', 8080, debug = True)
