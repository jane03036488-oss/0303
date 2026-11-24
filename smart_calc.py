ALLOWED_EXPR_CHARS = tuple("0123456789+-*/().% ")

LENGTH_TO_METER = {
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
}


def eval_expression(raw_expr: str) -> float | None:
    """清理並安全計算基本數學算式，錯誤時回傳 None。"""
    cleaned = raw_expr.strip().replace("×", "*").replace("÷", "/")
    if not cleaned:
        print("⚠️ 算式不可為空白。")
        return None

    if any(ch not in ALLOWED_EXPR_CHARS for ch in cleaned):
        print("⚠️ 算式包含不允許的字元，僅支援數字與 + - * / ** ( ) . %。")
        return None

    try:
        result = eval(cleaned, {"__builtins__": {}}, {})
        if isinstance(result, bool) or not isinstance(result, (int, float)):
            print("⚠️ 無法計算此算式。")
            return None
        return round(float(result), 4)
    except ZeroDivisionError:
        print("⚠️ 錯誤：除數不可為 0。")
        return None
    except Exception:
        print("⚠️ 算式格式有誤，請檢查括號或運算符號。")
        return None


def convert_temperature(value: float, src: str, dst: str) -> float | None:
    """轉換攝氏 (C)、華氏 (F)、克爾文 (K) 溫度。"""
    src = src.upper()
    dst = dst.upper()

    if src == dst:
        return value

    # 先轉為攝氏 C
    if src == "C":
        celsius = value
    elif src == "F":
        celsius = (value - 32) * 5 / 9
    elif src == "K":
        celsius = value - 273.15
    else:
        return None

    # 再由攝氏 C 轉為目標單位
    if dst == "C":
        return celsius
    if dst == "F":
        return celsius * 9 / 5 + 32
    if dst == "K":
        return celsius + 273.15
    return None


def handle_unit_conversion(history: list[str]) -> None:
    """處理長度與溫度單位換算。"""
    print("\n--- 單位換算 ---")
    print("長度單位：cm, m, km, inch（例如：cm -> m）")
    print("溫度單位：C, F, K（例如：C -> F）")

    src = input("請輸入來源單位：").strip()
    dst = input("請輸入目標單位：").strip()
    raw_val = input("請輸入數值：").strip()

    try:
        val = float(raw_val)
    except ValueError:
        print("⚠️ 數值格式錯誤，請輸入數字。\n")
        return

    src_lower = src.lower()
    dst_lower = dst.lower()

    if src_lower in LENGTH_TO_METER and dst_lower in LENGTH_TO_METER:
        if src_lower != "inch" and val < 0 and (src_lower in ("cm", "m", "km")):
            print("⚠️ 長度數值通常不為負數，請確認輸入。\n")
            return
        meters = val * LENGTH_TO_METER[src_lower]
        converted = meters / LENGTH_TO_METER[dst_lower]
        record = f"[長度] {val:g} {src_lower} = {converted:.4f} {dst_lower}"
        history.append(record)
        print(f"✅ 換算結果：{record}\n")
        return

    converted_temp = convert_temperature(val, src, dst)
    if converted_temp is not None:
        record = f"[溫度] {val:g} {src.upper()} = {converted_temp:.2f} {dst.upper()}"
        history.append(record)
        print(f"✅ 換算結果：{record}\n")
        return

    print("⚠️ 不支援此組單位換算，請重新確認單位名稱。\n")


def show_history(history: list[str]) -> None:
    """顯示計算歷史紀錄。"""
    print("\n" + "=" * 42)
    print("🧾 計算歷史紀錄")
    print("=" * 42)
    if not history:
        print("目前尚無任何計算紀錄。")
    else:
        for idx, item in enumerate(history, start=1):
            print(f"{idx}. {item}")
    print("=" * 42 + "\n")


def main() -> None:
    """主程式進入點。"""
    history: list[str] = []
    print("歡迎使用【多功能單位與算式計算小幫手】！")

    while True:
        print("請選擇功能：")
        print("1. 算式計算（支援 + - * / ** 括號）")
        print("2. 單位換算（長度 / 溫度）")
        print("3. 查看歷史紀錄")
        print("4. 離開程式")

        choice = input("輸入選項（1-4）：").strip()

        if choice == "1":
            expr = input("請輸入算式：")
            ans = eval_expression(expr)
            if ans is not None:
                clean_expr = expr.strip().replace("×", "*").replace("÷", "/")
                record = f"[算式] {clean_expr} = {ans:g}"
                history.append(record)
                print(f"✅ 計算結果：{ans:g}\n")
        elif choice == "2":
            handle_unit_conversion(history)
        elif choice == "3":
            show_history(history)
        elif choice == "4":
            print("感謝使用，計算完成！👋")
            break
        else:
            print("⚠️ 請輸入 1 到 4 之間的選項。\n")


if __name__ == "__main__":
    main()
    