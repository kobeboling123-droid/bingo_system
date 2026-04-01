import sqlite3
import json
from config import DB_PATH


def get_conn():
    return sqlite3.connect(DB_PATH)


def 初始化資料庫():
    conn = get_conn()
    cur = conn.cursor()

    # 核心修正：新增「超級獎號」欄位 (INTEGER 類型)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bingo (
            期別 INTEGER PRIMARY KEY,
            開獎時間 TEXT,
            號碼 TEXT,
            超級獎號 INTEGER,  -- <--- 關鍵新增：儲存 bullEye 或 bullEyeTop
            大小 TEXT,
            單雙 TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ 資料庫結構已更新，支援超級獎號儲存。")


def 寫入資料(資料列表):
    conn = get_conn()
    cur = conn.cursor()

    for d in 資料列表:
        # 請將原本的這段：
        cur.execute("""
            INSERT INTO bingo (期別, 開獎時間, 號碼, 超級獎號, 大小, 單雙)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(期別) DO UPDATE SET
                開獎時間=excluded.開獎時間,
                號碼=excluded.號碼,
                超級獎號=excluded.超級獎號,
                大小=excluded.大小,
                單雙=excluded.單雙
        """, (
            int(d["期別"]),
            d.get("開獎時間", ""),
            json.dumps(d.get("號碼", []), ensure_ascii=False),
            d.get("超級獎號", 0),  # <--- 新增這一行，對應抓到的超級獎號
            d.get("大小", ""),
            d.get("單雙", "")
        ))


    conn.commit()
    conn.close()


def 取得最近N期(n=50):
    conn = get_conn()
    cur = conn.cursor()
    # 【修正】SQL 加入超級獎號欄位 (位置在第 4 個)
    cur.execute("""
        SELECT 期別, 開獎時間, 號碼, 超級獎號, 大小, 單雙
        FROM bingo ORDER BY 期別 DESC LIMIT ?
    """, (n,))
    rows = cur.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "期別": r[0],
            "時間": r[1],
            "號碼": json.loads(r[2]) if isinstance(r[2], str) else r[2],
            "超級獎號": r[3], # <--- 這裡也要同步讀取
            "大小": r[4],
            "單雙": r[5]
        })
    return results

