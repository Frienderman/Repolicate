from flask import Flask, escape, request, redirect, json
import requests

app = Flask(__name__)

#Default route for site, points to index page.
@app.route('/')
def show_index():
    with open("index.html") as file:
        return file.read()

#OAuthRequest page is activated when 'login' is clicked and makes the first request of the OAuth system.
@app.route('/OAuthRequest')
def client_auth_request():

    #Supply client_id of app from local system (for security).
    with open('app.settings') as thing:
        settings = json.load(thing)
    client_id = settings['id']

    #Send an auth request to github by generating the appropriate url and forwarding the enduser to it so they authorize the app.
    #redirect_uri not required (handled by Authorization callback URL in OAuth system).
    requesturl = "https://github.com/login/oauth/authorize?response_type=code&client_id=" + str(client_id) + "&scope=public_repo"
    return redirect(requesturl,307)

#Action is called as the Authorization callback URL in OAuth and handles turning the code into an access_token and for performing the replicate function.
@app.route('/action')
def auth_response():
    #Supply client_id of app from local system (for security).
    with open('app.settings') as thing:
        settings = json.load(thing)
    client_id = settings['id']
    client_secret = settings['secret']

    #Take the OAuth response to /OAuthRequest's redirect (expecting enduser has approved app) and retrieve the code and state.
    get_request_info = request.args
    client_code = get_request_info['code']

    #With this data we perform a POST to https://github.com/login/oauth/access_token to obtain the OAuth access token.
    json_headers = {'Accept': 'application/json'}
    r = requests.post("https://github.com/login/oauth/access_token", data = {"client_id":client_id, "client_secret":client_secret, "code":client_code}, headers=json_headers)
    json_result = json.loads(r.text)
    confirm_error = 'error' in json_result
    if confirm_error == True:
        return redirect('/error')
    access_token = json_result['access_token']

    #Now, using the access_token we can perform functions with the Github API to clone the repository. (POST /repos/:owner/:repo/forks)
    #Store owner and repo as a variable for easy modification later.
    owner_plus_repo = "Frienderman/Repolicate"
    fork_repo_url = "https://api.github.com/repos/" + owner_plus_repo + "/forks"
    fork_formatted_token = "token " + access_token
    fork_headers = {'Authorization': fork_formatted_token, 'Accept': 'application/json'}
    f = requests.post(fork_repo_url, headers=fork_headers)
    fork_result = json.loads(f.text)
    if fork_result != 202:
        return redirect('/error')
    url = fork_result['html_url']
    return redirect(url,303)

#Error route, only called if one of the requests to github/OAuth fails.
@app.route('/error')
def show_error():
    with open("error.html") as file:
        return file.read()

if __name__ == "__main__":
    app.run()