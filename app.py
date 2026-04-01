from flask import Flask, render_template
import sqlite3
import json

from config import DB_PATH
from database import 初始化資料庫
from scheduler import 啟動排程

app = Flask(__name__)


def 解析(x):
    try:
        return json.loads(x)
    except:
        return []


@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 【核心修正 1】SQL 查詢加入「超級獎號」欄位 (第 4 個位置)
    cur.execute("""
        SELECT 期別, 開獎時間, 號碼, 超級獎號, 大小, 單雙
        FROM bingo
        ORDER BY 期別 DESC
        LIMIT 204
    """)

    rows = cur.fetchall()
    conn.close()

    data = []
    for r in rows:
        # 【核心修正 2】時間格式化：只取 HH:MM (例如 14:30)
        # 處理格式如 "2026-04-01 14:30:00" 的字串
        raw_time = r[1] or ""
        time_str = raw_time.split(" ")[1][:5] if " " in raw_time else raw_time

        data.append({
            "期別": r[0],
            "時間": time_str,
            "號碼": 解析(r[2]),
            "超級獎號": r[3], # <--- 這裡也要同步讀取並傳給前端
            "大小": r[4],
            "單雙": r[5]
        })

    print(f"DEBUG: 最新期別 {data[0]['期別']}, 超級獎號 {data[0]['超級獎號']}")

    return render_template("index.html", history=data, latest=data[0] if data else None)



def 抓取最新開獎():
    print("🔥 crawler 被觸發了")

if __name__ == "__main__":
    初始化資料庫()
    啟動排程()

    app.run(debug=False, use_reloader=False)