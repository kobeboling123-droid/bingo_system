import requests
from config import 最新開獎網址
from database import 寫入資料


def 格式化期別(draw_term):
    """只取後六碼（你需求）"""
    return int(str(draw_term)[-6:])


def 格式化號碼(big_show_order):
    """確保是 list[str]"""
    return list(map(str, big_show_order))


def 抓取最新開獎():
    """抓最新一期並寫入資料庫"""
    try:
        res = requests.get(最新開獎網址, timeout=5)
        res.raise_for_status()
        data = res.json()

        item = data["content"]["lotteryBingoLatestPost"]

        result = {
            "期別": 格式化期別(item["drawTerm"]),
            "開獎時間": item["dDate"],
            "號碼": 格式化號碼(item["bigShowOrder"]),
            "大小": None,
            "單雙": None
        }

        寫入資料([result])

        print(f"最新資料寫入成功：期別 {result['期別']}")

    except Exception as e:
        print("抓最新失敗:", e)