from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
import dbconfig
from pymysql import MySQLError

notification = Blueprint('notification_blueprint', __name__)


@notification.route("/getTagMsgCount",methods=["POST"])
@notification.route("/content/getTagMsgCount",methods=["POST"])
@notification.route("/group/getTagMsgCount",methods=["POST"])
@notification.route("/notifications/getTagMsgCount",methods=["POST"])
def countTagMsg():
    content = request.get_json(silent=True)
    username = content['username']

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) as count FROM tag WHERE username_taggee = %s AND status=0;'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if (data):
        return jsonify({"count": data["count"]})
    else:
        return jsonify({"error": True})


@notification.route("/getTagMessage",methods=["POST"])
@notification.route("/content/getTagMessage",methods=["POST"])
@notification.route("/group/getTagMessage",methods=["POST"])
@notification.route("/notifications/getTagMessage",methods=["POST"])
def getTagMessages():
    content = request.get_json(silent=True)
    username = content['username']

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT id, username_tagger AS tagger, username_taggee AS taggee FROM tag WHERE username_taggee = %s AND status=0;'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if (data):
        return jsonify({"error": None, "data": data})
    else:
        return jsonify({"error": "You have no notification!"})


@notification.route("/acceptTag",methods=["POST"])
@notification.route("/content/acceptTag",methods=["POST"])
@notification.route("/group/acceptTag",methods=["POST"])
@notification.route("/notifications/acceptTag",methods=["POST"])
def acceptTag():
    content = request.get_json(silent=True)
    taggee = content["taggee"]
    params = content["tid"].split("--")
    tagger = params[1]
    cid = params[2]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = "UPDATE tag SET status=1 WHERE id=%s AND username_taggee=%s AND username_tagger=%s;"
    try:
        cursor.execute(query, (int(cid), taggee, tagger))
        cursor.close()
        conn.commit()
        response = {"error": None}
        return jsonify(response)

    except MySQLError:
        cursor.close()
        return jsonify({"error": "Adding comment failed, please try again!"})

    finally:
        conn.close()

@notification.route("/declineTag", methods=["POST"])
@notification.route("/content/declineTag", methods=["POST"])
@notification.route("/group/declineTag", methods=["POST"])
@notification.route("/notifications/declineTag", methods=["POST"])
def declineTag():
    content = request.get_json(silent=True)
    taggee = content["taggee"]
    params = content["tid"].split("--")
    tagger = params[1]
    cid = params[2]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = "DELETE FROM tag WHERE id=%s AND username_taggee=%s AND username_tagger=%s AND status=0;"
    try:
        cursor.execute(query, (int(cid), taggee, tagger))
        cursor.close()
        conn.commit()
        response = {"error": None}
        return jsonify(response)

    except MySQLError:
        cursor.close()
        return jsonify({"error": "Adding comment failed, please try again!"})

    finally:
        conn.close()
