from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
import base64
import dbconfig

feed = Blueprint('feed_blueprint', __name__)
conn = dbconfig.getConnection()


@feed.route('/feed')
def feedRedir():
    try:
        username = session['username']
        return render_template('feed.html', username=username)
    except:
        return redirect('/')


@feed.route("/getPostCount",methods=["POST"])
def getPostCount():
    content = request.get_json(silent=True)
    username = content['username']

    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM content WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if(data):
        return jsonify({"count":data})
    else:
        return jsonify({"error":"You have not posted anything yet."})

@feed.route("/getPosts",methods=["POST"])
def getPosts():
    content = request.get_json(silent=True)
    username = content['username']
    offset = int(content['page'])
    show_max = int(content['max'])
    cursor = conn.cursor()
    query = 'SELECT * FROM content WHERE username=%s ORDER BY id DESC LIMIT %s,%s'
    cursor.execute(query, (username,int(offset),int(show_max)))
    data = cursor.fetchall()
    if (data):
        img_data = data.values()
        for obj in img_data:
            img_path = obj['file_path']
            with open(img_path, "r") as image_file:
                obj['img'] = base64.b64encode(image_file.read())

        response = {"error":None,"data":img_data}
        return jsonify(response)
    else:
        return jsonify({"error": "Nothing is here!"})
