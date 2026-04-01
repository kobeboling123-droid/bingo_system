import requests
import datetime
import time
import urllib3
from database import 寫入資料, get_conn

# 關閉 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# =========================================
# 🎯 單日全量抓取（已整合強化版）
# =========================================
def 抓取單日全量資料(日期字串):

    all_results = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.taiwanlottery.com/",
    }

    # ===== 基準時間（強化版）=====
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 期別, 開獎時間 
        FROM bingo 
        WHERE 開獎時間 LIKE '202%' 
          AND 開獎時間 LIKE '%:%'
        ORDER BY 期別 DESC 
        LIMIT 1
    """)

    base_row = cur.fetchone()
    conn.close()

    today_prefix = int(日期字串.replace("-", "")[2:])
    fallback_term = today_prefix * 1000 + 203
    fallback_time = datetime.datetime.strptime(f"{日期字串} 23:55", "%Y-%m-%d %H:%M")

    if base_row:
        base_term = base_row[0]

        try:
            base_time = datetime.datetime.strptime(base_row[1][:16], "%Y-%m-%d %H:%M")

            if base_time.year < 2024:
                raise ValueError

        except:
            base_term = fallback_term
            base_time = fallback_time
    else:
        base_term = fallback_term
        base_time = fallback_time

    # ===== API 抓取 =====
    page_size = 50
    print(f"📅 補資料: {日期字串}")

    for page in range(1, 6):

        url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult?openDate={日期字串}&pageNum={page}&pageSize={page_size}"

        try:
            res = requests.get(url, headers=headers, timeout=15, verify=False)
            data = res.json()
            results = data.get("content", {}).get("bingoQueryResult", [])

            if not results:
                break

            for item in results:
                full_term = str(item["drawTerm"])
                short_term = int(full_term[-6:])

                # ⭐ 時間推算
                term_diff = base_term - short_term
                calculated_time = base_time - datetime.timedelta(minutes=term_diff * 5)
                final_time_str = calculated_time.strftime("%Y-%m-%d %H:%M")

                all_results.append({
                    "期別": short_term,
                    "開獎時間": final_time_str,
                    "號碼": item["bigShowOrder"],
                    "超級獎號": item.get("bullEye") or item.get("bullEyeTop"),
                    "大小": item.get("prizeNum", {}).get("highLow", ""),
                    "單雙": item.get("prizeNum", {}).get("oddEven", "")
                })

            print(f"  ✔ 第 {page} 頁 ({len(results)} 筆)")

            if len(results) < page_size:
                break

            time.sleep(1)

        except Exception as e:
            print(f"  ❌ 第 {page} 頁錯誤: {e}")
            break

    if all_results:
        寫入資料(all_results)
        return len(all_results)

    return 0


# =========================================
# 🚀 補洞主程式（完整版）
# =========================================
def 補洞主程式(目標總數=1016):
    """智慧補洞：先補最新，再往歷史補"""

    today_dt = datetime.datetime.now()
    today = today_dt.strftime("%Y-%m-%d")
    yesterday = (today_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    print("🚀 檢查最新資料...")

    # 🔥 先補最新（很重要）
    抓取單日全量資料(today)
    抓取單日全量資料(yesterday)

    # ===== 找最舊資料 =====
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT MIN(開獎時間) 
            FROM bingo 
            WHERE 開獎時間 > '2000-01-01'
        """)
        res = cur.fetchone()
        oldest_time = res[0] if res else None
    except:
        oldest_time = None
    finally:
        conn.close()

    # ===== 安全轉換 =====
    current_date = today_dt

    if oldest_time and isinstance(oldest_time, str) and len(oldest_time) >= 10:
        try:
            clean_date = oldest_time.split(" ")[0]
            current_date = datetime.datetime.strptime(clean_date, "%Y-%m-%d")

            if current_date.year < 2024:
                current_date = today_dt
        except:
            current_date = today_dt

    # ===== 開始補洞 =====
    added_count = 0
    max_days = 60
    days_processed = 0

    print(f"⏳ 開始補歷史資料 (目標 {目標總數} 筆)")

    while added_count < 目標總數 and days_processed < max_days:

        current_date -= datetime.timedelta(days=1)
        date_str = current_date.strftime("%Y-%m-%d")

        added = 抓取單日全量資料(date_str)

        added_count += added
        days_processed += 1

        time.sleep(1.5)

    print(f"✨ 完成：{days_processed} 天 / {added_count} 筆")


# =========================================
# ▶ 主程式入口
# =========================================
if __name__ == "__main__":
    補洞主程式(1016)