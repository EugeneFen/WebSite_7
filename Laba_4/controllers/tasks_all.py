from app import app
import sqlite3
from flask import render_template, request, redirect, url_for, session
from models.tasks_get import *


@app.route('/todo', methods=['get'])
def get_tasks():
    conn = sqlite3.connect("ToDoYou.db")
    cur = conn.cursor()
    user_us = request.values.get('name_us')

    cur.execute(f"SELECT name FROM user WHERE credit_card_number = '{user_us}'")
    name_sql = cur.fetchall()
    if not name_sql:
        raise ValueError("Такого пользователя нет 4XX")

    cur.execute(f"SELECT id_task, text_task, status FROM task WHERE credit_card_number = '{user_us}'")

    list_task = cur.fetchall()
    return render_template(
        'todo.html',
        tasks_list=list_task,
        name_user=name_sql[0][0],
        user_credit=user_us,
        len=len
    )


@app.route('/todo', methods=['post'])
def add_tasks():
    conn = sqlite3.connect("ToDoYou.db")
    cur = conn.cursor()
    text_tasks = request.values.get('task_text')
    status_tasks = request.values.get('task_status')
    credit_tasks = request.values.get('credit')

    cur.execute("""INSERT INTO task(text_task, status, credit_card_number) VALUES(:text_t, :status_t, :credit);""",
                {"text_t": text_tasks, "status_t": status_tasks, "credit": credit_tasks})

    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Типо то что нужно, но оно не будет работать
# @app.route('/todo/<int:task_id>',methods=['DELETE', 'get'])
# def remove_task(task_id):
#     conn = sqlite3.connect("ToDoYou.db")
#     cur = conn.cursor()
#
#     cur.execute("""SELECT * FROM task where id_task = '{task_id}'""")
#     task_text=cur.fetchall()
#     if not task_text:
#         cur.execute("""DELETE FROM task where id_task = '{task_id}'""")
#         message = 'Task removed succesfully\n'
#     else:
#         print('Task not found')
#         message = 'Task not found\n'
#
#     return message
