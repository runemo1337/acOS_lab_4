import db

def print_contacts(contacts):
    if not contacts:
        print("\nСписок контактов пуст")
        return
    print("\n" + "="*60)
    for contact in contacts:
        print(f"ID: {contact[0]}")
        print(f"ФИО: {contact[1]}")
        print(f"Телефон: {contact[2]}")
        print(f"Заметка: {contact[3]}")
        print("-"*40)
    print("="*60)

def main():
    # Подключаемся к БД
    conn = db.wait_for_db()

    while True:
        print("\n ТЕЛЕФОННАЯ КНИГА")
        print("1. Добавить контакт")
        print("2. Изменить контакт")
        print("3. Удалить контакт")
        print("4. Выйти")
        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            print("\n--- Добавление контакта ---")
            name = input("ФИО: ")
            phone = input("Телефон: ")
            note = input("Заметка: ")
            db.create_contact(conn, name, phone, note)

        elif choice == "2":
            print("\n--- Изменение контакта ---")
            contacts = db.get_all_contacts(conn)
            print_contacts(contacts)
            if not contacts:
                continue
            try:
                contact_id = int(input("Введите ID контакта для изменения: "))
                old_data = db.get_contact_by_id(conn, contact_id)
                if not old_data:
                    print("Контакт не найден")
                    continue

                print("Оставьте поле пустым, чтобы оставить старое значение")
                new_name = input(f"Новое ФИО ({old_data[0]}): ") or old_data[0]
                new_phone = input(f"Новый телефон ({old_data[1]}): ") or old_data[1]
                new_note = input(f"Новая заметка ({old_data[2]}): ") or old_data[2]

                db.update_contact(conn, contact_id, new_name, new_phone, new_note)
            except ValueError:
                print("Некорректный ID")

        elif choice == "3":
            print("\n--- Удаление контакта ---")
            contacts = db.get_all_contacts(conn)
            print_contacts(contacts)
            if not contacts:
                continue
            try:
                contact_id = int(input("Введите ID контакта для удаления: "))
                db.delete_contact(conn, contact_id)
            except ValueError:
                print("Некорректный ID")

        elif choice == "4":
            print("Выход из программы")
            conn.close()
            break
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()