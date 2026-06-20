import os
import sqlite3
import sys

sys.path.insert(0, os.path.abspath("C:\\Users\\user\\Projects\\guru"))
conn = sqlite3.connect("Database/chat_history")
cursor = conn.cursor()
cursor.execute("DELETE FROM history")
conn.commit()
conn.close()
