from flask import Flask,session,jsonify,request
import json
import requests
import sqlite3
from flask_jwt_extended import create_access_token , get_jwt_identity , jwt_required , JWTManager


from scrapping_fncts import get_student_data, get_session , get_student_grades ,create_cookie, get_cookie
from encryption import encrypt, decrypt
import os


app = Flask(__name__)

#import localvariables HHHHH knt mwlf ndirhom plaintext I was like naaah this time this is going to github XDD
secret_key = os.getenv('SECRET_KEY')
api_username = os.getenv('api_user')
api_password = os.getenv('api_password')
app.config["JWT_SECRET_KEY"] = secret_key
app.secret_key = secret_key
jwt = JWTManager(app)


print(api_password , api_username)
@app.route("/login" , methods=["POST"])
def login():
    print("request received")
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user_id = request.json.get("user_id", None)
    if username != api_username or password != api_password:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity={"user_id" : encrypt(user_id)})
    return jsonify(access_token=access_token)


@app.route("/verify_creds" , methods=["POST"])
def verify_creds():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    response , actualsession = get_session(username, password)
    cookietosave = requests.utils.dict_from_cookiejar(actualsession.cookies)
    create_cookie(username,cookietosave)
    return response


@app.route("/get_data" , methods=["POST"])
def get_data():
    username = request.json.get("username", None)
    newsession = requests.Session()
    cookie = get_cookie(username)
    newsession.cookies.update(cookie)
    data = get_student_data(newsession)
    return data

@app.route("/get_grades" , methods=["POST"])
def get_grades():
    username = request.json.get("username", None)
    newsession = requests.Session()
    cookie = get_cookie(username)
    newsession.cookies.update(cookie)
    data = get_student_grades(newsession)
    return data
    
    