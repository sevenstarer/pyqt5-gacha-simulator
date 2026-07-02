import json
import os

DATA_PATH = "data/save.json"
DEFAULT_DATA = {
    "total_draw": 0,
    "remain_draw": 1000,
    "legend_streak": 0,  # 连续无传说抽数（保底计数）
    "card_count": {
        "普通": 0,
        "稀有": 0,
        "史诗": 0,
        "传说": 0
    },
    "collection": []  # 已解锁卡牌名
}

# 初始化data文件夹
if not os.path.exists("data"):
    os.mkdir("data")

def load_data():
    if not os.path.exists(DATA_PATH):
        return DEFAULT_DATA.copy()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def reset_all_data():
    save_data(DEFAULT_DATA.copy())