from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint,current_app,send_from_directory
from werkzeug.utils import secure_filename
import dbconfig
import os

upload = Blueprint('upload_blueprint', __name__)
conn = dbconfig.getConnection()

UPLOAD_FOLDER = '/Users/bill/PycharmProjects/PrivateContentShare/uploads' #windows config
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
        privacy = 0 #TODO:change
        filename = trim_filename_length(secure_filename(file.filename))
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cursor = conn.cursor()
        ins = 'INSERT INTO content (username, file_path, content_name, public)VALUES(%s, %s, %s,%s)'
        cursor.execute(ins, (username, filepath, filename, int(privacy)))
        conn.commit()
        cursor.close()

        session["error"]=None
        return redirect("/feed")


"""
@upload.route('/uploadContent', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        username = session["username"]
        print(request.form["privacy"])
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return redirect("/feed")
        '''return redirect(url_for('uploaded_file',
                                filename=filename))'''
"""

@upload.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)
