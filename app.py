from flask import Flask, render_template
from api import api_bp
import sqlite3
import json
from config import DB_NAME

app = Flask(__name__)

app.register_blueprint(api_bp)


def 解析號碼(號碼):
    try:
        if isinstance(號碼, str):
            return json.loads(號碼)
    except:
        pass
    return 號碼


@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM bingo
    ORDER BY 期別 DESC
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

    latest = history[0] if history else {}

    return render_template("index.html", latest=latest, history=history)


print("準備啟動 Flask")

if __name__ == "__main__":
    print("進入 main")
    app.run(host="0.0.0.0", port=10000, debug=True)