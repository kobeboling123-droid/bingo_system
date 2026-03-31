import requests
from database import 取得最近N期, 寫入資料


def 找出缺口(期別列表):
    """找缺失期別"""
    缺口 = []

    for i in range(len(期別列表) - 1):
        a = 期別列表[i]
        b = 期別列表[i + 1]

        if b - a > 1:
            for x in range(a + 1, b):
                缺口.append(x)

    return 缺口


def 補單一期別(期別):
    """補單一缺失資料"""
    try:
        url = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult?pageNum=1&pageSize=100"

        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        items = data["content"]["lottoBingoRes"]

        for item in items:
            if int(item["period"]) == int(期別):

                result = {
                    "期別": int(item["period"]),
                    "開獎時間": item["time"],
                    "號碼": list(map(str, item["drawNumbers"])),
                    "大小": item.get("bigSmall"),
                    "單雙": item.get("oddEven")
                }

                寫入資料([result])
                print("補洞成功:", 期別)
                return

    except Exception as e:
        print("補洞失敗:", e)


def 補洞主程式():
    """補洞主流程"""
    期別資料 = 取得最近N期(200)

    if not 期別資料:
        print("資料庫為空")
        return

    期別列表 = [r[0] for r in 期別資料]

    缺口 = 找出缺口(期別列表)

    print("缺口數:", len(缺口))

    for k in 缺口:
        補單一期別(k)