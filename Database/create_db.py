import sqlite3

conn = sqlite3.connect("chat_history")
cursor = conn.cursor()
# cursor.execute(    "insert into history (role,message,time) values('user',' hello GURU','2026-06-15 10:00')")
# cursor.execute("delete  from history where message='GURU'")
# cursor.execute("DELETE FROM history")
# cursor.execute("UPDATE history SET role='user' WHERE role='Raghava'")
cursor.execute("select * from history")
print(cursor.fetchall())

conn.commit()
conn.close()
