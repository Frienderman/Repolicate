# Repolicate

## Demo

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

