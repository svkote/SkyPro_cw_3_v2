import pytest
from main import (
    load_operations,
    mask_card_number,
    mask_account_number,
    mask_account_or_card,
    format_operation,
    get_last_executed_operations
)
import json

@pytest.fixture
def operations():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTЕД",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        }
    ]

def test_load_operations(tmpdir):
    data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }
    ]
    file_path = tmpdir.join('operations.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    loaded_operations = load_operations(file_path)
    assert loaded_operations == data

def test_mask_card_number():
    card_number = "1596837868705199"
    masked = mask_card_number(card_number)
    assert masked == "1596 83** **** 5199"

def test_mask_account_number():
    account_number = "64686473678894779589"
    masked = mask_account_number(account_number)
    assert masked == "**9589"

def test_mask_account_or_card():
    card = "Maestro 1596837868705199"
    masked_card = mask_account_or_card(card)
    assert masked_card == "Maestro 1596 83** **** 5199"

    account = "Счет 64686473678894779589"
    masked_account = mask_account_or_card(account)
    assert masked_account == "Счет **9589"

def test_format_operation(operations):
    operation = operations[0]
    formatted = format_operation(operation)
    expected = "26.08.2019 Перевод организации\nMaestro 1596 83** **** 5199 -> Счет **9589\n31957.58 руб."
    assert formatted == expected

def test_get_last_executed_operations(operations):
    last_operations = get_last_executed_operations(operations, count=1)
    assert last_operations == [operations[0]]
