CATALOG = (
    {"name": "機械鍵盤", "price": 1290.0, "category": "3C配件"},
    {"name": "無線滑鼠", "price": 590.0, "category": "3C配件"},
    {"name": "保溫隨行杯", "price": 450.0, "category": "生活用品"},
    {"name": "筆記本組合", "price": 180.0, "category": "文具書籍"},
    {"name": "耳罩式耳機", "price": 1580.0, "category": "3C配件"},
)

# 折扣碼設定：(說明, 折扣類型 'rate' 或 'off', 數值, 最低消費門檻)
PROMO_CODES = {
    "SAVE10": ("全館 9 折優惠", "rate", 0.9, 0.0),
    "STUDENT": ("學生專屬 85 折優惠", "rate", 0.85, 300.0),
    "NEWUSER": ("滿 500 元現折 80 元", "off", 80.0, 500.0),
}


def read_positive_int(prompt: str) -> int | None:
    """讀取並驗證大於 0 的整數，無效時回傳 None。"""
    raw = input(prompt).strip()
    try:
        val = int(raw)
        if val <= 0:
            print("⚠️ 數量必須是大於 0 的整數。")
            return None
        return val
    except ValueError:
        print("⚠️ 請輸入有效的整數。")
        return None


def read_positive_float(prompt: str) -> float | None:
    """讀取並驗證大於 0 的金額，無效時回傳 None。"""
    raw = input(prompt).strip()
    try:
        val = float(raw)
        if val <= 0:
            print("⚠️ 金額必須大於 0。")
            return None
        return round(val, 2)
    except ValueError:
        print("⚠️ 請輸入有效的數字金額。")
        return None


def show_catalog() -> None:
    """顯示預設商品目錄。"""
    print("\n" + "=" * 50)
    print("🛍️ 精選商品目錄")
    print("=" * 50)
    for idx, item in enumerate(CATALOG, start=1):
        print(f"{idx}. [{item['category']}] {item['name']} — {item['price']:g} 元")
    print("=" * 50 + "\n")


def add_to_cart(cart: list[dict]) -> None:
    """從目錄挑選或自訂新增商品至購物車。"""
    show_catalog()
    choice = input("輸入商品編號加入購物車（或輸入 '自訂' 新增品項）：").strip()

    if choice.lower() in ("自訂", "custom"):
        name = input("請輸入商品名稱：").strip()
        if not name:
            print("⚠️ 商品名稱不可為空白。\n")
            return
        price = read_positive_float("請輸入單價（元）：")
        if price is None:
            print()
            return
        qty = read_positive_int("請輸入購買數量：")
        if qty is None:
            print()
            return
        target_name = name
        target_price = price
    else:
        try:
            idx = int(choice)
            if idx < 1 or idx > len(CATALOG):
                print("⚠️ 商品編號超出範圍。\n")
                return
        except ValueError:
            print("⚠️ 無效的輸入。\n")
            return

        selected = CATALOG[idx - 1]
        qty = read_positive_int(f"請輸入【{selected['name']}】購買數量：")
        if qty is None:
            print()
            return
        target_name = selected["name"]
        target_price = selected["price"]

    for item in cart:
        if item["name"].lower() == target_name.lower():
            item["qty"] += qty
            print(f"✅ 已更新【{item['name']}】數量為 {item['qty']} 件。\n")
            return

    cart.append({
        "name": target_name,
        "price": target_price,
        "qty": qty,
    })
    print(f"✅ 已將【{target_name}】x {qty} 加入購物車。\n")


