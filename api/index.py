from flask import Flask, jsonify
import asyncio
from metaapi_cloud_sdk import MetaApi

app = Flask(__name__)

# --- ВНИМАНИЕ: ТОВА Е САМО ЗА ТЕСТ ---
# Изтрий os.environ и сложи данните в кавички директно тук:

token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJlMGNlOTZjOTEwYzRhNDU5Zjg5ZmJjN2QzNzk2MTI5OSIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiZTBjZTk2YzkxMGM0YTQ1OWY4OWZiYzdkMzc5NjEyOTkiLCJpYXQiOjE3NjUzODkwNTh9.i0kdJOYxiOTaTRm6yfDCM9-Wj8aIlmIokLa-mtiEVKGZz1J7c6armYA2GbJrOfr747lgSicDMyJe_RZ0E_Z51L_3Uu_eSbQrmMzU_Z0uyPQgyTMZnRpLGULKoZ17hefdOuQM3tKSohCAVdAUpZShK9QUyPW3Rq_VCzyMLxNj-ZHSECBTz51n6PjxWilBZVMuxSr9fgcM6-6STPLlYXIyM4VbHku0a5uSBl5afyxFu7TRXSC0dP47hOJpi-v7IkImu6VlL4F-WY9sf3yKTtmcoKYbvxNlQJHt8-s6tpGX3aLAEUathl5cvb7pjQVtUO8Xhhso1X65rCo62NxnbHX_sN7MurGzyBtUqRwl2gnawUme8nQIJP61gi9yquplKKkAImml0wirCMDeLXyDuf-URDojEYOMHEEb-HgtaV-78FNF1vQhSO8M-l2xyvjCWtZiJa4P_tcVlwFMTAr1Ji2pDE6VZN6-rw9388mt_z7ntKo2aHoJZo0HQ-de3TPP21DPxJXJuEHt0GPvUtm-LdWZontLQyLjZMVtE9HW84gPG5S8xE0wVHT-Zx-rv9W50skIUHYlFj4-T7fhhv2uQpv-SumS7tP5oOOxnbb4TP9MMC7t1nqhEuI5FoWkT6zQI33-3RHaPsQ4zeP7KGl7ILRGPsjLHKd6QSUnudYrr125vz0" 
account_id = "1807c98f-56c0-4021-a556-7815866eb07d"

# Увери се, че са в кавички! Пример:
# token = "MAPI-asd987f..."
# account_id = "abc-123..."
# -------------------------------------

async def trade_logic():
    # Вече няма нужда от проверки дали са празни, защото ги виждаш
    
    api = MetaApi(token)
    try:
        account = await api.metatrader_account_api.get_account(account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        price = await connection.get_symbol_price('EURUSD')
        account_info = await connection.get_account_information()
        
        await connection.close()

        return {
            "status": "Success - Hardcoded Works!",
            "symbol": "EURUSD",
            "bid": price['bid'],
            "balance": account_info['balance']
        }

    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def home():
    result = asyncio.run(trade_logic())
    return jsonify(result)