import sqlite3

conn = sqlite3.connect("chat_history")
cursor = conn.cursor()
# cursor.execute("create index locator on history(time)")
cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
print(cursor.fetchall())
conn.commit()
conn.close()
