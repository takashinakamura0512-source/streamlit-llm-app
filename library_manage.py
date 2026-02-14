from datetime import datetime, timedelta

# 定数定義
MAX_BORROW_LIMIT = 5
FINE_PER_DAY = 100
BORROW_PERIOD_DAYS = 7

# データストレージ
books = []
members = []
borrow_records = []

# ヘルパー関数
def find_book_by_id(book_id):
    """図書IDから図書を検索"""
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None

def find_member_by_id(member_id):
    """会員IDから会員を検索"""
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None

def count_active_borrows(member_id):
    """会員の現在の貸出冊数をカウント"""
    count = 0
    for record in borrow_records:
        if record["member_id"] == member_id and not record["returned"]:
            count += 1
    return count

def calculate_overdue_days(due_date_str):
    """延滞日数を計算"""
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    today = datetime.now()
    overdue = (today - due_date).days
    return max(overdue, 0)

def add_book(book_id, title, author, copies):
    """図書を追加"""
    if find_book_by_id(book_id):
        print(f"図書ID「{book_id}」の本は既に存在します。")
        return

    books.append({
        "book_id": book_id,
        "title": title,
        "author": author,
        "copies": copies,
        "available_copies": copies
    })
    print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")

def list_books():
    """図書一覧を表示"""
    if not books:
        print("現在、登録されている図書はありません。")
        return

    print("\n--- 図書一覧 ---")
    for book in books:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, "
              f"著者: {book['author']}, 総冊数: {book['copies']}, "
              f"在庫: {book['available_copies']}")

def search_book(book_id):
    """図書を検索"""
    book = find_book_by_id(book_id)
    if book:
        print(f"\nID: {book['book_id']}, タイトル: {book['title']}, "
              f"著者: {book['author']}, 総冊数: {book['copies']}, "
              f"在庫: {book['available_copies']}")
    else:
        print(f"図書ID「{book_id}」の本は存在しません。")

def add_member(member_id, name):
    """会員を追加"""
    if find_member_by_id(member_id):
        print(f"会員ID「{member_id}」の会員は既に存在します。")
        return

    members.append({"member_id": member_id, "name": name})
    print(f"会員「{name}」（ID: {member_id}）を追加しました。")

def list_members():
    """会員一覧を表示"""
    if not members:
        print("現在、登録されている会員はいません。")
        return

    print("\n--- 会員一覧 ---")
    for member in members:
        borrowed_count = count_active_borrows(member["member_id"])
        print(f"ID: {member['member_id']}, 名前: {member['name']}, "
              f"貸出中: {borrowed_count}/{MAX_BORROW_LIMIT}冊")

def borrow_book(book_id, member_id):
    """図書を貸し出す"""
    book = find_book_by_id(book_id)
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return

    member = find_member_by_id(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return

    if book["available_copies"] <= 0:
        print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
        return

    active_borrows = count_active_borrows(member_id)
    if active_borrows >= MAX_BORROW_LIMIT:
        print(f"貸出可能数は{MAX_BORROW_LIMIT}冊までです。現在{active_borrows}冊借りています。")
        return

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=BORROW_PERIOD_DAYS)
    
    borrow_records.append({
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "returned": False
    })
    
    book["available_copies"] -= 1
    
    print(f"\n図書「{book['title']}」を会員「{member['name']}」に貸し出しました。")
    print(f"貸出日: {borrow_date.strftime('%Y-%m-%d')}")
    print(f"返却期限: {due_date.strftime('%Y-%m-%d')}")

def list_borrowed_books():
    """貸出中の図書一覧を表示"""
    print("\n--- 貸出中の図書一覧 ---")
    borrow_count = 0
    
    for record in borrow_records:
        if not record["returned"]:
            book = find_book_by_id(record["book_id"])
            member = find_member_by_id(record["member_id"])
            
            if book and member:
                overdue_days = calculate_overdue_days(record["due_date"])
                status = f" [延滞{overdue_days}日]" if overdue_days > 0 else ""
                
                print(f"図書: {book['title']}（ID: {record['book_id']}）")
                print(f"  会員: {member['name']}（ID: {record['member_id']}）")
                print(f"  貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}{status}")
                print()
                borrow_count += 1
    
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

