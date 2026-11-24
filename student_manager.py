VALID_YEARS = (1, 2, 3, 4, 5, 6)


def normalize_student_id(raw_id: str) -> str:
    """清理並統一學號格式（去空白、轉大寫）。"""
    return raw_id.strip().upper()


def find_student_index(students: list[dict], student_id: str) -> int:
    """依學號尋找學生在串列中的索引，找不到回傳 -1。"""
    target = normalize_student_id(student_id)
    for idx, stu in enumerate(students):
        if stu["id"] == target:
            return idx
    return -1


def read_year(prompt: str) -> int | None:
    """讀取並驗證年級（1-6），無效時回傳 None。"""
    raw = input(prompt).strip()
    try:
        year = int(raw)
        if year not in VALID_YEARS:
            print("⚠️ 年級必須介於 1 到 6 之間。")
            return None
        return year
    except ValueError:
        print("⚠️ 年級格式錯誤，請輸入整數。")
        return None


def add_student(students: list[dict]) -> None:
    """新增一位學生資料。"""
    stu_id = normalize_student_id(input("\n請輸入學號："))
    if not stu_id:
        print("⚠️ 學號不可為空白。\n")
        return

    if find_student_index(students, stu_id) != -1:
        print(f"⚠️ 學號【{stu_id}】已存在，請勿重複新增。\n")
        return

    name = input("請輸入學生姓名：").strip()
    if not name:
        print("⚠️ 姓名不可為空白。\n")
        return

    department = input("請輸入系別或班級：").strip()
    if not department:
        print("⚠️ 系別或班級不可為空白。\n")
        return

    year = read_year("請輸入年級（1-6）：")
    if year is None:
        print()
        return

    note = input("請輸入備註（可留白）：").strip()
    students.append({
        "id": stu_id,
        "name": name,
        "department": department,
        "year": year,
        "note": note if note else "無",
    })
    print(f"✅ 已新增學生【{stu_id}】{name}（{department} {year}年級）\n")


def show_all_students(students: list[dict]) -> None:
    """顯示完整學生名冊。"""
    print("\n" + "=" * 62)
    print(f"📋 學生資料名冊（共 {len(students)} 人）")
    print("=" * 62)

    if not students:
        print("目前尚無任何學生資料。")
        print("=" * 62 + "\n")
        return

    for idx, stu in enumerate(students, start=1):
        print(
            f"{idx:>2}. 學號:{stu['id']:<10} | "
            f"姓名:{stu['name']:<8} | "
            f"系別:{stu['department']:<14} | "
            f"{stu['year']}年級 | 備註:{stu['note']}"
        )
    print("=" * 62 + "\n")


def search_students(students: list[dict]) -> None:
    """依學號、姓名或系別關鍵字搜尋學生。"""
    if not students:
        print("\n⚠️ 目前尚無任何學生資料可查詢。\n")
        return

    keyword = input("\n請輸入查詢關鍵字（學號、姓名或系別）：").strip()
    if not keyword:
        print("⚠️ 查詢關鍵字不可為空白。\n")
        return

    key_lower = keyword.lower()
    matched = []
    for stu in students:
        if (
            key_lower in stu["id"].lower()
            or key_lower in stu["name"].lower()
            or key_lower in stu["department"].lower()
        ):
            matched.append(stu)

    print(f"\n--- 搜尋結果（共 {len(matched)} 筆） ---")
    if not matched:
        print("查無符合條件的學生資料。\n")
        return

    for stu in matched:
        print(
            f"* [{stu['id']}] {stu['name']}｜{stu['department']}｜"
            f"{stu['year']}年級｜備註：{stu['note']}"
        )
    print()


def update_or_delete_student(students: list[dict]) -> None:
    """修改指定學生資料或刪除學生紀錄。"""
    if not students:
        print("\n⚠️ 目前尚無任何學生資料可操作。\n")
        return

    stu_id = normalize_student_id(input("\n請輸入目標學生學號："))
    idx = find_student_index(students, stu_id)
    if idx == -1:
        print(f"⚠️ 找不到學號為【{stu_id}】的學生。\n")
        return

    target = students[idx]
    print(f"已找到學生：{target['id']} - {target['name']}（{target['department']} {target['year']}年級）")
    action = input("輸入 'e' 修改資料、'd' 刪除學生，或按 Enter 取消：").strip().lower()

    if action == "d":
        removed = students.pop(idx)
        print(f"🗑️ 已刪除學生【{removed['id']}】{removed['name']} 的資料。\n")
        return

    if action == "e":
        new_dept = input(f"新系別/班級（目前：{target['department']}，留白不改）：").strip()
        if new_dept:
            target["department"] = new_dept

        new_year_raw = input(f"新年級 1-6（目前：{target['year']}，留白不改）：").strip()
        if new_year_raw:
            try:
                yr = int(new_year_raw)
                if yr in VALID_YEARS:
                    target["year"] = yr
                else:
                    print("⚠️ 年級超出 1-6 範圍，維持原年級。")
            except ValueError:
                print("⚠️ 年級輸入非數字，維持原年級。")

        new_note = input(f"新備註（目前：{target['note']}，留白不改）：").strip()
        if new_note:
            target["note"] = new_note

        print(f"✅ 已更新【{target['id']}】{target['name']} 的資料。\n")
    else:
        print("已取消操作。\n")


def main() -> None:
    """主程式進入點。"""
    students: list[dict] = []
    print("歡迎使用【學生基本資料與學籍查詢管理系統】！")

    while True:
        print("請選擇功能：")
        print("1. 新增學生資料")
        print("2. 檢視完整名冊")
        print("3. 搜尋學生資料")
        print("4. 修改 / 刪除學生資料")
        print("5. 離開系統")

        choice = input("輸入選項（1-5）：").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            show_all_students(students)
        elif choice == "3":
            search_students(students)
        elif choice == "4":
            update_or_delete_student(students)
        elif choice == "5":
            print("感謝使用，學生資料管理系統已關閉！🎓")
            break
        else:
            print("⚠️ 請輸入 1 到 5 之間的選項。\n")


if __name__ == "__main__":
    main()