DEFAULT_CATEGORIES = ("餐飲", "交通", "學習", "娛樂", "日用品", "其他")


def read_positive_amount(prompt: str) -> float | None:
    """讀取並驗證大於 0 的金額，無效時回傳 None。"""
    raw = input(prompt).strip()
    try:
        amount = float(raw)
        if amount <= 0:
            print("⚠️ 金額必須大於 0。")
            return None
        return round(amount, 2)
    except ValueError:
        print("⚠️ 金額格式錯誤，請輸入數字。")
        return None


def add_expense(expenses: list[dict]) -> None:
    """新增一筆支出紀錄。"""
    print("\n常見類別：" + " / ".join(DEFAULT_CATEGORIES))
    category = input("請輸入支出類別：").strip()
    if not category:
        category = "其他"
    else:
        category = category.capitalize()

    amount = read_positive_amount("請輸入支出金額：")
    if amount is None:
        print()
        return

    note = input("請輸入備註（可留白）：").strip()
    record = {
        "category": category,
        "amount": amount,
        "note": note if note else "無",
    }
    expenses.append(record)
    print(f"✅ 已記錄【{category}】{amount:g} 元（備註：{record['note']}）\n")


def show_report(expenses: list[dict], budget: float) -> None:
    """顯示支出明細、分類統計與預算狀態。"""
    print("\n" + "=" * 48)
    print("📒 個人記帳明細與預算報表")
    print("=" * 48)

    total_spent = 0.0
    category_totals: dict[str, float] = {}

    if not expenses:
        print("目前尚無任何支出紀錄。")
    else:
        for idx, item in enumerate(expenses, start=1):
            amt = item["amount"]
            cat = item["category"]
            total_spent += amt
            category_totals[cat] = category_totals.get(cat, 0.0) + amt
            print(f"{idx:>2}. [{cat}] {amt:g} 元｜備註：{item['note']}")

    remaining = budget - total_spent
    usage_ratio = (total_spent / budget * 100) if budget > 0 else 0.0

    print("-" * 48)
    print(f"每月預算：{budget:g} 元 | 已花費：{total_spent:g} 元 | 剩餘：{remaining:g} 元")
    print(f"預算使用率：{usage_ratio:.1f}%")

    if total_spent > budget:
        print(f"🚨 警告：目前已超出預算 {total_spent - budget:g} 元！")
    elif usage_ratio >= 80:
        print("⚠️ 提醒：支出已達預算 80% 警戒線，請留意後續花費。")

    if category_totals:
        print("-" * 48)
        print("分類支出統計（由高到低）：")
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        for cat, cat_sum in sorted_cats:
            print(f"  * {cat}：{cat_sum:g} 元")

    print("=" * 48 + "\n")


def set_budget(current_budget: float) -> float:
    """設定新的每月預算上限。"""
    print(f"\n目前每月預算為：{current_budget:g} 元")
    new_val = read_positive_amount("請輸入新的每月預算上限：")
    if new_val is None:
        print("維持原本預算設定。\n")
        return current_budget
    print(f"✅ 已更新每月預算為：{new_val:g} 元\n")
    return new_val


def main() -> None:
    """主程式進入點。"""
    expenses: list[dict] = []
    budget = 6000.0
    print("歡迎使用【智慧分類記帳與預算提醒小幫手】！")

    while True:
        print("請選擇功能：")
        print("1. 新增支出紀錄")
        print("2. 檢視明細與分類統計")
        print("3. 設定每月預算")
        print("4. 離開程式")

        choice = input("輸入選項（1-4）：").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_report(expenses, budget)
        elif choice == "3":
            budget = set_budget(budget)
        elif choice == "4":
            print("感謝使用，記帳完成！💰")
            break
        else:
            print("⚠️ 請輸入 1 到 4 之間的選項。\n")


if __name__ == "__main__":
    main()
    