import random
from core.data_save import load_data, save_data

# 卡牌配置
CARD_RATE = {
    "普通": 85.0,
    "稀有": 12.0,
    "史诗": 2.5,
    "传说": 0.5
}
CARD_LIST = {
    "普通": ["普通战士A", "普通法师B", "普通弓手C"],
    "稀有": ["稀有骑士", "稀有牧师", "稀有盗贼"],
    "史诗": ["史诗龙人", "史诗精灵王"],
    "传说": ["创世神", "终末魔龙"]
}

def get_one_card(data):
    """单抽，返回卡牌名称、品质"""
    streak = data["legend_streak"]
    legend_rate = CARD_RATE["传说"]

    # 软保底：90抽无传说，传说概率翻倍
    if streak >= 90:
        legend_rate *= 2
    # 硬保底：100抽必出传说
    if streak >= 100:
        quality = "传说"
    else:
        # 加权随机
        total = 100 - CARD_RATE["传说"] + legend_rate
        r = random.uniform(0, total)
        cur = 0
        quality = "普通"
        if r < CARD_RATE["普通"]:
            quality = "普通"
        elif r < CARD_RATE["普通"] + CARD_RATE["稀有"]:
            quality = "稀有"
        elif r < CARD_RATE["普通"] + CARD_RATE["稀有"] + CARD_RATE["史诗"]:
            quality = "史诗"
        else:
            quality = "传说"

    # 随机卡牌
    card_name = random.choice(CARD_LIST[quality])

    # 更新计数
    data["total_draw"] += 1
    data["remain_draw"] -= 1
    data["card_count"][quality] += 1

    if quality == "传说":
        data["legend_streak"] = 0
    else:
        data["legend_streak"] += 1

    # 加入图鉴
    if card_name not in data["collection"]:
        data["collection"].append(card_name)

    save_data(data)
    return card_name, quality

def ten_pull(data):
    """十连，保底至少一张稀有"""
    result = []
    has_rare = False
    for _ in range(10):
        name, qua = get_one_card(data)
        result.append((name, qua))
        if qua in ("稀有", "史诗", "传说"):
            has_rare = True
    # 十连无稀有则重抽最后一张保证稀有保底
    if not has_rare:
        new_name, new_qua = random.choice([(n, "稀有") for n in CARD_LIST["稀有"]])
        result[-1] = (new_name, new_qua)
    save_data(data)
    return result