from flask import request, session, redirect,jsonify, Blueprint
import dbconfig

from password import hashPassword

auth = Blueprint('auth_blueprint', __name__)


@auth.route('/loginAuth', methods=['POST'])
def loginAuth():
    content = request.get_json(silent=True)
    username = content['name']
    password = hashPassword(content['pass'])
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if (data):
        session['username'] = username
        return jsonify({"username":username})
    else:
        return jsonify({"error": "Invalid login or username"})


@auth.route('/registerAuth', methods=['POST'])
def registerAuth():
    content = request.get_json(silent=True)
    username = content['name']
    password = hashPassword(content['pass'])
    firstname = content['fname']
    lastname = content['lname']
    conn = dbconfig.getConnection()
    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if (data):
        cursor.close()
        conn.close()
        return jsonify({"error": "This user name already exists, please choose a different one!"})
    else:

        ins = 'INSERT INTO person VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstname, lastname))
        conn.commit()
        cursor.close()
        conn.close()
        session['username'] = username
        return jsonify({"username":username})


@auth.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
