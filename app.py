from flask import Flask
from api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)

@app.route("/")
def home():
    return "Bingo 系統運行中"

print("準備啟動 Flask")

if __name__ == "__main__":
    print("進入 main")
    app.run(host="0.0.0.0", port=10000)