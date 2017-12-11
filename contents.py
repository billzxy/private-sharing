from flask import render_template, request, session, redirect,jsonify, Blueprint,current_app
import dbconfig
from pymysql import MySQLError

contents = Blueprint('content_blueprint', __name__)


@contents.route("/content/<iD>")
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
    public = data['public']
    return render_template('contentdetail.html', cid=iD,owner=owner,timest=time,path=lstripDirPath(filepath),contentname=contentname,
                           username=username,public=public)


@contents.route("/content/getComments",methods=["POST"])
def getComments():
    content = request.get_json(silent=True)
    cid = content["cid"]
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM comment WHERE id=%s ORDER BY timest DESC'

    cursor.execute(query, (int(cid)))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if(data):
        response = {"error": None, "data": data}
        return jsonify(response)
    else:
        return jsonify({"error": "No comments yet! Say something!"})


@contents.route("/content/postComment",methods=["POST"])
def postComment():
    content = request.get_json(silent=True)
    username = content["username"]
    comment_text = content["comment_text"]
    cid = content["cid"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = "INSERT INTO comment (id, username, comment_text) VALUES(%s, %s, %s)"
    try:
        cursor.execute(query, (int(cid),username,comment_text))
        cursor.close()
        conn.commit()
        response = {"error": None}
        return jsonify(response)

    except MySQLError:
        cursor.close()
        return jsonify({"error": "Adding comment failed, please try again!"})

    finally:
        conn.close()


@contents.route("/content/getTags",methods=["POST"])
def getTags():
    content = request.get_json(silent=True)
    cid = content["cid"]
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = ("SELECT DISTINCT person.first_name AS fname, person.last_name AS lname FROM person "+
            "INNER JOIN tag ON person.username=tag.username_taggee "+
            "WHERE tag.id=%s AND tag.status=1")

    cursor.execute(query, (int(cid)))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if(data):
        response = {"error": None, "data": data}
        return jsonify(response)
    else:
        return jsonify({"error": True})


@contents.route("/content/getUntaggedUsers",methods=["POST"])
def getUntaggedUsers():
    content = request.get_json(silent=True)
    public = content["public"]
    cid = content["cid"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = ""
    if(public=="1" or public==str(1)):
        query = ("SELECT username,first_name,last_name " +
                 "FROM person " +
                 "WHERE username NOT IN( " +
                 "SELECT t.username_taggee FROM tag t " +
                 "WHERE t.id = %s)")
    else:
        query = ("select p.username, p.first_name, p.last_name "+
                "from Content c inner join Share s on c.id = s.id "+
                "inner join FriendGroup f on s.group_name = f.group_name AND s.username = f.username "+
                "inner join Member m on f.username = m.username_creator AND f.group_name = m.group_name "+
                "inner join Person p on m.username = p.username "+
                "where c.id = %s;")

    cursor.execute(query, (int(cid)))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if (data):
        response = {"error": None, "data": data}
        return jsonify(response)
    else:
        return jsonify({"error": "You're the only one existing on this planet!"})


@contents.route("/content/tagPerson",methods=["POST"])
def tagUser():
    content = request.get_json(silent=True)
    taggee = content["taggee"].lstrip("user_")
    tagger = content["tagger"]
    cid = content["cid"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query=str()
    if(taggee==tagger):
        query = "INSERT INTO tag (id, username_tagger, username_taggee, status) VALUES(%s, %s, %s,1)"
    else:
        query = "INSERT INTO tag (id, username_tagger, username_taggee, status) VALUES(%s, %s, %s,0)"

    try:
        cursor.execute(query, (int(cid),tagger, taggee))
        cursor.close()
        conn.commit()
        response = {"error": None, "msg": "Successfully sent tag request to %s!" % taggee}
        return jsonify(response)

    except MySQLError:
        cursor.close()
        return jsonify({"error": "Adding tag failed, please try again!"})

    finally:
        conn.close()


def lstripDirPath(path):
    return path.lstrip(current_app.config['UPLOAD_FOLDER']+"\\")