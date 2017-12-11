from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
from PIL import Image
import base64,os
import dbconfig

feed = Blueprint('feed_blueprint', __name__)


@feed.route('/feed')
def feedRedir():
    try:
        username = session['username']
    except:
        return redirect('/')

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name FROM person WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    fname=data['first_name']
    lname=data['last_name']

    return render_template('feed.html', username=username,fname=fname,lname=lname)


@feed.route("/getPostCount",methods=["POST"])
def getPostCount():
    content = request.get_json(silent=True)
    username = content['username']

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) as count FROM content WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

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
    #TODO: Allow PNG and other formats
    thumbnail = os.path.splitext(path)[0] + ".thumbnail"

    try:
        with open(thumbnail, "rb") as thumb_file:
            th_str = str(base64.b64encode(thumb_file.read()))
            #thumb_file.close()
        return th_str
    except:
        try:
            im = Image.open(path)
            im.thumbnail((275,275), Image.ANTIALIAS)
            im.save(thumbnail, "JPEG")
            with open(thumbnail, "rb") as thumb_file:
                th_str = str(base64.b64encode(thumb_file.read()))
                #thumb_file.close()
            return th_str
        except IOError:
            print("cannot create thumbnail for '%s'" % path)


@feed.route("/getPosts",methods=["POST"])
def getPosts():
    content = request.get_json(silent=True)
    username = content['username']
    offset = int(content['page'])
    show_max = int(content['max'])

    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = ('SELECT c.id AS id, c.username AS username, c.timest AS timest, c.file_path AS file_path, '+
            'c.content_name AS content_name, c.public AS public, p.first_name AS first_name, '+
            'p.last_name AS last_name FROM content c '+
            'INNER JOIN person p ON c.username=p.username '+
            'WHERE c.public=1 ORDER BY id DESC')
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if (data):
        for obj in data:
            img_path = obj['file_path']
            try:
                obj['img'] = encodeThumbnail(img_path).lstrip("b'").rstrip("'")
            except AttributeError:
                obj['img']="noimg"

        response = {"error":None,"data":data}
        return jsonify(response)
    else:
        return jsonify({"error": "Nothing to show! Post something!"})

