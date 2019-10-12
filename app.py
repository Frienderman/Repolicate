from flask import Flask, escape, request, redirect
import requests, jsonify

app = Flask(__name__)

@app.route('/')
def show_index():
    with open("index.html") as file:
        return file.read()

@app.route('/OAuthRequest')
def client_auth_request():

    #Send an auth request to github by generating teh appropriate url and forwarding the enduser to it so theyy authorize the app.
    #Supply redirect_uri to point them to the action page to utilize the code returned by OAuth immediately (10 minute timeout limit).
    #Supply client_id of app and a generated_secret for cross-checking later.

    client_id = "3d797b42387a734066a6"
    redirect_uri = "http://127.0.0.1:5000/action"
    generated_secret = "bilbobaggins"
    requesturl = "https://github.com/login/oauth/authorize?response_type=code&client_id=" + str(client_id) + "&redirect_uri=" + redirect_uri + "&scope=public_repo&state=" + generated_secret
    return redirect(requesturl,307)

@app.route('/action')
def auth_response():
    get_request_info = request.args
    client_code = get_request_info['code']
    returned_secret = get_request_info['state']
    
    requests.get(‘’)

    return {"ok": True}

if __name__ == "__main__":
    app.run()







#example response from OAuth: http://127.0.0.1:5000/action?code=26c2736ff97da85fc8c1&state=bilbobaggins