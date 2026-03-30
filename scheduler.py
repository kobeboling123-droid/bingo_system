from apscheduler.schedulers.background import BackgroundScheduler
from crawler import 抓取最新開獎
from patch_engine import 補洞主程式


def 啟動排程():
    scheduler = BackgroundScheduler()

    # 每2分鐘抓最新
    scheduler.add_job(抓取最新開獎, "interval", minutes=2)

    # 每10分鐘補洞
    scheduler.add_job(補洞主程式, "interval", minutes=10)

    scheduler.start()