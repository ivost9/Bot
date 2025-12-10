from flask import Flask, jsonify
import asyncio
import os
from metaapi_cloud_sdk import MetaApi

app = Flask(__name__)

# Твоята тайна парола (token) и ID
token = os.environ.get('METAAPI_TOKEN')
account_id = os.environ.get('ACCOUNT_ID')

async def trade_logic():
    # Проверка дали има настроени променливи
    if not token or not account_id:
        return {"error": "Липсват METAAPI_TOKEN или ACCOUNT_ID в настройките на Vercel!"}

    api = MetaApi(token)
    try:
        # Свързване с акаунта
        account = await api.metatrader_account_api.get_account(account_id)
        
        # Използваме RPC connection (най-бързата и евтина)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        # 1. Взимаме текущата цена на EURUSD
        price = await connection.get_symbol_price('EURUSD')
        
        # 2. Тук можеш да сложиш проверка за индикатори в бъдеще
        # Например: if price['bid'] < 1.0500: buy()

        # 3. Информация за акаунта (баланс)
        account_info = await connection.get_account_information()
        
        await connection.close()

        return {
            "status": "Success",
            "symbol": "EURUSD",
            "bid": price['bid'],
            "ask": price['ask'],
            "balance": account_info['balance']
        }

    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def home():
    # Стартираме async логиката и връщаме резултата като JSON
    result = asyncio.run(trade_logic())
    return jsonify(result)

# Тази част е само за локални тестове
if __name__ == '__main__':
    app.run()