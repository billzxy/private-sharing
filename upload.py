from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint,current_app,send_from_directory
from werkzeug.utils import secure_filename
import dbconfig
import os

upload = Blueprint('upload_blueprint', __name__)
conn = dbconfig.getConnection()

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
def upload_content():
    if 'file' not in request.files:
        error = "No file part"
        print(error)
        session["error"] = error
        return redirect("/feed")
    file = request.files['file']
    if file.filename == '':
        error = "No file selected"
        print(error)
        session["error"] = error
        return redirect("/feed")
    if file and allowed_file(file.filename):
        username = session["username"]
        content_name = request.form["contname"]
        sharing = request.form["groupname"]
        params = sharing.split("^^")
        groupname = params[0]

        filename = trim_filename_length(secure_filename(file.filename))
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if(groupname=="public"):
            privacy = 1
            cursor = conn.cursor()
            ins = 'INSERT INTO content (username, file_path, content_name, public)VALUES(%s, %s, %s,%s)'
            cursor.execute(ins, (username, filepath, content_name, int(privacy)))
            conn.commit()
        else:
            privacy=0
            owner = params[1]
            cursor = conn.cursor()
            ins = 'INSERT INTO content (username, file_path, content_name, public) VALUES(%s, %s, %s,%s)'
            sel = "SELECT LAST_INSERT_ID() AS id"
            cursor.execute(ins, (username, filepath, content_name, int(privacy)))
            cursor.execute(sel)
            result = cursor.fetchone()
            id = result['id']
            ins = 'INSERT INTO share VALUES(%s, %s, %s)'
            cursor.execute(ins, (id, groupname, owner))
            conn.commit()

        cursor.close()

        session["error"]=None
        return redirect("/feed")


@upload.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)
