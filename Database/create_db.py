import os
import sqlite3
import sys

sys.path.insert(0, os.path.abspath("C:\\Users\\user\\Projects\\guru"))
conn = sqlite3.connect("chat_history")
cursor = conn.cursor()
cursor = conn.execute(
    "CREATE TABLE IF NOT EXISTS emails ( id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, to_address TEXT,  subject TEXT, body TEXT,  status TEXT, time TEXT, FOREIGN KEY(chat_id) REFERENCES history(id))"
)
cursor.execute("pragma table_info(emails)  ")
rows = cursor.fetchall()
print(rows)
conn.commit()
conn.close()
