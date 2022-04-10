from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("users.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/users", methods=["GET", "POST"])
def users():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM user")
        users = [
            dict(id=row[0], name=row[1], mail=row[2])
            for row in cursor.fetchall()
        ]
        if users is not None:
            return jsonify(users)

    if request.method == "POST":
        new_name = request.form["name"]
        new_mail= request.form["mail"]

        sql = """INSERT INTO user (name ,mail)
                 VALUES (?, ?)"""
        cursor = cursor.execute(sql, (new_name, new_mail))
        conn.commit()
        return f"User with the id: {cursor.lastrowid} created successfully", 201


@app.route("/user/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_user(id):
    conn = db_connection()
    cursor = conn.cursor()
    user = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM user WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            user = r
        if user is not None:
            return jsonify(user), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE user
                SET name=?,
                    mail=?
                WHERE id=? """

        name = request.form["name"]
        mail = request.form["mail"]

        updated_user = {
            "id": id,
            "name": name,
            "mail": mail,
   
        }
        conn.execute(sql, (name, mail, id))
        conn.commit()
        return jsonify(updated_user)

    if request.method == "DELETE":
        sql = """ DELETE FROM user WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The user with id: {} has been deleted.".format(id), 200


if __name__ == "__main__":
     app.run(host='localhost', port=5000)