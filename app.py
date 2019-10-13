from flask import Flask, escape, request, redirect, json
import requests

app = Flask(__name__)

#Default route for site, points to index page.
@app.route('/')
def show_index():
    with open("index.html") as file:
        return file.read()

#OAuthRequest page is activated when 'login' is clicked and makes the redirect to the OAuth system.
@app.route('/OAuthRequest')
def client_auth_request():

    #Supply client_id of app from local system (for security).
    with open('app.settings') as thing:
        settings = json.load(thing)
    #client_id = settings['id']

    #Send an auth request to github by generating the appropriate url and forwarding the enduser to it so they authorize the app.
    #redirect_uri not required (handled by Authorization callback URL in OAuth system).
    requesturl = "https://github.com/login/oauth/authorize?response_type=code&client_id=" + settings['id'] + "&scope=public_repo"
    return redirect(requesturl,307)

#Action is called as the Authorization callback URL in OAuth and handles turning the code into an access_token and for performing the replicate function.
@app.route('/action')
def auth_response():
    #Supply client_id of app from local system (app.settings) (for security).
    with open('app.settings') as thing:
        settings = json.load(thing)

    #Take the OAuth response to /OAuthRequest's redirect (expecting enduser has approved app) and retrieve the code and state.
    get_request_info = request.args
    client_code = get_request_info['code']

    #With this data we perform a POST to https://github.com/login/oauth/access_token to obtain the OAuth access token.
    json_headers = {'Accept': 'application/json'}
    r = requests.post("https://github.com/login/oauth/access_token", data = {"client_id":settings['id'], "client_secret":settings['secret'], "code":client_code}, headers=json_headers)
    json_result = json.loads(r.text)
    #Check if 'error' key exists in json_result, if it does then something has gone wrong so go to error page.
    confirm_error = 'error' in json_result
    if confirm_error == True:
        return redirect('/error')
    access_token = json_result['access_token']

    #Now, using the access_token we can perform functions with the Github API to clone the repository. (POST /repos/:owner/:repo/forks)
    #Target Repo and Owner are contained in app.settings, pull them out for use in fork.
    fork_repo_url = "https://api.github.com/repos/" + settings['target_owner'] + "/" + settings['target_repo'] + "/forks"
    fork_formatted_token = "token " + access_token
    fork_headers = {'Authorization': fork_formatted_token, 'Accept': 'application/json'}
    f = requests.post(fork_repo_url, headers=fork_headers)
    fork_result = json.loads(f.text)
    #Check if status code 202 is reported, if not, something has gone wrong so go to error page.
    if f.status_code != 202:
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