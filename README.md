# flashcards

## Setup

* Set up a virtualenv wit `mkvirtualenv`
* `pip install -r requirements.txt`
* `./manage.py migrate`
* Copy the `.example-env` to `.env` and fill in the values
* Don't forget `./manage.py collectstatic`


## Some arbitrary notes

* Console: `python manage.py shell_plus`
* Edit deployment script: `joe /root/.bash_profile`
* `pip-compile requirements.in > requirements.txt`
