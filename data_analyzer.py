SAMPLE_DATA = [72.0, 85.5, 91.0, 64.0, 78.5, 88.0, 95.0, 69.5, 82.0, 76.0]

# (區間名稱, 最低含, 最高不含)
BUCKETS = (
    ("90 以上", 90.0, 999999.0),
    ("80 - 89", 80.0, 90.0),
    ("70 - 79", 70.0, 80.0),
    ("60 - 69", 60.0, 70.0),
    ("60 以下", -999999.0, 60.0),
)


def parse_numbers(raw_text: str) -> list[float]:
    """將逗號、全形逗號或空白分隔的字串轉為浮點數串列。"""
    normalized = raw_text.replace("，", ",").strip()
    if not normalized:
        return []

    tokens = normalized.replace(",", " ").split()
    parsed: list[float] = []
    for tok in tokens:
        try:
            parsed.append(round(float(tok), 2))
        except ValueError:
            print(f"⚠️ 略過無效數值：'{tok}'")
    return parsed


def add_data(data: list[float]) -> None:
    """新增單筆或多筆數值至資料集。"""
    print("\n--- 新增數據 ---")
    print("可一次輸入多筆數字，以逗號或空白分隔（例如：80, 85.5, 90 或 75 82 88）")
    raw = input("請輸入數值：")
    new_items = parse_numbers(raw)

    if not new_items:
        print("⚠️ 未新增任何有效數值。\n")
        return

    data.extend(new_items)
    print(f"✅ 已新增 {len(new_items)} 筆資料，目前共有 {len(data)} 筆。\n")


def show_summary(data: list[float]) -> None:
    """顯示基本統計摘要。"""
    print("\n" + "=" * 48)
    print("📊 數據基本統計摘要")
    print("=" * 48)

    if not data:
        print("目前資料集為空，請先新增資料或載入範例。")
        print("=" * 48 + "\n")
        return

    count = len(data)
    total = 0.0
    max_val = data[0]
    min_val = data[0]

    for val in data:
        total += val
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val

    mean_val = total / count
    data_range = max_val - min_val
    above_mean = sum(1 for val in data if val > mean_val)
    above_ratio = (above_mean / count) * 100

    print(f"資料筆數：{count} 筆")
    print(f"總和：{total:g} | 平均值：{mean_val:.2f}")
    print(f"最大值：{max_val:g} | 最小值：{min_val:g} | 全距：{data_range:g}")
    print(f"高於平均值：{above_mean} 筆（佔 {above_ratio:.1f}%）")
    print("=" * 48 + "\n")


def show_distribution(data: list[float]) -> None:
    """統計各數值區間分佈並印出文字直條圖。"""
    print("\n" + "=" * 52)
    print("📈 區間分佈統計與直條圖")
    print("=" * 52)

    if not data:
        print("目前資料集為空，無法進行分佈分析。")
        print("=" * 52 + "\n")
        return

    counts: dict[str, int] = {label: 0 for label, _, _ in BUCKETS}
    for val in data:
        for label, low, high in BUCKETS:
            if low <= val < high:
                counts[label] += 1
                break

    total = len(data)
    for label, _, _ in BUCKETS:
        cnt = counts[label]
        pct = (cnt / total) * 100
        bar = "█" * cnt
        print(f"{label:<8} | {cnt:>2} 筆 ({pct:>5.1f}%) | {bar}")

    print("=" * 52 + "\n")


def main() -> None:
    """主程式進入點。"""
    data: list[float] = list(SAMPLE_DATA)
    print("歡迎使用【學習與消費數據統計分析小幫手】！")
    print(f"已預載 {len(data)} 筆範例資料：{data}\n")

    while True:
        print("請選擇功能：")
        print("1. 新增數值資料（支援批次輸入）")
        print("2. 檢視基本統計摘要")
        print("3. 檢視區間分佈與直條圖")
        print("4. 清空並重設為範例資料")
        print("5. 離開程式")

        choice = input("輸入選項（1-5）：").strip()

        if choice == "1":
            add_data(data)
        elif choice == "2":
            show_summary(data)
        elif choice == "3":
            show_distribution(data)
        elif choice == "4":
            data.clear()
            data.extend(SAMPLE_DATA)
            print("✅ 已重設為內建範例資料。\n")
        elif choice == "5":
            print("感謝使用，數據分析完成！📉")
            break
        else:
            print("⚠️ 請輸入 1 到 5 之間的選項。\n")


if __name__ == "__main__":
    main()