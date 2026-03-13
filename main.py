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
    conn = db.create_connection()
    
    while True:
        print("\n" + "="*40)
        print(" ТЕЛЕФОННАЯ КНИГА")
        print("="*40)
        print("1. Добавить контакт")
        print("2. Изменить контакт")
        print("3. Удалить контакт")
        print("4. Показать все контакты")
        print("5. Выйти")
        print("="*40)
        
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == "1":
            print("\n--- Добавление контакта ---")
            name = input("ФИО: ").strip()
            phone_number = input("Телефон: ").strip()
            note = input("Заметка: ").strip()
            
            if name and phone_number:
                db.create_contact(conn, name, phone_number, note)
            else:
                print("Ошибка: ФИО и телефон обязательны!")
                
        elif choice == "2":
            print("\n--- Изменение контакта ---")
            contacts = db.get_all_contacts(conn)
            if not contacts:
                print("Список контактов пуст")
                continue
                
            print_contacts(contacts)
            
            try:
                contact_id = int(input("Введите ID контакта для изменения: "))
                old_data = db.get_contact_by_id(conn, contact_id)
                
                if not old_data:
                    print("Контакт не найден")
                    continue
                    
                print("\nОставьте поле пустым, чтобы оставить старое значение")
                
                new_name = input(f"Новое ФИО ({old_data[0]}): ").strip()
                if not new_name:
                    new_name = old_data[0]
                    
                new_phone = input(f"Новый телефон ({old_data[1]}): ").strip()
                if not new_phone:
                    new_phone = old_data[1]
                    
                new_note = input(f"Новая заметка ({old_data[2]}): ").strip()
                if not new_note:
                    new_note = old_data[2]
                    
                db.update_contact(conn, contact_id, new_name, new_phone, new_note)
                
            except ValueError:
                print("Ошибка: введите корректный ID")
                
        elif choice == "3":
            print("\n--- Удаление контакта ---")
            contacts = db.get_all_contacts(conn)
            if not contacts:
                print("Список контактов пуст")
                continue
                
            print_contacts(contacts)
            
            try:
                contact_id = int(input("Введите ID контакта для удаления: "))
                db.delete_contact(conn, contact_id)
            except ValueError:
                print("Ошибка: введите корректный ID")
                
        elif choice == "4":
            print("\n--- Список контактов ---")
            contacts = db.get_all_contacts(conn)
            print_contacts(contacts)
                
        elif choice == "5":
            print("Выход из программы...")
            conn.close()
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    # Проверяем, что это главный модуль
    main()