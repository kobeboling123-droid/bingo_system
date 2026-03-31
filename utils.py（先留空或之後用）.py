from flask import Blueprint, jsonify
import sqlite3
import json
from config import DB_NAME

api_bp = Blueprint("api", __name__)


def 解析號碼(號碼):
    """把 DB 字串還原成 list"""
    try:
        if isinstance(號碼, str):
            return json.loads(號碼)
    except:
        pass
    return 號碼


@api_bp.route("/data")
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM bingo
    ORDER BY 期別 DESC
    LIMIT 100
    """)

    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "期別": r[0],
            "時間": r[1],
            "號碼": 解析號碼(r[2]),
            "大小": r[3],
            "單雙": r[4]
        })

    return jsonify(data)