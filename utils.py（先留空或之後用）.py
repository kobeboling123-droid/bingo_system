from flask import Blueprint, jsonify
import sqlite3
from config import DB_NAME

api_bp = Blueprint("api", __name__)


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
            "號碼": r[2],
            "大小": r[3],
            "單雙": r[4]
        })

    return jsonify(data)