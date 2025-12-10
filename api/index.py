from flask import Flask, jsonify
import os
import asyncio
import traceback
# Вмъкваме библиотеката само ако е инсталирана, за да не гръмне от това
try:
    from metaapi_cloud_sdk import MetaApi
except ImportError:
    MetaApi = None

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handler():
    debug_info = {}
    
    try:
        # 1. Проверка на Environment Variables
        token = os.environ.get('METAAPI_TOKEN')
        account_id = os.environ.get('ACCOUNT_ID')
        
        debug_info['has_token'] = bool(token)
        debug_info['has_account_id'] = bool(account_id)
        debug_info['library_installed'] = (MetaApi is not None)

        if not token or not account_id:
            return jsonify({
                "status": "ERROR", 
                "message": "Missing Environment Variables in Vercel Settings",
                "debug": debug_info
            })

        if MetaApi is None:
             return jsonify({
                "status": "ERROR", 
                "message": "MetaApi library not found. Check requirements.txt",
                "debug": debug_info
            })

        # 2. Тест на Async връзката (най-рисковата част)
        async def test_connect():
            api = MetaApi(token)
            account = await api.metatrader_account_api.get_account(account_id)
            # Само четем състоянието, без да се свързваме тежко
            return account.state

        # Стартиране
        state = asyncio.run(test_connect())
        
        return jsonify({
            "status": "SUCCESS", 
            "message": "Connected to MetaApi!", 
            "account_state": state
        })

    except Exception as e:
        # ТОВА Е ВАЖНАТА ЧАСТ - Връща грешката като текст
        return jsonify({
            "status": "CRITICAL ERROR",
            "error_type": str(type(e)),
            "message": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == '__main__':
    app.run()