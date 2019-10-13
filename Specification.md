# Repolicate

Repolicate automatically forks a configured repository to the local user's github accounts using OAuth to authenticate the user to allow for requests to the Github API to be made on the user's behalf.

Python and the web framework Flask are used to achieve this, flask is used to handle the requests used throughout.

## Environment Variables

Repolicate requires 4 environment variables `CLIENT_ID`, `CLIENT_SECRET`, `GITHUB_OWNER` and `GITHUB_REPO` these are variables that can and should be changed as required, both client_id and client_secret will need to be updated if the application is expected to run using OAuth with another user/organization.
`CLIENT_ID` and `CLIENT_SECRET` are the corresponding *Client ID* and *Client Secret* provided by Github when an OAuth app is registered (this can be found under Github's [Developer Settings](https://github.com/settings/developers) under your account. The `GITHUB_OWNER` and `GITHUB_REPO` are the target owner and repository which you with to copy, in the case of the app as is is configured in the demo that is *Frienderman* and *Repolicate* respectively.

## Endpoints

The system uses four endpoints to progress through the various stages of the code and to respond to the user's input.

#### /

This provides the welcome page to the user and provides them with a link (button) to begin the OAuth request and replication process.

#### /OAuthRequest

Receives the request to begin and generates the OAuth redirect url using the client_id from app.settings, it returns a redirect request to the enduser's browser to take them to the OAuth url it generated.

#### /action

Called as the Authorization Callback URL from Github's OAuth system, handles the response from Github which provides the client_code. A POST request is then generated using the client_code returned and the client_id and client_secret taken from app.settings. The POST response is then checked to determine if an error has occured by confirming if the dictionary response from the POST contains an `error` key. If it does then the system is forwarded to `/error`.
If it does not meet the requirements to report an error the system pulls the `access_token` from the data and provides it to an API fork request. This request is formatted to include the `target_owner` and `target_repo` from app.settings, the request is also supplied with headers to request a response in JSON and to provide the `access_token` formatted to include the required token prefix: `token <access_token>`. Once the POST request has been performed the response provided by the github API is checked to determine if the `status_code` is `200` (Accepted). If it is not then the system is forwarded to `/error`.
If passes the error check then the system assumes that the fork has completed successfully and pulls the `html_url` of the fork repository from the response and redirects the end user with the status `303` (See Other).

#### /error

If called this endpoint provides the `error.html` page to the enduser, it provides a static page with a button that will return them to `/` to restart the process.

## Github Interactions

### 1. Github OAuth

Github OAuth is handled by two endpoints, `/OAuthRequest` and `/action`;

#### OAuth Redirect

`/OAuthRequest` does not directly interact with OAuth outside of providing the user with the redirect url for them to authorize Repolicate at. The url that the enduser is redirected to is:
```https://github.com/login/oauth/authorize?response_type=code&client_id={client_id}&scope=public_repo```
Where `{client_id}` is the Repolicate OAuth client_id taken from `app.settings`.

#### Authorization Response

`/action` interacts with the response from the `/OAuthRequest` redirect (once the user has authorized, or potentially not authorized, Repolicate) where it retrieves the `client_code` from the `code` key of the authorization response.

#### Access Token Request

`/action` also performs the access_token request to:
```https://github.com/login/oauth/access_token```
This request is made with a data body containing:

```javascript
{"client_id":client_id, "client_secret":client_secret, "code":client_code}
```

Where `client_id` and `client_secret` are the Repolicate id and secret taken from `settings.app` file and the `client_code` is the 'code' taken from the authorization response (see above).
And a header containing:

```javascript
{'Accept': 'application/json'}
```

That requests the server respond with json.
Upon response the `access_token` will then be taken from the response payload for use in the Github API requests (see below).

### 2. Github API

Requests to the github API (not including OAuth) are handled by the `/action` endpoint entirely.
The fork request is the only request used by Repolicate and is a request to:
```https://api.github.com/repos/{owner}/{repository}/forks```

Where `{owner}` is the `target_owner` supplied by `settings.app` and `{repository}` is the `target_repo` supplied by `app.settings` (these settings can be altered to accept whatever repository/owner combination you wish to fork).
This request carries with it a header containing:

```javascript
{'Authorization': "token <access_token>", 'Accept': 'application/json'}
```

Where `<access_token>` is the access_token collected from the Access Token Request response processed previously.
