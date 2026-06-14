import sqlite3

conn = sqlite3.connect("chat_history")
cursor = conn.cursor()
# cursor.execute(    "insert into history (role,message,time) values('user',' hello GURU','2026-06-15 10:00')")
# cursor.execute("delete  from history where message='GURU'")
cursor.execute("update history  set role='Raghava' where role='user'")
cursor.execute("select * from history")
print(cursor.fetchall())

conn.commit()
conn.close()
