import random
import string

SYMBOLS = tuple("!@#$%^&*()-_=+[]{}")

STRENGTH_LEVELS = (
    (80, "極強 🔒", "密碼長度充足且涵蓋多種字元，安全性高。"),
    (60, "強 🛡️", "安全性良好，若再增加長度或特殊符號會更穩固。"),
    (40, "中等 ⚠️", "建議拉長至 12 字元以上並混合大小寫、數字與符號。"),
    (0, "偏弱 🚨", "容易被猜測或破解，請重新產生更複雜的密碼。"),
)


def build_pools(use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> dict[str, str]:
    """依使用者勾選的類別建置字元池字典。"""
    pools: dict[str, str] = {}
    if use_upper:
        pools["upper"] = string.ascii_uppercase
    if use_lower:
        pools["lower"] = string.ascii_lowercase
    if use_digits:
        pools["digits"] = string.digits
    if use_symbols:
        pools["symbols"] = "".join(SYMBOLS)
    return pools


def generate_single_password(length: int, pools: dict[str, str]) -> str:
    """產生單組符合指定長度與字元類別的密碼。"""
    chars: list[str] = []

    # 確保每個啟用的字元類別至少出現一次
    for pool in pools.values():
        chars.append(random.choice(pool))

    all_chars = "".join(pools.values())
    for _ in range(max(0, length - len(chars))):
        chars.append(random.choice(all_chars))

    random.shuffle(chars)
    return "".join(chars[:length])


def read_yes_no(prompt: str, default: bool = True) -> bool:
    """讀取 y/n 選項，空白時使用預設值。"""
    raw = input(prompt).strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes", "1", "是", "好")


def handle_generate_passwords(history: list[dict]) -> None:
    """引導使用者設定條件並批次產生密碼。"""
    print("\n--- 產生安全密碼 ---")
    raw_len = input("請輸入密碼長度（6 - 64，預設 12）：").strip()
    if not raw_len:
        length = 12
    else:
        try:
            length = int(raw_len)
        except ValueError:
            print("⚠️ 長度必須是整數。\n")
            return

    if length < 6 or length > 64:
        print("⚠️ 密碼長度必須介於 6 到 64 之間。\n")
        return

    use_upper = read_yes_no("包含大寫英文字母 A-Z？（Y/n，預設 Y）：", True)
    use_lower = read_yes_no("包含小寫英文字母 a-z？（Y/n，預設 Y）：", True)
    use_digits = read_yes_no("包含數字 0-9？（Y/n，預設 Y）：", True)
    use_symbols = read_yes_no("包含特殊符號 !@#$...？（Y/n，預設 Y）：", True)

    pools = build_pools(use_upper, use_lower, use_digits, use_symbols)
    if not pools:
        print("⚠️ 至少需要選擇一種字元類型！\n")
        return

    raw_count = input("要產生幾組密碼？（1 - 20，預設 3）：").strip()
    if not raw_count:
        count = 3
    else:
        try:
            count = int(raw_count)
        except ValueError:
            print("⚠️ 組數必須是整數。\n")
            return

    if count < 1 or count > 20:
        print("⚠️ 組數必須介於 1 到 20 之間。\n")
        return

    print("\n✅ 產生的密碼如下：")
    for idx in range(1, count + 1):
        pwd = generate_single_password(length, pools)
        score, label, _ = evaluate_password_strength(pwd)
        history.append({"password": pwd, "label": label, "score": score})
        print(f"  {idx:>2}. {pwd}  （強度：{label}，{score} 分）")
    print()


def evaluate_password_strength(password: str) -> tuple[int, str, str]:
    """評估密碼強度，回傳（分數 0-100, 等級標籤, 建議文字）。"""
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(ch in SYMBOLS or (not ch.isalnum()) for ch in password)

    length_score = min(40, len(password) * 3)
    variety_count = sum([has_upper, has_lower, has_digit, has_symbol])
    variety_score = variety_count * 15

    score = min(100, length_score + variety_score)
    for threshold, label, advice in STRENGTH_LEVELS:
        if score >= threshold:
            return score, label, advice
    return 0, "偏弱 🚨", "建議重新產生密碼。"


def handle_check_strength(history: list[dict]) -> None:
    """讓使用者輸入任一密碼並檢測其強度。"""
    pwd = input("\n請輸入要檢測強度的密碼：").strip()
    if not pwd:
        print("⚠️ 密碼不可為空白。\n")
        return

    score, label, advice = evaluate_password_strength(pwd)
    history.append({"password": pwd, "label": label, "score": score})
    print(f"強度評分：{score} / 100")
    print(f"強度等級：{label}")
    print(f"安全建議：{advice}\n")


def show_history(history: list[dict]) -> None:
    """顯示本次產生的密碼紀錄（支援遮罩或明文顯示）。"""
    print("\n" + "=" * 46)
    print("🔑 本次密碼紀錄")
    print("=" * 46)

    if not history:
        print("目前尚無任何密碼紀錄。")
        print("=" * 46 + "\n")
        return

    reveal = read_yes_no("是否直接顯示完整密碼？（y 顯示明文 / n 遮罩，預設 n）：", False)
    for idx, item in enumerate(history, start=1):
        pwd = item["password"]
        if reveal:
            shown = pwd
        else:
            shown = pwd[:2] + "*" * max(2, len(pwd) - 4) + pwd[-2:] if len(pwd) >= 4 else "*" * len(pwd)
        print(f"{idx:>2}. {shown}｜{item['label']}（{item['score']}分）")
    print("=" * 46 + "\n")


def main() -> None:
    """主程式進入點。"""
    history: list[dict] = []
    print("歡迎使用【安全密碼產生器與強度檢測小幫手】！")

    while True:
        print("請選擇功能：")
        print("1. 產生隨機安全密碼")
        print("2. 檢測現有密碼強度")
        print("3. 查看本次密碼紀錄")
        print("4. 離開程式")

        choice = input("輸入選項（1-4）：").strip()

        if choice == "1":
            handle_generate_passwords(history)
        elif choice == "2":
            handle_check_strength(history)
        elif choice == "3":
            show_history(history)
        elif choice == "4":
            print("感謝使用，祝帳號安全無虞！🔐")
            break
        else:
            print("⚠️ 請輸入 1 到 4 之間的選項。\n")


if __name__ == "__main__":
    main()python3 password_generator.py