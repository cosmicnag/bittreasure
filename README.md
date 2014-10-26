Bitcoin Treasure Hunt (BTCTREASURE)
=========



** [ Introduction ]**

BTH is an open source bitcoin treasure hunt application. The treasure is, you guessed it, Bitcoin. 
As the user unlocks each clue, he gains access to each signing key required
to unlock funds stored in a 'bounty address'.
The project consists of the following parts :

  - An API driven Django server 
  - 'Treasure Hunt' Web App
  - 'Treasure Hunt' Android App


88 [ Project Setup ]**

Install system dependencies:

### Postgres / PostGIS:

Ubuntu / Debian-based:
  sudo apt-get install postgresql-9.3 postgresql-9.3-postgis


### Python setup:

Ubuntu / Debian-based:
  sudo apt-get install python-setuptools
  sudo easy_install pip
  sudo pip install virtualenv


### Create virtualenv:

In side code folder, or wherever you like to keep your virtualenvs:

  virtualenv .
  source bin/activate  (activate virtualenv)

### Install python requirements:
(when inside virtualenv):

pip install -r requirements.txt

### Setup database:
(when inside virtualenv):

python manage.py migrate

### Run project:
(when inside virtualenv):

python manage.py runserver

