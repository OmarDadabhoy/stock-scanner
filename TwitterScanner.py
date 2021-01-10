import tweepy
from get_all_tickers import get_tickers as gt

# This function scrapes the users you type in and attempts to grab their top count tweets and process them and add them to the maps. 
def scrapeUsers(mapOfStocks, allStocks):
    # List of the accounts we want to scrap 
    usernames = []
    # how many tweets you want
    count = 150

    for name in usernames:
        try: 
            #Create query method using parameters
            tweets = tweepy.Cursor(api.user_timeline, id=name).items(count)
            # Grab the important info from the persons tweets
            tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

            for tweet in tweets_list:
                tweetDescp = tweet.text
                addStocks(tweetDescp, mapOfStocks, allStocks) 

        except BaseException as e: 
            print("failed on_status,", str(e))

# This function needs to add any stock tickers seen in sentnce into into the mapOfStocks
# sentence- The sentence that needs to parsed which possibly contains any stock tickers
# mapOfStocks - The mapping between stock tickers and the number of times they appear
# allstocks- A map of all stock tickers
def addStocks(sentence, mapOfStocks, allstocks):
    # Split the sentence into words
    splits = sentence.split()
    # Loop through each word
    for word in splits:
        # If the word is a ticker then add it to the mapOfStocks
        if allstocks.get(word) != None:
            if mapOfStocks.get(word) == None:
                mapOfStocks.update({word: 1})
            else: 
                mapOfStocks.update({word: mapOfStocks.get(word) + 1})

# converts the stockslist into a map
def listToMap(stockslist):
    allStocks = {}
    for i in stockslist:
        allStocks.update({i: 1})
    return allStocks

# Set up authentication
consumer_key = "xxx"
consumer_secret = "xxx"
access_token = "xxx"
access_token_secret = "xxxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Create the map and get all the stocks from the csv
mapOfStocks = {}
stockslist = gt.get_tickers()
allStocks = listToMap(stockslist)

scrapeUsers(mapOfStocks, allStocks)


# sort the values of the mapofstocks and go through and print all of them in order
sortedVals = sorted(mapOfStocks.values())
seen = {}

#initialize the seen array
for key in mapOfStocks.keys():
    seen.update({key: False})

# Print the stuff out
for i in sortedVals:
    for key in mapOfStocks.keys():
        if mapOfStocks.get(key) == i and seen.get(key) == False:
            print(key + ": " + str(i))
            seen.update({key: True})
            break