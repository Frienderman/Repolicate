# Repolicate

## Demo

A demonstration of Repolicate is available on a Heroku app deployment at: [Repolicate](https://repolicate.herokuapp.com/)

## Technical Specification

See Specification.md

## Local Installation

### Prequisites

This guide assumes you have python3 and virtualenv and the instructions were tested on Linux Mint 19.2. If these packages are not installed , please run:

```bash
sudo apt-get install python3 virtualenv
```

### Running

To run this app locally perform the following steps:

#### 1. Clone Repository

Assuming you have github configured open a terminal and run:

```bash
git clone https://github.com/Frienderman/Repolicate.git
cd Repolicate
```

Alternatively you can [download](https://github.com/Frienderman/Repolicate/archive/master.zip) the Repolicate master branch .zip and unpack it in a location of your choosing then browsing to the folder unpacked (where app.py is located) and open a terminal in that location.

#### 2. Setup Virtual Environment

Setup your virtual environment by (without changing directory) running:

```bash
virtualenv -p python3 venv
. venv/bin/activate
```

#### 3. Install Requirements

Install the packages required for the app (as listed in requirements.txt) by running:

```bash
pip install -r requirements.txt
```
#### 5. OAuth settings

Login to Github's [Developer Settings](https://github.com/settings/developers) and select **OAuth Apps** from the side menu.
Click the **New OAuth App** button to generate a new app and fill in the required fields.
Note that `Authorization callback URL` will need to be the full url plus `/action` (for example: `https://repolicate.herokuapp.com/action` or `http://localhost:8000/action`) for the system to work.

#### 4. Generate app.settings

Without changing directory, generate the app.settings file by running:

```bash
echo '{ "id":"<client_id>", "secret":"<client_secret>", "target_owner":"Frienderman", "target_repo":"Repolicate" }' > app.settings
```
Where `client_id` and `client_secret` are the corresponding id and secret you have generated in OAuth Apps under Github's [Developer Settings](https://github.com/settings/developers).
`Frienderman` and `Repolicate` can be replaced with a different owner and repository name if a different repository is to be cloned.

#### 5. Run

You should now be able to start the app by running:

```bash
python app.py
```

Open a web browser and browse to [localhost:5000/](localhost:5000/) to use the app.

## Heroku Installation

##### Install Snap & Heroku CLI

Run:

```bash
sudo apt install snapd
sudo snap install heroku --classic
```

##### Heroku Login

Now open Heroku's login command:

```bash
heroku login
```

If you get an error regarding the PATH environment variable you can temporarily bypass the problem by running:

```bash
export PATH=$PATH:/snap/bin
```

Now follow the prompts to open a browser and login, once logged in the CLI should report:

```bash
Logging in... done
Logged in as username@example.com
```

##### Clone Repository

These instructions will assume you have github configured, open a terminal and clone the Repolicate repository by running:

```bash
git clone https://github.com/Frienderman/Repolicate.git
cd Repolicate
```
##### Create Heroku Project

Create a project with heroku by running:

```bash
heroku create <project_name>
```

Where `<project_name>` is a name consisting of only lowercase letters and numbers.

You will get a response similar to this:

```bash
Creating ⬢ <project_name>... done
https://<project_name>.herokuapp.com/ | https://git.heroku.com/<project_name>.git
```

##### Push App to Heroku

Now you should be able to run:

```bash
git push heroku master
```

Heroku will now proceed to perform git push and will perform a build before providing you with a message similar to:

```bash
remote:        https://repolicate.herokuapp.com/ deployed to Heroku
remote: 
remote: Verifying deploy... done.
```

The link provided should now available for use.
