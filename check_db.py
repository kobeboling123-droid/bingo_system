import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "bingo.db")

print("DB位置:", DB)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM bingo")
print("資料筆數:", cur.fetchone()[0])

conn.close()