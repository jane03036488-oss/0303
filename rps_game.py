import random

CHOICES = ("剪刀", "石頭", "布")

ALIAS_MAP = {
    "1": "剪刀",
    "剪刀": "剪刀",
    "s": "剪刀",
    "scissors": "剪刀",
    "2": "石頭",
    "石頭": "石頭",
    "r": "石頭",
    "rock": "石頭",
    "3": "布",
    "布": "布",
    "p": "布",
    "paper": "布",
}

# key 贏 value
BEATS = {
    "剪刀": "布",
    "石頭": "剪刀",
    "布": "石頭",
}


def normalize_choice(raw: str) -> str | None:
    """將使用者輸入轉為標準手勢（剪刀／石頭／布），無效輸入回傳 None。"""
    cleaned = raw.strip().lower()
    return ALIAS_MAP.get(cleaned)


def judge_round(player: str, computer: str) -> str:
    """判定單局結果，回傳 'win'、'lose' 或 'tie'。"""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "win"
    return "lose"


def print_summary(stats: dict, history: list[str]) -> None:
    """顯示最終對戰統計與最近紀錄。"""
    total = stats["win"] + stats["lose"] + stats["tie"]
    win_rate = (stats["win"] / total * 100) if total > 0 else 0.0

    print("\n" + "=" * 42)
    print("📊 猜拳對戰結算報表")
    print("=" * 42)
    print(f"總場次：{total} 場")
    print(f"勝場：{stats['win']} | 敗場：{stats['lose']} | 平手：{stats['tie']}")
    print(f"勝率：{win_rate:.1f}% | 最高連勝：{stats['best_streak']} 連勝")
    print(
        "出拳分佈："
        f"剪刀 {stats['picks']['剪刀']} 次、"
        f"石頭 {stats['picks']['石頭']} 次、"
        f"布 {stats['picks']['布']} 次"
    )

    if history:
        print("-" * 42)
        print("最近對戰紀錄：")
        for line in history[-5:]:
            print(f"  * {line}")
    print("=" * 42 + "\n")


def main() -> None:
    """主程式進入點。"""
    stats = {
        "win": 0,
        "lose": 0,
        "tie": 0,
        "streak": 0,
        "best_streak": 0,
        "picks": {"剪刀": 0, "石頭": 0, "布": 0},
    }
    history: list[str] = []

    print("歡迎來到【猜拳對戰與勝率統計小遊戲】！")
    print("出拳方式：輸入 1/剪刀/s、2/石頭/r、3/布/p；輸入 q 或 離開 可結束遊戲。\n")

    while True:
        user_input = input("請出拳：").strip()
        if user_input.lower() in ("q", "quit", "exit", "離開"):
            break

        player_move = normalize_choice(user_input)
        if player_move is None:
            print("⚠️ 無效輸入，請輸入 1(剪刀)、2(石頭)、3(布)，或輸入 q 離開。\n")
            continue

        computer_move = random.choice(CHOICES)
        stats["picks"][player_move] += 1

        result = judge_round(player_move, computer_move)
        if result == "win":
            stats["win"] += 1
            stats["streak"] += 1
            if stats["streak"] > stats["best_streak"]:
                stats["best_streak"] = stats["streak"]
            outcome_text = "🎉 你贏了！"
        elif result == "lose":
            stats["lose"] += 1
            stats["streak"] = 0
            outcome_text = "😅 電腦贏了！"
        else:
            stats["tie"] += 1
            stats["streak"] = 0
            outcome_text = "🤝 平手！"

        round_num = stats["win"] + stats["lose"] + stats["tie"]
        record_line = f"第 {round_num} 局：你出【{player_move}】vs 電腦【{computer_move}】→ {outcome_text}"
        history.append(record_line)
        print(f"{record_line}（目前連勝：{stats['streak']}）\n")

    print_summary(stats, history)
    print("感謝遊玩，下次再來挑戰！👋")


if __name__ == "__main__":
    main()