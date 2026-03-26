import db
import re

def validate_name(name):
    """Проверка ФИО: только буквы, пробелы, дефис, не пустое"""
    if not name or len(name.strip()) == 0:
        return False, "ФИО не может быть пустым"
    if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s\-]+$', name):
        return False, "ФИО должно содержать только буквы, пробелы и дефис"
    if len(name) > 100:
        return False, "ФИО не должно превышать 100 символов"
    return True, ""

def validate_phone(phone):
    """Проверка телефона: цифры, может начинаться с +, длина 10-15"""
    phone = phone.strip()
    if not phone:
        return False, "Телефон не может быть пустым"
    phone_clean = phone.lstrip('+')
    if not phone_clean.isdigit():
        return False, "Телефон должен содержать только цифры (и + в начале)"
    if len(phone_clean) < 10 or len(phone_clean) > 15:
        return False, "Телефон должен содержать 10-15 цифр"
    return True, ""

def validate_note(note):
    """Проверка заметки: не длиннее 200 символов"""
    if note and len(note) > 200:
        return False, "Заметка не должна превышать 200 символов"
    return True, ""

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
            
            while True:
                name = input("ФИО: ").strip()
                valid, error = validate_name(name)
                if valid:
                    break
                print(f"Ошибка: {error}")
            
            while True:
                phone = input("Телефон: ").strip()
                valid, error = validate_phone(phone)
                if valid:
                    break
                print(f"Ошибка: {error}")
            
            while True:
                note = input("Заметка: ").strip()
                valid, error = validate_note(note)
                if valid:
                    break
                print(f"Ошибка: {error}")
            
            db.create_contact(conn, name, phone, note)
                
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
                
                while True:
                    new_name = input(f"Новое ФИО ({old_data[0]}): ").strip()
                    if not new_name:
                        new_name = old_data[0]
                        break
                    valid, error = validate_name(new_name)
                    if valid:
                        break
                    print(f"Ошибка: {error}")
                
                while True:
                    new_phone = input(f"Новый телефон ({old_data[1]}): ").strip()
                    if not new_phone:
                        new_phone = old_data[1]
                        break
                    valid, error = validate_phone(new_phone)
                    if valid:
                        break
                    print(f"Ошибка: {error}")
                
                while True:
                    new_note = input(f"Новая заметка ({old_data[2]}): ").strip()
                    if not new_note:
                        new_note = old_data[2]
                        break
                    valid, error = validate_note(new_note)
                    if valid:
                        break
                    print(f"Ошибка: {error}")
                    
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
            input("\nНажмите Enter, чтобы вернуться в меню...")
                
        elif choice == "5":
            print("Выход из программы...")
            conn.close()
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()