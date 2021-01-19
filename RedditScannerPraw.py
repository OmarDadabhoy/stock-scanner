import praw
import getpass
import os
import csv
from get_all_tickers import get_tickers as gt
from praw.models import MoreComments

# This puts the CSV tickers and names into a map
def convertCSVToMap():
    # Get the path for the file with the tickers
    pathName = os.getcwd()
    pathName = pathName + "/nasdaq_screener.csv"
    file = open(pathName)
    reader = csv.reader(file, delimiter=',')
    map = {}
    # Go through each row in the file and grab all the data we need
    for row in reader:
        for column in row:
            map.update({column: 1})
    return map

# This function needs to add any stock tickers seen in sentnce into into the mapOfStocks
# sentence- The sentence that needs to parsed which possibly contains any stock tickers
# mapOfStocks - The mapping between stock tickers and the number of times they appear
# allstocks- A map of all stock tickers
def addStocks(sentence, mapOfStocks, allstocks):
    # Split the sentence into words
    splits = sentence.split()
    # Loop through each word
    for word in splits:
        newWord = word
        # if the first letter of the word is a $ get rid of it 
        if word[0:1] == "$":
            newWord = word[1:]
        # If the word is a ticker then add it to the mapOfStocks
        if allstocks.get(newWord) != None:
            if mapOfStocks.get(newWord) == None:
                mapOfStocks.update({newWord: 1})
            else: 
                mapOfStocks.update({newWord: mapOfStocks.get(newWord) + 1})

# This function processes comments for the post that is passed in
# reddit- the reddit object which allows us to communicate with reddit
# post - The thread whose comments we want to get
# mapOfStocks - The mapping between stock tickers and the number of times they appear
# allstocks- A map of all stock tickers
def processComments(reddit, post, mapOfStocks, allStocks):
    # Go through each comment and make a call to the addStocks function
    submission = reddit.submission(str(post.id))
    for comment in submission.comments:
        if isinstance(comment, MoreComments):
            continue
        addStocks(comment.body, mapOfStocks, allStocks)

# converts the stockslist into a map
def listToMap(stockslist):
    allStocks = {}
    for i in stockslist:
        allStocks.update({i: 1})
    return allStocks

# Ask user for information about their username and stuff
print("Enter your reddit username: ")
username = str(input())
print("Enter your reddit password: ")
password = getpass.getpass()
APPID = ''
APPSECRET = ''

# The reddit object which allows us to communicate with Reddit
reddit = praw.Reddit(client_id=APPID, client_secret=APPSECRET, password=password, user_agent='stock-scanner-script by ' + username, username=username)

# Ask the user what subreddits they want to go through
subreddits = []
print("Enter the subreddit/subreddits you want to index then enter done to indicate a finish: ")
sr = ""
while sr != "done":
    sr = str(input())
    subreddits.append(sr)

# Get information like time, post types, number of posts
print("Enter the type of posts you want (Ex: top, hot, controversial, new, rising)")
postType = str(input())
print("Enter the time limit of the posts you want to grab (Ex: hour, day, week, month, year, all): ")
time = str(input())
print("Enter the number of posts you want to grab from each subreddit (max = 100): ")
numberOfPosts = int(input())

# Does the user want to take the description and comments into account
print("Do you want to use the descriptions as well? (Enter y for yes and n for no): ")
useDescriptionAnswer = str(input())
useDescription = False
if useDescriptionAnswer == "y" or useDescriptionAnswer == "Y":
    useDescription = True
print("Do you want to use comments as well? (Enter y for yes and n for no): ")
useCommentsAns = str(input())
useComments = False
if useCommentsAns == 'Y' or useCommentsAns == 'y':
    useComments = True

# Create the map and get all the stocks from the csv
mapOfStocks = {}
stockslist = gt.get_tickers()
allStocks = listToMap(stockslist)

# Go through the subreddits and get the data
for s in subreddits:
    posts = None
    subreddit = reddit.subreddit(s)
    # get the posts based on the postTypes the user wants and the number they want. 
    if postType == "hot":
        posts = subreddit.hot(limit=numberOfPosts)
    elif postType == "top":
        posts = subreddit.top(limit=numberOfPosts, time_filter=time)
    elif postType == "controversial":
        posts = subreddit.controversial(limit=numberOfPosts, time_filter=time)
    elif postType == "new":
        posts = subreddit.new(limit=numberOfPosts)
    else:
        posts = subreddit.rising(limit=numberOfPosts)
    
    # Go through each post and process the title. Do description and comments if necessary.
    for post in posts:
        addStocks(post.title, mapOfStocks, allStocks)
        # Process the description
        if useDescription:
            addStocks(post.selftext, mapOfStocks, allStocks)
        # Process the comments for the post
        if useComments:
            processComments(reddit, post, mapOfStocks, allStocks)

# Sort the values of the mapofstocks and go through and print all of them in order
sortedVals = sorted(mapOfStocks.values())
seen = {}

#initialize the seen array
for key in mapOfStocks.keys():
    seen.update({key: False})

# Go through the sortedVals and print every ticker along with its value in order
for i in sortedVals:
    for key in mapOfStocks.keys():
        if mapOfStocks.get(key) == i and seen.get(key) == False:
            print(key + ": " + str(i))
            seen.update({key: True})
            break