import sqlite3

connect = sqlite3.connect('patterns.sqlite')
cursor = connect.cursor()

with open('create_db.sql')as database:
    text = database.read()

cursor.executescript(text)
cursor.close()
connect.close()
