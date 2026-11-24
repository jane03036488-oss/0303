def parse_positive_float(prompt: str) -> float | None:
    """讀取並驗證大於 0 的金額字串，輸入無效時回傳 None。"""
    raw = input(prompt).strip()
    try:
        value = float(raw)
        if value <= 0:
            print("⚠️ 金額必須大於 0，請重新輸入。")
            return None
        return round(value, 2)
    except ValueError:
        print("⚠️ 輸入格式錯誤，請輸入數字（例如：120 或 85.5）。")
        return None


def add_expense(records: list[dict], budget: float) -> None:
    """新增一筆支出紀錄並檢查預算狀態。"""
    category = input("請輸入支出類別（例如：餐飲、交通、娛樂、學習）：").strip().lower()
    if not category:
        category = "其他"

    amount = parse_positive_float("請輸入支出金額（元）：")
    if amount is None:
        return

    note = input("請輸入備註（可留白）：").strip()
    if not note:
        note = "無備註"

    record = {
        "category": category,
        "amount": amount,
        "note": note,
    }
    records.append(record)

    total_spent = sum(item["amount"] for item in records)
    remaining = budget - total_spent

    print(f"✅ 已新增紀錄：[{category}] ${amount:.2f}（{note}）")
    print(f"📊 目前累計支出：${total_spent:.2f} / 預算：${budget:.2f}（剩餘：${remaining:.2f}）")

    if total_spent > budget:
        print(f"🚨 警告：已超出預算 ${abs(remaining):.2f}！")
    elif budget > 0 and (total_spent / budget) >= 0.8:
        print("⚠️ 提醒：支出已達預算 80% 以上，請留意花費！")


def show_records(records: list[dict], budget: float) -> None:
    """顯示所有支出明細與預算摘要。"""
    print("\n" + "=" * 45)
    print("📋 支出明細列表")
    print("=" * 45)

    if not records:
        print("目前尚無任何支出紀錄。")
    else:
        for idx, item in enumerate(records, start=1):
            cat = item["category"].capitalize()
            amt = item["amount"]
            note = item["note"]
            print(f"{idx:>2}. [{cat:<8}] ${amt:>8.2f} | {note}")

    total_spent = sum(item["amount"] for item in records)
    remaining = budget - total_spent
    print("-" * 45)
    print(f"總支出：${total_spent:.2f} | 預算：${budget:.2f} | 剩餘：${remaining:.2f}")
    print("=" * 45 + "\n")


def show_category_summary(records: list[dict]) -> None:
    """依支出類別統計總金額。"""
    print("\n" + "=" * 45)
    print("🗂️ 類別花費統計")
    print("=" * 45)

    if not records:
        print("目前尚無資料可統計。")
        print("=" * 45 + "\n")
        return

    category_totals: dict[str, float] = {}
    for item in records:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + item["amount"]

    # 依金額由高到低排序顯示
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    for cat, total in sorted_categories:
        print(f"- {cat.capitalize():<10}：${total:.2f}")
    print("=" * 45 + "\n")


def main() -> None:
    """主程式進入點。"""
    records: list[dict] = []
    budget = 10000.0

    print("歡迎使用【個人記帳與預算小幫手】！")
    custom_budget = input(f"請輸入本月預算（直接按 Enter 使用預設 ${budget:.0f}）：").strip()
    if custom_budget:
        try:
            parsed = float(custom_budget)
            if parsed > 0:
                budget = round(parsed, 2)
            else:
                print("⚠️ 預算需大於 0，已改用預設預算。")
        except ValueError:
            print("⚠️ 輸入非有效數字，已改用預設預算。")

    print(f"本次設定預算為：${budget:.2f}\n")

    while True:
        print("請選擇功能：")
        print("1. 新增支出")
        print("2. 檢視支出明細")
        print("3. 查看類別統計")
        print("4. 離開程式")

        choice = input("輸入選項（1-4）：").strip()

        if choice == "1":
            add_expense(records, budget)
        elif choice == "2":
            show_records(records, budget)
        elif choice == "3":
            show_category_summary(records)
        elif choice == "4":
            print("感謝使用，祝你理財順利！👋")
            break
        else:
            print("⚠️ 無效的選項，請輸入 1 到 4 之間的數字。\n")


if __name__ == "__main__":
    main()