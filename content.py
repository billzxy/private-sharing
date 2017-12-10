from flask import render_template, request, session, url_for, redirect,jsonify, Blueprint,current_app
import dbconfig
from pymysql import MySQLError

content = Blueprint('content_blueprint', __name__)


@content.route("/content/<iD>")
def redirectContent(iD):
    try:
        username = session['username']
    except:
        return redirect('/')
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM content WHERE id=%s'
    cursor.execute(query,(int(iD)))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    owner = data['username']
    time = data['timest']
    filepath = data["file_path"]
    contentname = data["content_name"]
    return render_template('contentdetail.html', cid=iD,owner=owner,timest=time,path=lstripDirPath(filepath),contentname=contentname,username=username)


@content.route("/content/getComments",methods=["POST"])
def getComments():
    content = request.get_json(silent=True)
    cid = content["cid"]
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM comment WHERE id=%s'

    cursor.execute(query, (cid))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if(data):
        response = {"error": None, "data": data}
        return jsonify(response)
    else:
        return jsonify({"error": "No comments yet! Say something!"})


@content.route("/content/postComment",methods=["POST"])
def postComment():
    content = request.get_json(silent=True)
    username = content["username"]
    comment_text = content["comment_text"]
    cid = content["cid"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = "INSERT INTO comment (id, username, comment_text) VALUES(%s, %s, %s)"
    try:
        cursor.execute(query, (cid,username,comment_text))
        cursor.close()
        conn.commit()
        response = {"error": None}
        return jsonify(response)

    except MySQLError:
        cursor.close()
        return jsonify({"error": "Adding comment failed, please try again!"})

    finally:
        conn.close()


def lstripDirPath(path):
    return path.lstrip(current_app.config['UPLOAD_FOLDER']+"\\")