import sqlite3

con = sqlite3.connect("ToDoYou.db")
cur = con.cursor()

cur.execute("""
SELECT * FROM user
""")
print(cur.fetchall())

cur.execute("""
SELECT * FROM task inner join user using(credit_card_number)
""")
print(cur.fetchall())



# cur.execute("""
# CREATE TABLE IF NOT EXISTS user (
#     credit_card_number INTEGER PRIMARY KEY,
#     name TEXT NOT NULL UNIQUE
# );
# """)
#
# cur.execute("""DROP TABLE task""")
# cur.execute("""
# CREATE TABLE IF NOT EXISTS task (
#     id_task INTEGER PRIMARY KEY,
#     text_task TEXT NOT NULL UNIQUE,
#     status TEXT NOT NULL,
#     credit_card_number INTEGER NOT NULL,
#     FOREIGN KEY (credit_card_number)
#             REFERENCES user (credit_card_number)
#               ON DELETE CASCADE
#               ON UPDATE NO ACTION
# );
# """)

# users_spec = [
#     ('1', 'Иванов Иван Иванович'),
#     ('2', 'Жук Генадий Арсеньевич'),
#     ('3', 'Белякова Валерия Андреевна')]
#
# cur.executemany("INSERT INTO user VALUES(?, ?);", users_spec)
#
# tasks_spec = [
#     ('1', 'Eat', 'Planned', '2'),
#     ('2', 'Go to a shop', 'Planned', '3'),
#     ('3', 'Sleep', 'Done', '2')]
#
# cur.executemany("INSERT INTO task VALUES(?, ?, ?, ?);", tasks_spec)

con.commit()
con.close()