import base64
import requests


# на вход функция принимает номер блока, если он не существует - вызывается ошибка, иначе возвращается декодированная строка
# обработал также ключ block внутри транзакции
def get_transaction(number_block):
    transaction = requests.get(f"https://akash-api.polkachu.com/blocks/{number_block}")
    if transaction.status_code == 404:
        raise 'Блок транзакции не найден'
    try:
        transaction.json()['block']
    except KeyError as e:
        raise e
    return base64.b64decode(transaction.json()['block']['data']['txs'][0])


# вызов функции
print(get_transaction(12166520))
