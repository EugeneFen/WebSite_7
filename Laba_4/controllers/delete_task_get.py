from app import app
import sqlite3
from flask import render_template, request, redirect, url_for, session


@app.route('/delete_task', methods=['get'])
def get_del_tasks():
    conn = sqlite3.connect("ToDoYou.db")
    cur = conn.cursor()
    user_us = request.values.get('credit_card')

    cur.execute(f"SELECT name FROM user WHERE credit_card_number = '{user_us}'")
    name_sql = cur.fetchall()
    if not name_sql:
        raise ValueError("Такого пользователя нет 4XX")

    cur.execute(f"SELECT id_task, text_task, status FROM task WHERE credit_card_number = '{user_us}'")

    list_task = cur.fetchall()
    return render_template(
        'delete_task.html',
        tasks_list=list_task,
        len=len
    )


@app.route('/delete_task', methods=['post'])
def remove_task():
    conn = sqlite3.connect("ToDoYou.db")
    cur = conn.cursor()
    task_id = request.values.get('task_num')

    cur.execute(f"DELETE FROM task where id_task = '{task_id}'")

    conn.commit()
    return redirect(url_for("index"))
