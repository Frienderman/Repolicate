from flask import Flask, escape, request, redirect, jsonify, json
import requests

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
    
    #Take the OAuth response to /OAuthRequest's redirect (expecting enduser has approved app) and retrieve the code and state.

    get_request_info = request.args
    client_code = get_request_info['code']
    returned_secret = get_request_info['state']

    #With this data we perform a POST to https://github.com/login/oauth/access_token to obtain the OAuth access token.
    jsonheaders = {'Accept': 'application/json'}
    r = requests.post("https://github.com/login/oauth/access_token", data = {"client_id":"3d797b42387a734066a6", "client_secret":"602350fc855d4349dc3fd3b17453d45e844163ba", "code":client_code}, headers=jsonheaders)
    json_result = json.loads(r.text)
    #access_token = json_result['access_token']
    #access_scope = json_result['scope']
    #access_token_type = json_result['token_type']

    #Now, using the access_token we can perform functions with the Github API to clone the repository.

    return json_result

if __name__ == "__main__":
    app.run()







#example response from OAuth: http://127.0.0.1:5000/action?code=26c2736ff97da85fc8c1&state=bilbobaggins