def view_and_edit_cart(cart: list[dict]) -> None:
    """檢視購物車內容，並支援修改數量或移除商品。"""
    print("\n" + "=" * 52)
    print("🛒 目前購物車清單")
    print("=" * 52)

    if not cart:
        print("購物車目前是空的。")
        print("=" * 52 + "\n")
        return

    subtotal = 0.0
    for idx, item in enumerate(cart, start=1):
        line_total = item["price"] * item["qty"]
        subtotal += line_total
        print(f"{idx}. {item['name']}｜單價 {item['price']:g} 元 × {item['qty']} ＝ {line_total:g} 元")

    print("-" * 52)
    print(f"目前商品小計：{subtotal:g} 元")
    print("=" * 52)

    action = input("要修改數量請輸入 'u'，移除商品請輸入 'r'，直接返回請按 Enter：").strip().lower()
    if action == "u":
        idx = read_positive_int("請輸入要修改的購物車編號：")
        if idx is None or idx > len(cart):
            print("⚠️ 編號無效。\n")
            return
        new_qty = read_positive_int("請輸入新的數量：")
        if new_qty is None:
            print()
            return
        cart[idx - 1]["qty"] = new_qty
        print(f"✅ 已將【{cart[idx - 1]['name']}】數量更新為 {new_qty}。\n")
    elif action == "r":
        idx = read_positive_int("請輸入要移除的購物車編號：")
        if idx is None or idx > len(cart):
            print("⚠️ 編號無效。\n")
            return
        removed = cart.pop(idx - 1)
        print(f"🗑️ 已從購物車移除【{removed['name']}】。\n")
    else:
        print()


def apply_promo(subtotal: float, code_input: str) -> tuple[float, str]:
    """依折扣碼計算折抵金額，回傳（折抵金額, 說明文字）。"""
    code = code_input.strip().upper()
    if not code:
        return 0.0, "未套用折扣碼"

    if code not in PROMO_CODES:
        return 0.0, f"折扣碼 '{code}' 無效，未折抵"

    desc, promo_type, val, min_spend = PROMO_CODES[code]
    if subtotal < min_spend:
        return 0.0, f"未達【{code}】滿 {min_spend:g} 元門檻，未折抵"

    if promo_type == "rate":
        discount = round(subtotal * (1 - val), 2)
        return discount, f"{code}（{desc}）"

    discount = min(round(val, 2), subtotal)
    return discount, f"{code}（{desc}）"


def checkout(cart: list[dict]) -> None:
    """執行結帳並印出明細，完成後清空購物車。"""
    if not cart:
        print("\n⚠️ 購物車是空的，無法結帳。\n")
        return

    print("\n可用折扣碼參考：SAVE10（9折）、STUDENT（滿300享85折）、NEWUSER（滿500折80）")
    code = input("請輸入折扣碼（無則直接按 Enter）：")

    subtotal = sum(item["price"] * item["qty"] for item in cart)
    discount, promo_note = apply_promo(subtotal, code)
    final_total = max(0.0, round(subtotal - discount, 2))

    print("\n" + "=" * 50)
    print("🧾 結帳收據明細")
    print("=" * 50)
    for item in cart:
        line_total = item["price"] * item["qty"]
        print(f"* {item['name']} x {item['qty']} = {line_total:g} 元")
    print("-" * 50)
    print(f"商品小計：{subtotal:g} 元")
    print(f"優惠狀態：{promo_note}")
    print(f"折扣金額：-{discount:g} 元")
    print(f"實付總額：{final_total:g} 元")
    print("=" * 50 + "\n")

    cart.clear()
    print("✅ 結帳完成，購物車已清空，歡迎再次光臨！\n")


def main() -> None:
    """主程式進入點。"""
    cart: list[dict] = []
    print("歡迎使用【智慧購物車與折扣結算系統】！")

    while True:
        print("請選擇功能：")
        print("1. 瀏覽目錄並加入商品")
        print("2. 檢視 / 修改購物車")
        print("3. 前往結帳")
        print("4. 清空購物車")
        print("5. 離開系統")

        choice = input("輸入選項（1-5）：").strip()

        if choice == "1":
            add_to_cart(cart)
        elif choice == "2":
            view_and_edit_cart(cart)
        elif choice == "3":
            checkout(cart)
        elif choice == "4":
            cart.clear()
            print("🗑️ 已清空購物車。\n")
        elif choice == "5":
            print("感謝使用，祝你有美好的一天！🛒")
            break
        else:
            print("⚠️ 請輸入 1 到 5 之間的選項。\n")


if __name__ == "__main__":
    main()