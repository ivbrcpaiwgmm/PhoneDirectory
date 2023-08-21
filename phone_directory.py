import json
import os

# Имя файла для хранения справочника
PHONEBOOK_FILE: str = "contacts_db.json"


def load_phonebook() -> list:
    """Загрузка справочника из файла."""
    if not os.path.isfile(PHONEBOOK_FILE):
        print(f"Программа остановлена. Справочник с именем '{PHONEBOOK_FILE}' не найден."
              f" Проверьте название и расположение файла.")
        exit()
    try:
        with open(PHONEBOOK_FILE, "r") as file:
            phonebook: list = json.load(file)
    except json.JSONDecodeError:
        print("Программа остановлена. Ошибка при загрузке файла с данными. Проверьте формат файла.")
        exit()
    return phonebook


def save_phonebook(phonebook: list) -> None:
    """Сохранение справочника в файл."""
    with open(PHONEBOOK_FILE, "w") as file:
        json.dump(phonebook, file, indent=4)


def input_contact_data(contact: dict) -> None:
    """Функция для ввода данных контакта."""
    contact["last_name"] = input("Введите фамилию: ")
    contact["first_name"] = input("Введите имя: ")
    contact["middle_name"] = input("Введите отчество: ")
    contact["organization"] = input("Введите название организации: ")
    while True:
        phone = input("Введите рабочий телефон (только цифры и символ '-' ): ")
        if all(char.isdigit() or char == '-' for char in phone):
            contact["work_phone"] = str(phone)
            break
        else:
            print("Недопустимые символы. Пожалуйста, введите телефон повторно (только цифры и символ '-' ):")
    while True:
        phone = input("Введите личный (сотовый) телефон (только цифры и символ '-' ): ")
        if all(char.isdigit() or char == '-' for char in phone):
            contact["personal_phone"] = str(phone)
            break
        else:
            print("Недопустимые символы. Пожалуйста, введите телефон повторно (только цифры и символ '-' ):")


def add_contact() -> None:
    """Добавление новой записи в справочник."""
    phonebook: list = load_phonebook()
    contact: dict = {}
    contact["id"]: str = str(len(phonebook) + 1)  # Присваиваем уникальный id как строку
    input_contact_data(contact)
    phonebook.append(contact)
    save_phonebook(phonebook)
    print("Запись успешно добавлена.")
    print_headers()
    print_contact(contact)


def edit_contact() -> None:
    """Редактирование записи в справочнике по id."""
    contact_id: str = input("Введите id записи для редактирования: ")
    phonebook: list = load_phonebook()
    for contact in phonebook:
        if contact["id"] == contact_id:
            print_headers()
            print_contact(contact)
            input_contact_data(contact)
            save_phonebook(phonebook)
            print("Запись успешно отредактирована.")
            print_headers()
            print_contact(contact)
            return
    print("Запись не найдена.")


def search_contacts() -> None:
    """Поиск записей по характеристикам."""
    queries: list = input("Введите текст для поиска. Вы можете ввести совокупность запросов через пробел: ").split()
    phonebook: list = load_phonebook()
    results: list = []

    if not queries:
        print("Вы не ввели запрос.")
        return

    for contact in phonebook:
        matches: int = 0
        for query in queries:
            # Поиск по всем характеристикам
            if any(query.lower() in value.lower() for value in contact.values()):
                matches += 1
        if matches == len(queries):
            results.append(contact)

    if results:
        print("Результаты поиска:")
        print_headers()
        for result in results:
            print_contact(result)
    else:
        print("Записи не найдены.")


def display_contacts(page: int, page_size: int) -> None:
    """Вывод записей из справочника постранично."""
    phonebook: list = load_phonebook()
    start: int = (page - 1) * page_size
    end: int = start + page_size
    contacts_to_display: list = phonebook[start:end]

    if contacts_to_display:
        print_headers()
        for contact in contacts_to_display:
            print_contact(contact)
    else:
        print("Справочник пуст или страница не существует.")


def print_headers() -> None:
    """Вывод заголовков для таблицы контактов."""
    print(
        f"{'id':<6} {'Фамилия':<18} {'Имя':<15} {'Отчество':<18} {'Организация':<30} "
        f"{'Рабочий тел.':<18} {'Личный тел.':<18}")


def print_contact(contact: dict) -> None:
    """Вывод информации о контакте в заданном формате."""
    id_width: int = 6
    name_width: int = 15
    mid_last_name_width: int = 18
    org_width: int = 30
    phone_width: int = 18

    id_formatted: str = f"{contact['id']:<{id_width}}"

    name_formatted: str = f"{contact['last_name']:<{mid_last_name_width}} {contact['first_name']:<{name_width}} " \
                          f"{contact['middle_name']:<{mid_last_name_width}}"

    org_formatted: str = f"{contact['organization']:<{org_width}}"
    work_phone_formatted: str = f"{contact['work_phone']:<{phone_width}}"
    personal_phone_formatted: str = f"{contact['personal_phone']:<{phone_width}}"

    print(f"{id_formatted} {name_formatted} {org_formatted} {work_phone_formatted} {personal_phone_formatted}")


def main() -> None:
    """Основная функция программы."""
    while True:
        print("\nТелефонный справочник:")
        print("1. Вывод записей")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Выход")

        choice: str = input("Выберите действие: ")

        if choice == "1":
            page_size: int = 10  # Количество записей для отображения на одной странице
            page: int = int(input("Введите номер страницы: "))
            display_contacts(page, page_size)
        elif choice == "2":
            add_contact()
        elif choice == "3":
            edit_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Введите номер необходимого пункта меню.")


if __name__ == "__main__":
    main()
