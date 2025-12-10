from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():  # <-- ПРЕДИ БЕШЕ handler, ТОВА ЧУПЕШЕ VERCEL
    return jsonify({
        "status": "success",
        "message": "Hello! The bot is working correctly on Vercel."
    })

@app.route('/about')
def about():
    return "About page"