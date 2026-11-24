import random

DICE_FACES = (1, 2, 3, 4, 5, 6)


def roll_dice(count: int = 2) -> list[int]:
    """擲出指定數量的六面骰，回傳點數串列。"""
    rolls = []
    for _ in range(count):
        rolls.append(random.randint(DICE_FACES[0], DICE_FACES[-1]))
    return rolls


def play_high_low(stats: dict, history: list[str]) -> None:
    """模式 1：擲兩顆骰子猜點數和較大（H >= 7）或較小（L < 7）。"""
    guess = input("猜總點數較大輸入 'H'（7～12），較小輸入 'L'（2～6）：").strip().upper()
    if guess not in ("H", "L"):
        print("⚠️ 無效的猜測，請輸入 H 或 L。\n")
        return

    dice = roll_dice(2)
    total = sum(dice)
    stats["sum_counts"][total] = stats["sum_counts"].get(total, 0) + 1

    actual = "H" if total >= 7 else "L"
    won = guess == actual

    update_streak_and_result(stats, won)
    outcome_text = "🎉 猜對了，你贏得本局！" if won else "😅 猜錯了，本局落敗！"
    label_map = {"H": "大(>=7)", "L": "小(<7)"}
    line = (
        f"[比大小] 骰子 {dice[0]} + {dice[1]} = {total}（{label_map[actual]}）"
        f"｜你猜 {label_map[guess]} → {outcome_text}"
    )
    history.append(line)
    print(f"{line}（目前連勝：{stats['streak']}）\n")


def play_duel(stats: dict, history: list[str]) -> None:
    """模式 2：玩家與電腦各擲兩顆骰子，比總點數大小。"""
    player_dice = roll_dice(2)
    comp_dice = roll_dice(2)

    player_sum = sum(player_dice)
    comp_sum = sum(comp_dice)
    stats["sum_counts"][player_sum] = stats["sum_counts"].get(player_sum, 0) + 1

    if player_sum > comp_sum:
        update_streak_and_result(stats, True)
        outcome_text = "🎉 你的點數較高，獲勝！"
    elif player_sum < comp_sum:
        update_streak_and_result(stats, False)
        outcome_text = "😅 電腦點數較高，落敗！"
    else:
        stats["tie"] += 1
        stats["streak"] = 0
        outcome_text = "🤝 雙方點數相同，平手！"

    line = (
        f"[雙骰對戰] 你 {player_dice[0]}+{player_dice[1]}={player_sum} "
        f"vs 電腦 {comp_dice[0]}+{comp_dice[1]}={comp_sum} → {outcome_text}"
    )
    history.append(line)
    print(f"{line}（目前連勝：{stats['streak']}）\n")


def update_streak_and_result(stats: dict, won: bool) -> None:
    """更新勝敗場次、目前連勝與最高連勝。"""
    if won:
        stats["win"] += 1
        stats["streak"] += 1
        if stats["streak"] > stats["best_streak"]:
            stats["best_streak"] = stats["streak"]
    else:
        stats["lose"] += 1
        stats["streak"] = 0


def print_summary(stats: dict, history: list[str]) -> None:
    """印出最終戰績結算報表。"""
    total_rounds = stats["win"] + stats["lose"] + stats["tie"]
    win_rate = (stats["win"] / total_rounds * 100) if total_rounds > 0 else 0.0

    print("\n" + "=" * 46)
    print("🎲 幸運骰子挑戰結算報表")
    print("=" * 46)
    print(f"總回合數：{total_rounds} 局")
    print(f"勝場：{stats['win']} | 敗場：{stats['lose']} | 平手：{stats['tie']}")
    print(f"勝率：{win_rate:.1f}% | 最高連勝：{stats['best_streak']} 連勝")

    if history:
        print("-" * 46)
        print("最近對戰紀錄：")
        for item in history[-5:]:
            print(f"  * {item}")
    print("=" * 46 + "\n")


def main() -> None:
    """主程式進入點。"""
    stats = {
        "win": 0,
        "lose": 0,
        "tie": 0,
        "streak": 0,
        "best_streak": 0,
        "sum_counts": {},
    }
    history: list[str] = []

    print("歡迎來到【幸運骰子比大小與連勝挑戰遊戲】！")

    while True:
        print("請選擇玩法：")
        print("1. 雙骰比大小（猜大 H / 猜小 L）")
        print("2. 雙骰對戰（玩家 vs 電腦）")
        print("Q. 結束遊戲並查看戰績")

        choice = input("輸入選項：").strip().upper()
        if choice in ("Q", "QUIT", "EXIT", "離開"):
            break
        if choice == "1":
            play_high_low(stats, history)
        elif choice == "2":
            play_duel(stats, history)
        else:
            print("⚠️ 請輸入 1、2 或 Q 離開。\n")

    print_summary(stats, history)
    print("感謝挑戰，下次再來試試手氣！🎲")


if __name__ == "__main__":
    main()