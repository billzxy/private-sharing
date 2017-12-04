from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
import dbconfig

feed = Blueprint('feed', __name__)
conn = dbconfig.getConnection()

@feed.route('/feed')
def feed():
	try:
		username = session['username']
		return render_template('feed.html', username=username)
	except:
		return redirect('/')
