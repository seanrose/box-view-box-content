box-view-box-content
====================

Showing how to use the Box Content API with the Box View API

## Clone the Repo

    git clone https://github.com/seanrose/box-view-box-content.git
    cd box-view-box-content

## Install the Dependencies

Install [pip](http://www.pip-installer.org/en/latest/installing.html) and [virtualenv](http://www.virtualenv.org/en/latest/#installation) if you haven't already.

Create and activate a virtual environment

    virtualenv venv --distribute
    source venv/bin/activate

Install the requirements

    pip install -r requirements.txt

## Add your credentials

In `settings.py`, update `VIEW_API_KEY` and `CONTENT_ACCESS_TOKEN` to be your own credentials. If you need a content access token quickly, you can use the [Box Token Generator](https://box-token-generator.herokuapp.com/)

## Run the app

    python app.py
