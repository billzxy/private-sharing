from flask import Flask, render_template, request, session, url_for, redirect,jsonify, Blueprint
import dbconfig
from feed import encodeThumbnail
from pymysql import MySQLError

notification = Blueprint('notification_blueprint', __name__)

@notification.route("/getTagMsgCount",methods=["POST"])
@notification.route("/content/getTagMsgCount",methods=["POST"])
@notification.route("/group/getTagMsgCount",methods=["POST"])
def countTagMsg():
    pass

@notification.route("/getGroupMsgCount",methods=["POST"])
@notification.route("/content/getGroupMsgCount",methods=["POST"])
@notification.route("/group/getGroupMsgCount",methods=["POST"])
def countGroupMsg():
    pass