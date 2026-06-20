import os
import sqlite3


def save_message(role, message):
    conn = sqlite3.connect("C:\\Users\\user\\Projects\\guru\\Database\\chat_history")
    cursor = conn.cursor()
    cursor.execute(
        "insert into history (role,message,time) values(?,?,datetime('now'))",
        (role, message),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def load_history(limit=20):
    conn = sqlite3.connect("C:\\Users\\user\\Projects\\guru\\Database\\chat_history")
    cursor = conn.cursor()
    cursor.execute("select * from history order by time desc LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def init_db():
    """Creates the directories and the database table if they do not exist."""
    db_dir = "C:\\Users\\user\\Projects\\guru\\Database"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect("C:\\Users\\user\\Projects\\guru\\Database\\chat_history")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            role TEXT,
            message TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    test_history = load_history(limit=1)
    if not test_history:
        save_message("user", "Hello, can I get the history output?")
        save_message(
            "assistant", "Yes! Here is the output from your load_history function."
        )

    print(load_history(limit=50))
