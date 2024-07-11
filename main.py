import json
from datetime import datetime
from typing import List, Dict

def load_operations(file_path: str) -> List[Dict]:
    """
    Загружает операции из JSON файла.

    :param file_path: Путь к файлу операций.
    :return: Список операций.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX.

    :param card_number: Номер карты.
    :return: Маскированный номер карты.
    """
    cleaned_number = card_number.replace(" ", "")
    return f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"

def mask_account_number(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX.

    :param account_number: Номер счета.
    :return: Маскированный номер счета.
    """
    return f"**{account_number[-4:]}"

def mask_account_or_card(account: str) -> str:
    """
    Определяет тип счета/карты и применяет соответствующую маскировку.

    :param account: Номер счета или карты.
    :return: Маскированный номер счета или карты.
    """
    if account.startswith('Счет'):
        return f"Счет {mask_account_number(account.split()[-1])}"
    else:
        name, number = ' '.join(account.split()[:-1]), account.split()[-1]
        return f"{name} {mask_card_number(number)}"

def format_operation(operation: Dict) -> str:
    """
    Форматирует операцию в строку для вывода.

    :param operation: Словарь с данными операции.
    :return: Строка с отформатированной операцией.
    """
    date = datetime.strptime(operation['date'], "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = date.strftime("%d.%m.%Y")
    description = operation['description']
    from_account = mask_account_or_card(operation['from']) if 'from' in operation else 'Неизвестно'
    to_account = mask_account_or_card(operation['to'])
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    return f"{formatted_date} {description}\n{from_account} -> {to_account}\n{amount} {currency}"

def get_last_executed_operations(operations: List[Dict], count: int = 5) -> List[Dict]:
    """
    Получает последние выполненные операции.

    :param operations: Список операций.
    :param count: Количество последних операций для вывода.
    :return: Список последних выполненных операций.
    """
    executed_operations = [op for op in operations if op.get('state') == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)
    return sorted_operations[:count]

def main():
    operations = load_operations('operations.json')
    last_operations = get_last_executed_operations(operations)

    for operation in last_operations:
        print(format_operation(operation))
        print()  # Пустая строка для разделения операций

if __name__ == "__main__":
    main()
