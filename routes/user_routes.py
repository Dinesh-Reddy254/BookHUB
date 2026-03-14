from flask import Blueprint, request, jsonify
from database import db, cursor

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():

    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]

    query = "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
    cursor.execute(query,(name,email,password))
    db.commit()

    return jsonify({"message":"User registered successfully"})


@user_bp.route("/users", methods=["GET"])
def get_users():

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return jsonify(users)

@user_bp.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data["email"]
    password = data["password"]

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query,(email,password))

    user = cursor.fetchone()

    if user:
        return jsonify({
            "message":"Login successful",
            "user": user
        })
    else:
        return jsonify({
            "error":"Invalid email or password"
        }),401