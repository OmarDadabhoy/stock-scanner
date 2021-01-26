# stock-scanner

This is a script which scrapes reddit for information on stocks.

## Installation

Use python's virtual environment feature to download and isolate all the packages you need for the scripts.

'''python3 -m venv venv; source venv/bin/activate; pip install requirements.txt;'''

This will create the virtual environment, activate it, and then install all needed packages

## Usage

When running either script, they will ask a series of questions which then makes calls to reddit with your information and grabs the information necessary. The difference is that the RedditScannerPraw can process comments as well making it a bit more useful in most cases.

## More notes

There are two scripts included in this. redditscanner is more primitive but adjustable and uses just the redditapi. The other being the RedditScannerPraw which does the same thing, but can also take comments into account. This is confined to the limitations of praw.
