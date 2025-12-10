from flask import Flask, jsonify
import asyncio
import os
from metaapi_cloud_sdk import MetaApi

app = Flask(__name__)

# Взимаме тайните ключове от Vercel Environment Variables
token = os.environ.get('eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJlMGNlOTZjOTEwYzRhNDU5Zjg5ZmJjN2QzNzk2MTI5OSIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiZTBjZTk2YzkxMGM0YTQ1OWY4OWZiYzdkMzc5NjEyOTkiLCJpYXQiOjE3NjUzODY0NTd9.f8e1x5sdp2vH_z1Nwpj0fJ7sKbDGN31SL8cMdpTrDXklLiqaI7vcLoYQsgBr3_zgZqvr1qqMfewNE8U3e0IJcN7yhXMk2aKPK9Ykec3DiivGIPL3Cow5t_kqZ-0sgAgqnYEEAi73YDhckDSpklcvKGLHri8w2sxFSOycIwwGiu1ca7Vbd4qfpnjvY3GRtIH6zsqWNuJMdXaBoCHkSrRsB7GAGGhLZyVhsivMFubykZrZBlrADRUlCX96nCk3Mnttm569zVE0vvzgPUz-UCOx_6yTDjpBLodqUbFj5oa35fDG5FzDqclk-ihe3QgkYOP4tBW-B_ZMqr4YWttRadcSo9p9aZk0st8sEfHo0KltR8iGbQ7-UBESc0TSVtAsROYN07CWd5TgIbxi_1gfT6bUUK5QuzIRE848g-Bsj6kKomPh3lHTBMu-0c4dkqIpM8gb7SzAQ4S-mG_JXZXHJ2lzpIfyCKWPdokXykRRsJ70q4-zb2ACKQdAsaoaJB7g_9FUQUfHEznasePpyKzVWCG8QA8j6NCVcqywFMlM_buwcj7OHYmdiaV6t1qudxHrFkgFJS1cBJ8TlQTGgqK5cUPpEiG1hnpM71DDW3pPH0EuObXV5YguF5pY_n_pilmTz0HDWNXioZoZkr2rkmvS98WSxaORIQaaCiaykm04V3oxarA')
account_id = os.environ.get('1807c98f-56c0-4021-a556-7815866eb07d')

async def trade_logic():
    if not token or not account_id:
        return {"error": "Missing credentials"}

    api = MetaApi(token)
    try:
        account = await api.metatrader_account_api.get_account(account_id)
        
        # Използваме RPC връзка (най-бърза за serverless)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        # 1. Взимаме цената
        price_info = await connection.get_symbol_price('EURUSD')
        bid = price_info['bid']
        
        # --- ТУК Е ТВОЯТА СТРАТЕГИЯ ---
        # Пример: Просто връщаме цената, за да видим, че работи
        result = f"Current EURUSD Price: {bid}"
        
        # Пример за сделка (махни коментара, за да работи):
        # if bid < 1.0500:
        #     trade = await connection.create_market_buy_order('EURUSD', 0.01, 0.9000, 1.2000)
        #     result = f"Bought! {trade['orderId']}"

        await connection.close()
        return {"status": "success", "message": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/', methods=['GET', 'POST'])
def handler():
    # Стартираме async логиката
    result = asyncio.run(trade_logic())
    return jsonify(result)

# Тази част е само за локални тестове, Vercel я игнорира
if __name__ == '__main__':
    app.run()