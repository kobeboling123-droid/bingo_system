from flask import Flask
from database import 初始化資料庫
from scheduler import 啟動排程
from api import api_bp

app = Flask(__name__)

初始化資料庫()
啟動排程()

app.register_blueprint(api_bp)

@app.route("/")
def home():
    return "Bingo 系統運行中"