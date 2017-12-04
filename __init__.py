from flask import Flask, render_template, request, session, url_for, redirect,jsonify
from datetime import timedelta

from auth import auth
from feed import feed

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(feed)

@app.before_request
def session_timeout():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=20)

@app.route('/')
def main():
	try:
		if(session["username"]):
			return redirect(url_for('feed'))
	except:
		return render_template('main.html')

app.secret_key = 'some key that you will never guess' #TBD

if __name__ == "__main__":
	app.run('127.0.0.1', 8080, debug = True)
