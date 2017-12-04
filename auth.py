from flask import request, session, redirect,jsonify, Blueprint
import dbconfig

from password import hashPassword

auth = Blueprint('auth', __name__)
conn = dbconfig.getConnection()

@auth.route('/loginAuth', methods=['POST'])
def loginAuth():
    content = request.get_json(silent=True)
    username = content['name']
    password = hashPassword(content['pass'])

    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()

    if (data):
        session['username'] = username
        return jsonify("ok")
    else:
        return jsonify({"error": "Invalid login or username"})

@auth.route('/registerAuth', methods=['POST'])
def registerAuth():
    content = request.get_json(silent=True)
    username = content['name']
    password = hashPassword(content['pass'])
    firstname = content['fname']
    lastname = content['lname']

    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if (data):
        return jsonify({"error": "This user name already exists, please choose a different one!"})
    else:

        ins = 'INSERT INTO person VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstname, lastname))
        conn.commit()
        cursor.close()
        session['username'] = username
        return jsonify("ok")

@auth.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
