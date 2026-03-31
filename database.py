import sqlite3
import json
from config import DB_NAME


def 初始化資料庫():
    """建立資料表"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bingo (
        期別 INTEGER PRIMARY KEY,
        開獎時間 TEXT,
        號碼 TEXT,
        大小 TEXT,
        單雙 TEXT
    )
    """)

    conn.commit()
    conn.close()


def 寫入資料(資料列表):
    """寫入資料（自動去重）"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for d in 資料列表:

        號碼 = d["號碼"]

        # 如果是 list → 轉 JSON 存
        if isinstance(號碼, list):
            號碼 = json.dumps(號碼, ensure_ascii=False)

        cursor.execute("""
        INSERT OR IGNORE INTO bingo
        (期別, 開獎時間, 號碼, 大小, 單雙)
        VALUES (?, ?, ?, ?, ?)
        """, (
            int(d["期別"]),
            d["開獎時間"],
            號碼,
            d["大小"],
            d["單雙"]
        ))

    conn.commit()
    conn.close()


def 取得所有資料():
    """取得全部資料"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 期別, 開獎時間, 號碼, 大小, 單雙 FROM bingo ORDER BY 期別 ASC")
    rows = cursor.fetchall()

    conn.close()

    return rows


def 取得最近N期(n=50):
    """取得最近 N 期"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 期別, 開獎時間, 號碼, 大小, 單雙
    FROM bingo
    ORDER BY 期別 DESC
    LIMIT ?
    """, (n,))

    rows = cursor.fetchall()
    conn.close()

    return list(reversed(rows))