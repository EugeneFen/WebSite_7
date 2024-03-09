from app import app
# import constants
import sqlite3
from flask import render_template, request
from models.users_get import *

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect("ToDoYou.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT credit_card_number, name FROM user
    """)

    list_user = cur.fetchall()
    return render_template(
        'index.html',
        users_list=list_user,
        len=len)

    # list_user = get_all_user(conn)
    # return render_template(
    #     'index.html',
    #     users_list=list_user,
    #     len=len)