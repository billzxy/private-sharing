from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
import dbconfig

group = Blueprint('group_blueprint', __name__)
conn = dbconfig.getConnection()


@group.route("/groups")
def groupPage():
    try:
        username = session['username']
        return render_template('grouplist.html', username=username)
    except:
        return redirect('/')

@group.route("/getAllGroups",methods=["GET"])
def getAllGroups():
    cursor = conn.cursor()
    query = 'SELECT * FROM friendgroup'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    if (data):
        response = {"error":None,"data":data}
        return jsonify(response)
    else:
        return jsonify({"error": "No groups have been created yet!"})


@group.route("/getMyGroups",methods=["POST"])
def getMyGroups():
    content = request.get_json(silent=True)
    username = content['username']
    cursor = conn.cursor()
    query = ("SELECT * FROM friendgroup"+
            " INNER JOIN member ON friendgroup.username=member.username_creator"+
            " WHERE member.username=%s")
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    if (data):
        response = {"error":None,"data":data}
        return jsonify(response)
    else:
        return jsonify({"error": "You haven't join any group yet!"})

@group.route("/createGroup",methods=["POST"])
def createGroup():
    content = request.get_json(silent=True)
    username = session['username']
    groupname = content["groupname"]
    description = ""
    try:
        description = content["description"]
    except:
        pass
    cursor = conn.cursor()
    query = 'SELECT * FROM friendgroup WHERE username = %s AND group_name = %s'
    cursor.execute(query, (username,groupname))
    data = cursor.fetchone()
    if (data):
        return jsonify({"error": "This group name already exists, please choose a different one!"})
    else:

        query = ("INSERT INTO friendgroup VALUES(%s, %s, %s)")
        cursor.execute(query, (groupname, username, description))
        query = ("INSERT INTO member VALUES(%s, %s, %s)")
        cursor.execute(query, (username, groupname, username))
        conn.commit()
        cursor.close()
        return jsonify({"error":None})

