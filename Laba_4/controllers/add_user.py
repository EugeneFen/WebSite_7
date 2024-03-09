from app import app
import sqlite3
from flask import render_template, request, redirect, url_for

@app.route('/user', methods=['post'])
def add_user2():
    conn = sqlite3.connect("ToDoYou.db")
    cur = conn.cursor()
    name_us = request.values.get('user_name')

    cur.execute("INSERT into user (name) VALUES(:name_add)", {"name_add":name_us})

    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route('/user', methods=['get'])
def what():
    return render_template(
        'user.html',
        user_name="",
        len=len)