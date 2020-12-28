# stock-scanner

This is a script which scrapes reddit for information on stocks.

## Installation

Use the package manager pip to install praw and requests from the command line.

'''bash 
pip install praw
pip install requests
'''
## Usage
When running either script, they will ask a series of questions which then makes calls to reddit with your information and grabs the information necessary. The difference is that the RedditScannerPraw can process comments as well making it a bit more useful in most cases. 

## More notes
There are two scripts included in this. redditscanner is more primitive but adjustable and uses just the redditapi. The other being the RedditScannerPraw which does the same thing, but can also take comments into account. This is confined to the limitations of praw. 
