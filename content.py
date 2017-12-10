from flask import render_template, request, session, url_for, redirect,jsonify, Blueprint,current_app
import dbconfig

content = Blueprint('content_blueprint', __name__)
conn = dbconfig.getConnection()


@content.route("/content/<id>")
def redirectContent(id):
    try:
        username = session['username']
    except:
        return redirect('/')

    cursor = conn.cursor()
    query = 'SELECT * FROM content WHERE id=%s'
    cursor.execute(query,(int(id)))
    data = cursor.fetchone()
    cursor.close()
    owner = data['username']
    time = data['timest']
    filepath = data["file_path"]
    contentname = data["content_name"]
    return render_template('contentdetail.html', owner=owner,timest=time,path=lstripDirPath(filepath),contentname=contentname)


def lstripDirPath(path):
    return path.lstrip(current_app.config['UPLOAD_FOLDER']+"\\")