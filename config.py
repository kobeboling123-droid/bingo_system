import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bingo.db")
DB_NAME = DB_PATH # api.py uses DB_NAME

最新開獎網址 = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery/LatestBingoResult"
歷史開獎網址 = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult"

每日筆數 = 203
抓取間隔秒數 = 60

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}