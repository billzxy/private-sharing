from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint,current_app
from werkzeug.utils import secure_filename
import dbconfig
import os

upload = Blueprint('upload_blueprint', __name__)
conn = dbconfig.getConnection()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def trim_filename_length(filename):
    l = filename.split(".")
    if(len(l[0])>20):
        l[0] = l[0][0:20]
        return ".".join(l)
    return filename


@upload.route('/uploadContent', methods=['POST'])
def upload_file():
    error = None
    if 'file' not in request.files:
        error = "No file part"
        print(error)
        return render_template("feed.html",error=error)
    file = request.files['file']
    if file.filename == '':
        error = "No file selected"
        print(error)
        return render_template("feed.html",error=error)
    if file and allowed_file(file.filename):
        filename = trim_filename_length(secure_filename(file.filename))
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(filepath)
        file.save(filepath)

        username = session["username"]
        privacy = request.form["privacy"]

        cursor = conn.cursor()
        ins = 'INSERT INTO content VALUES(,%s, NOW(), %s, %s,%i)'
        cursor.execute(ins, (username, filepath, filename, privacy))
        conn.commit()
        cursor.close()
        return render_template("feed.html",error=error)
