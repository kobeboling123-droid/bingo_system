import requests
import urllib3
from config import 最新開獎網址, REQUEST_HEADERS
from database import 寫入資料

# 關閉 SSL 警告（方案一）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def 格式化期別(x):
    return int(str(x)[-6:])


def 抓取最新開獎():
    try:
        res = requests.get(
            最新開獎網址,
            headers=REQUEST_HEADERS,
            timeout=10,
            verify=False
        )
        data = res.json()

        item = data["content"]["lotteryBingoLatestPost"]

        result = {
        "期別": int(str(item.get("drawTerm") or item.get("period"))[-6:]), # 兼容不同欄位名，並統一取後 6 位
        "開獎時間": (item.get("dDate") or item.get("time") or "").replace("T", " "),
        "號碼": item.get("bigShowOrder") or item.get("drawNumbers") or [],
        
        # 【核心修正】兼容 bullEye (最新) 與 bullEyeTop (歷史)
        "超級獎號": item.get("bullEye") or item.get("bullEyeTop") or 0,
        
        # 兼容大小與單雙的欄位
        "大小": item.get("prizeNum", {}).get("highLow") or item.get("bigSmall") or "",
        "單雙": item.get("prizeNum", {}).get("oddEven") or item.get("oddEven") or ""
        }


        寫入資料([result])
        print("✔ crawler 寫入:", result["期別"])

    except Exception as e:
        print("❌ crawler error:", e)