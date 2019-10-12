from flask import Flask, escape, request
import requests, jsonify

app = Flask(__name__)

@app.route('/')
def show_index():
    with open("index.html") as file:
        return file.read()

@app.route('/OAuthRequest')
def client_auth_request():
    return {"ok": True}

if __name__ == "__main__":
    app.run()
