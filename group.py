from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint, make_response
import dbconfig
from feed import encodeThumbnail
from pymysql import MySQLError

group = Blueprint('group_blueprint', __name__)


@group.route("/groups")
def groupPage():
    try:
        username = session['username']
        return render_template('grouplist.html', username=username)
    except:
        return redirect('/')

@group.route("/getAllGroups",methods=["GET"])
def getAllGroups():
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM friendgroup'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if (data):
        response = {"error":None,"data":data}
        return jsonify(response)
    else:
        return jsonify({"error": "No groups have been created yet!"})


@group.route("/getMyGroups",methods=["POST"])
def getMyGroups():
    content = request.get_json(silent=True)
    username = content['username']

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = ("SELECT * FROM friendgroup"+
            " INNER JOIN member ON friendgroup.username=member.username_creator"+
            " WHERE member.username=%s")
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
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

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM friendgroup WHERE username = %s AND group_name = %s'
    cursor.execute(query, (username,groupname))
    data = cursor.fetchone()
    if (data):
        cursor.close()
        conn.close()
        return jsonify({"error": "This group name already exists, please choose a different one!"})
    else:

        query = ("INSERT INTO friendgroup VALUES(%s, %s, %s)")
        cursor.execute(query, (groupname, username, description))
        query = ("INSERT INTO member VALUES(%s, %s, %s)")
        cursor.execute(query, (username, groupname, username))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"error":None})


@group.route("/group/<group_name>")
def redirectGroupPage(group_name):
    try:
        username = session['username']
    except:
        return redirect('/')
    params = group_name.split("6")
    groupname = params[0]
    owner = params[1]
    return render_template('groupdetail.html', group_name=groupname, owner=owner,username=username)


@group.route("/group/getGroupContents",methods=["POST"])
def getGroupContents():
    content = request.get_json(silent=True)
    username = session['username']
    groupname = content["group_name"]
    owner = content["owner"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = ("Select c.id as id, c.content_name as caption, c.username as owner, c.timest as timestamp, c.file_path as filePath "+
        "From Content c inner join Share s on c.id = s.id "+
        "inner join FriendGroup f on s.group_name = f.group_name AND s.username = f.username "+
        "inner join Member m on f.group_name = m.group_name AND f.username = m.username_creator "+
        "Where m.username = %s AND m.group_name = %s AND m.username_creator = %s")

    cursor.execute(query, (username, groupname, owner))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if(data):
        for obj in data:
            img_path = obj['filePath']
            obj['img'] = encodeThumbnail(img_path).lstrip("b'").rstrip("'")
        response = {"error": None, "data": data}
        return jsonify(response)

    else:
        return jsonify({"error": "No posts exist! Post something!"})


@group.route("/group/getNonMemberPeople",methods=["POST"])
def getNonMembers():
    content = request.get_json(silent=True)
    groupname = content["group_name"]
    owner = content["owner"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = (
    "select username,first_name,last_name "+
    "from Person "+
    "where username not in "+
    "(select m.username "+
    "from Member m inner join FriendGroup f on m.username_creator = f.username AND m.group_name = f.group_name "+
    "AND f.group_name =%s AND f.username = %s)")

    cursor.execute(query, (groupname, owner))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if(data):
        response = {"error": None, "data": data}
        return jsonify(response)
    else:
        return jsonify({"error": "No one exists or everyone has found where they belong to!"})


@group.route("/group/addPersonToGroup",methods=["POST"])
def addMember():
    content = request.get_json(silent=True)
    username = content["addee"].lstrip("user_")
    creator = content["adder"]
    groupname = content["group_name"]

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = "INSERT INTO member (username, group_name, username_creator) VALUES(%s, %s, %s)"
    try:
        cursor.execute(query, (username,groupname,creator))
        cursor.close()
        conn.commit()
        response = {"error": None, "msg":"Successfully added %s to group!"%username}
        return jsonify(response)

    except MySQLError:
        cursor.close()
        return jsonify({"error": "Adding member failed, please try again!"})

    finally:
        conn.close()
