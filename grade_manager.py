# (最低分數門檻, 等第, 4.3制 GPA 積點)
GRADE_SCALE = (
    (90, "A+", 4.3),
    (85, "A", 4.0),
    (80, "A-", 3.7),
    (77, "B+", 3.3),
    (73, "B", 3.0),
    (70, "B-", 2.7),
    (67, "C+", 2.3),
    (63, "C", 2.0),
    (60, "C-", 1.7),
    (0, "F", 0.0),
)


def score_to_grade_and_gpa(score: float) -> tuple[str, float]:
    """依原始分數（0-100）回傳（等第, GPA 積點）。"""
    for threshold, letter, gpa in GRADE_SCALE:
        if score >= threshold:
            return letter, gpa
    return "F", 0.0


def parse_float_in_range(prompt: str, min_val: float, max_val: float, allow_open_max: bool = False) -> float | None:
    """讀取並驗證數值範圍，無效時回傳 None。"""
    raw = input(prompt).strip()
    try:
        val = float(raw)
        if allow_open_max:
            if val < min_val:
                print(f"⚠️ 數值必須大於等於 {min_val:g}。")
                return None
        else:
            if val < min_val or val > max_val:
                print(f"⚠️ 數值必須介於 {min_val:g} 到 {max_val:g} 之間。")
                return None
        return round(val, 2)
    except ValueError:
        print("⚠️ 輸入格式錯誤，請輸入數字。")
        return None


def add_course(courses: list[dict]) -> None:
    """新增一筆課程成績紀錄。"""
    name = input("請輸入科目名稱：").strip()
    if not name:
        print("⚠️ 科目名稱不可為空白。\n")
        return

    credits = parse_float_in_range("請輸入學分數（例如 3 或 2）：", 0.5, 99.0, allow_open_max=True)
    if credits is None:
        print()
        return

    score = parse_float_in_range("請輸入原始成績（0 - 100）：", 0.0, 100.0)
    if score is None:
        print()
        return

    letter, gpa = score_to_grade_and_gpa(score)
    record = {
        "name": name,
        "credits": credits,
        "score": score,
        "grade": letter,
        "gpa": gpa,
    }
    courses.append(record)
    print(f"✅ 已新增【{name}】｜{credits:g} 學分｜分數 {score:.1f}｜等第 {letter}（GPA {gpa:.1f}）\n")


def show_overview(courses: list[dict]) -> None:
    """顯示所有修課明細、加權平均與整體 GPA。"""
    print("\n" + "=" * 54)
    print("🎓 課程成績與 GPA 總覽")
    print("=" * 54)

    if not courses:
        print("目前尚無任何修課紀錄。")
        print("=" * 54 + "\n")
        return

    total_credits = 0.0
    weighted_score_sum = 0.0
    weighted_gpa_sum = 0.0

    for idx, c in enumerate(courses, start=1):
        cr = c["credits"]
        sc = c["score"]
        gp = c["gpa"]
        total_credits += cr
        weighted_score_sum += sc * cr
        weighted_gpa_sum += gp * cr
        print(
            f"{idx:>2}. {c['name']:<12} | "
            f"學分:{cr:>4.1f} | "
            f"成績:{sc:>5.1f} | "
            f"等第:{c['grade']:<2} | "
            f"GPA:{gp:.1f}"
        )

    avg_score = weighted_score_sum / total_credits if total_credits > 0 else 0.0
    overall_gpa = weighted_gpa_sum / total_credits if total_credits > 0 else 0.0

    print("-" * 54)
    print(f"總學分：{total_credits:.1f} | 加權平均：{avg_score:.2f} | 整體 GPA：{overall_gpa:.2f}")
    print("=" * 54 + "\n")


def search_or_filter_courses(courses: list[dict]) -> None:
    """查詢指定科目，或列出不及格（<60）科目。"""
    if not courses:
        print("\n⚠️ 目前尚無任何修課紀錄可查詢。\n")
        return

    keyword = input("請輸入查詢科目關鍵字（輸入 '不及格' 可列出低於 60 分科目）：").strip()
    if not keyword:
        print("⚠️ 查詢關鍵字不可為空白。\n")
        return

    print("\n--- 查詢結果 ---")
    matched = []
    if keyword == "不及格":
        for c in courses:
            if c["score"] < 60:
                matched.append(c)
    else:
        key_lower = keyword.lower()
        for c in courses:
            if key_lower in c["name"].lower():
                matched.append(c)

    if not matched:
        print("查無符合條件的課程。\n")
        return

    for c in matched:
        print(f"* {c['name']}｜學分：{c['credits']:g}｜成績：{c['score']:.1f}｜等第：{c['grade']}")
    print()


def main() -> None:
    """主程式進入點。"""
    courses: list[dict] = []
    print("歡迎使用【課程成績與 GPA 計算管理系統】！")

    while True:
        print("請選擇功能：")
        print("1. 新增課程成績")
        print("2. 檢視成績總覽與 GPA")
        print("3. 查詢科目 / 不及格清單")
        print("4. 離開程式")

        choice = input("輸入選項（1-4）：").strip()

        if choice == "1":
            add_course(courses)
        elif choice == "2":
            show_overview(courses)
        elif choice == "3":
            search_or_filter_courses(courses)
        elif choice == "4":
            print("感謝使用，祝學業順利！📚")
            break
        else:
            print("⚠️ 無效的選項，請輸入 1 到 4 之間的數字。\n")


if __name__ == "__main__":
    main()