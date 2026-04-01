from flask import Blueprint, jsonify
import sqlite3
import json
from config import DB_NAME

api_bp = Blueprint("api", __name__)


def 解析號碼(號碼):
    if not 號碼:
        return []

    if isinstance(號碼, list):
        return [int(x) for x in 號碼]

    if isinstance(號碼, str):
        try:
            data = json.loads(號碼)
            return [int(x) for x in data]
        except:
            pass

        if "," in 號碼:
            try:
                return [int(x) for x in 號碼.split(",") if x.strip()]
            except:
                pass

    return []


@api_bp.route("/test")
def test():
    return "OK"


@api_bp.route("/data")
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 期別, 開獎時間, 號碼, 大小, 單雙
        FROM bingo
        ORDER BY CAST(期別 AS INTEGER) DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()
    conn.close()

    data = []

    for r in rows:
        data.append({
            "期別": int(r[0]),
            "時間": r[1],
            "號碼": 解析號碼(r[2]),
            "大小": r[3] or "",
            "單雙": r[4] or ""
        })

    return jsonify({
        "count": len(data),
        "data": data
    })