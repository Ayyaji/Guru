import sqlite3


def save_message(role, message):
    conn = sqlite3.connect("C:\\Users\\user\\Projects\\guru\\Database\\chat_history")
    cursor = conn.cursor()
    cursor.execute(
        "insert into history (role,message,time) values(?,?,datetime('now'))",
        (role, message),
    )
    conn.commit()
    conn.close()


def load_history(limit=20):
    conn = sqlite3.connect("C:\\Users\\user\\Projects\\guru\\Database\\chat_history")
    cursor = conn.cursor()
    cursor.execute("select * from history order by time desc LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]
