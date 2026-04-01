from apscheduler.schedulers.background import BackgroundScheduler
from crawler import 抓取最新開獎
from patch_engine import 補洞主程式
import logging

logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()


def 啟動排程():
    logging.info("scheduler start")

    scheduler.add_job(抓取最新開獎, "interval", minutes=2, id="crawler")
    scheduler.add_job(補洞主程式, "interval", minutes=10, id="patch")

    scheduler.start()