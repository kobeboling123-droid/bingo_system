import requests
from config import 最新開獎網址
from database import 寫入資料


def 抓取最新開獎():
    """抓最新一期"""
    try:
        res = requests.get(最新開獎網址, timeout=5)
        data = res.json()

        item = data["content"]["lotteryBingoLatestPost"]

        result = {
            "期別": item["drawTerm"],
            "開獎時間": item["dDate"],
            "號碼": item["bigShowOrder"],
            "大小": "-",   # 可之後補
            "單雙": "-"
        }

        寫入資料([result])
        print("最新資料寫入成功")

    except Exception as e:
        print("抓最新失敗:", e)