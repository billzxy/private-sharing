from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
from PIL import Image
import base64,os
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
    query = 'SELECT COUNT(*) as count FROM content WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    conn.commit()
    cursor.close()

    if(data):
        return jsonify({"count":data["count"]})
    else:
        return jsonify({"error":"You have not posted anything yet."})

def encodeThumbnail(path):
    """
    Base64 encode the thumbnail of image
    Check for existence of thumbnail
    Create thumbnail if does not exist
    :param path: path of the image that needs to be thumbnailed
    :return: the base64 string of thumbnail

    """
    thumbnail = os.path.splitext(path)[0] + ".thumbnail"

    try:
        with open(thumbnail, "rb") as thumb_file:
            th_str = str(base64.b64encode(thumb_file.read()))
            thumb_file.close()
            return th_str
    except:
        try:
            im = Image.open(path)
            im.thumbnail((125,125), Image.ANTIALIAS)
            im.save(thumbnail, "JPEG")
            with open(thumbnail, "rb") as thumb_file:
                th_str = str(base64.b64encode(thumb_file.read()))
                thumb_file.close()
                return th_str
        except IOError:
            print("cannot create thumbnail for '%s'" % path)


@feed.route("/getPosts",methods=["POST"])
def getPosts():
    content = request.get_json(silent=True)
    username = content['username']
    offset = int(content['page'])
    show_max = int(content['max'])
    cursor = conn.cursor()
    query = 'SELECT * FROM content WHERE username=%s'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    if (data):
        for obj in data:
            img_path = obj['file_path']
            obj['img'] = encodeThumbnail(img_path).lstrip("b'").rstrip("'")

        response = {"error":None,"data":data}
        return jsonify(response)
    else:
        return jsonify({"error": "Nothing is here!"})
