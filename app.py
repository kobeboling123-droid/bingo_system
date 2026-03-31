from flask import Flask, render_template
import sqlite3
import json
from config import DB_NAME

app = Flask(__name__)


def 解析號碼(號碼):
    if not 號碼:
        return []

    # 🔥 先處理 list
    if isinstance(號碼, list):
        return 號碼

    # 🔥 再處理字串
    if isinstance(號碼, str):
        # 1️⃣ JSON
        try:
            return json.loads(號碼)
        except:
            pass

        # 2️⃣ CSV fallback
        if "," in 號碼:
            try:
                return [int(x) for x in 號碼.split(",") if x.strip()]
            except:
                pass

    return []


@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM bingo
    ORDER BY CAST(期別 AS INTEGER) DESC
    LIMIT 24
    """)

    rows = cursor.fetchall()
    conn.close()

    history = []

    for r in rows:
        history.append({
            "期別": r[0],
            "時間": r[1],
            "號碼": 解析號碼(r[2]),
            "大小": r[3],
            "單雙": r[4]
        })

    latest = history[0] if history else {
        "期別": "-",
        "時間": "-",
        "號碼": [],
        "大小": "-",
        "單雙": "-"
    }

    return render_template("index.html", latest=latest, history=history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)