
import sqlite3
import os

PROJECT_DIR = os.path.expanduser("~/lsmms")
DATABASE_FILE = os.path.join(PROJECT_DIR, "lsmms.db")


def create_table():
    conn = sqlite3.connect(DATABASE_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monitoring_type TEXT NOT NULL,
            output TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_log(monitoring_type, output):
    conn = sqlite3.connect(DATABASE_FILE)

    conn.execute(
        "INSERT INTO monitoring_logs (monitoring_type, output) VALUES (?, ?)",
        (monitoring_type, output)
    )

    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect(DATABASE_FILE)

    cursor = conn.execute(
        "SELECT id, monitoring_type, output, datetime(created_at, 'localtime') "
        "FROM monitoring_logs ORDER BY id DESC"
    )

    logs = cursor.fetchall()
    conn.close()

    return logs


if __name__ == "__main__":
    create_table()
    print("Database created and table is ready.")
    print("Database location:", DATABASE_FILE)
