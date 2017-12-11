from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from datetime import timedelta

from auth import auth
from feed import feed
from upload import upload
from group import group
from contents import contents
from dbconfig import getLocalFolder
from notification import notification

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = getLocalFolder()
app.register_blueprint(auth)
app.register_blueprint(feed)
app.register_blueprint(upload)
app.register_blueprint(group)
app.register_blueprint(contents)
app.register_blueprint(notification)


@app.before_request
def session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)


@app.route('/')
def main():
    try:
        if (session["username"]):
            return redirect('/feed')
    except:
        return render_template('main.html')


app.secret_key = 'private_content_share_project'  # TBD

if __name__ == "__main__":
    app.run('127.0.0.1', 8080, debug=False)