def return_book(book_id, member_id):
    """図書を返却"""
    record = None
    for r in borrow_records:
        if (r["book_id"] == book_id and 
            r["member_id"] == member_id and 
            not r["returned"]):
            r["returned"] = True
            record = r
            break
    
    if not record:
        print(f"図書ID「{book_id}」を会員ID「{member_id}」の会員は借りていません。")
        return

    book = find_book_by_id(book_id)
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return
    
    book["available_copies"] += 1
    
    overdue_days = calculate_overdue_days(record["due_date"])
    fine = overdue_days * FINE_PER_DAY
    
    print(f"\n図書「{book['title']}」が返却されました。")
    if overdue_days > 0:
        print(f"延滞日数: {overdue_days}日")
        print(f"延滞料金: {fine}円")
    else:
        print("期限内の返却です。")

def calculate_fines():
    """延滞料金を計算"""
    print("\n--- 延滞料金一覧 ---")
    overdue_count = 0
    total_fine = 0
    
    for record in borrow_records:
        if not record["returned"]:
            overdue_days = calculate_overdue_days(record["due_date"])
            
            if overdue_days > 0:
                book = find_book_by_id(record["book_id"])
                member = find_member_by_id(record["member_id"])
                
                if book and member:
                    fine = overdue_days * FINE_PER_DAY
                    total_fine += fine
                    
                    print(f"図書: {book['title']}（ID: {record['book_id']}）")
                    print(f"  会員: {member['name']}（ID: {record['member_id']}）")
                    print(f"  返却期限: {record['due_date']}")
                    print(f"  延滞日数: {overdue_days}日, 延滞料金: {fine}円")
                    print()
                    overdue_count += 1
    
    if overdue_count == 0:
        print("現在、延滞している図書はありません。")
    else:
        print(f"延滞合計: {overdue_count}件, 合計延滞料金: {total_fine}円")

def show_member_borrowed_books(member_id):
    """会員の貸出状況を表示"""
    member = find_member_by_id(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return

    print(f"\n--- 会員「{member['name']}」（ID: {member_id}）の貸出状況 ---")
    borrowed_count = 0
    total_fine = 0
    
    for record in borrow_records:
        if record["member_id"] == member_id and not record["returned"]:
            book = find_book_by_id(record["book_id"])
            
            if book:
                overdue_days = calculate_overdue_days(record["due_date"])
                fine = overdue_days * FINE_PER_DAY if overdue_days > 0 else 0
                total_fine += fine
                
                status = f" [延滞{overdue_days}日、料金{fine}円]" if overdue_days > 0 else " [期限内]"
                
                print(f"図書: {book['title']}（ID: {record['book_id']}）")
                print(f"  貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}{status}")
                borrowed_count += 1
    
    print(f"\n現在の貸出冊数: {borrowed_count}/{MAX_BORROW_LIMIT}冊")
    if total_fine > 0:
        print(f"延滞料金合計: {total_fine}円")
    
    if borrowed_count == 0:
        print("この会員は現在、図書を借りていません。")

def main():
    """メイン関数"""
    print("\n=== 図書館管理システム ===")
    print(f"貸出期間: {BORROW_PERIOD_DAYS}日")
    print(f"延滞料金: {FINE_PER_DAY}円/日")
    print(f"貸出上限: {MAX_BORROW_LIMIT}冊\n")
    
    while True:
        print("\n" + "="*40)
        print("図書館管理システムメニュー")
        print("="*40)
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 会員の貸出状況を表示")
        print("11: 終了")
        print("="*40)

        try:
            choice = int(input("\n操作を選択してください（1-11）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ")
                search_book(book_id)

            elif choice == 4:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 5:
                list_members()

            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 7:
                list_borrowed_books()

            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 9:
                calculate_fines()

            elif choice == 10:
                member_id = input("会員IDを入力してください: ")
                show_member_borrowed_books(member_id)

            elif choice == 11:
                print("\n図書館管理システムを終了します。")
                break

            else:
                print("\n無効な選択です。1-11の数字を入力してください。")

        except ValueError as e:
            print(f"\n入力エラー: {e}")
        except Exception as e:
            print(f"\n予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()