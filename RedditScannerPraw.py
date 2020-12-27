import praw
import getpass
import os
import csv
from praw.models import MoreComments

# This puts the CSV tickers and names into a map
def convertCSVToMap():
    pathName = os.getcwd()
    pathName = pathName + "/nasdaq_screener.csv"
    file = open(pathName)
    reader = csv.reader(file, delimiter=',')
    map = {}
    for row in reader:
        for column in row:
            map.update({column: 1})
    return map

# This function needs to add any stock tickers passed in into the mapOfStocks
def addStocks(sentence, mapOfStocks, allstocks):
    splits = sentence.split()
    for word in splits:
        if allstocks.get(word) != None:
            if mapOfStocks.get(word) == None:
                mapOfStocks.update({word: 1})
            else: 
                mapOfStocks.update({word: mapOfStocks.get(word) + 1})

# This function processes comments
#TODO getting error on some subreddits when we need to get the comments where we get a 404 response. 
#TODO use a try catach block
def processComments(reddit, subreddit):
    print(str(subreddit.id))
    submission = reddit.submission(id=str(subreddit.id))
    # print("The subreddit id is: " + str(submission.comments))
    # for comment in submission.comments:
    #     if isinstance(comment, MoreComments):
    #         continue
    #     addStocks(comment.body)

    


# Ask user for information about their username and stuff
print("Enter your reddit username: ")
username = str(input())
print("Enter your reddit password: ")
password = getpass.getpass()
APPID = ''
APPSECRET = ''

reddit = praw.Reddit(client_id=APPID, client_secret=APPSECRET, password=password, user_agent='stock-scanner-script by ' + username, username=username)

# Ask the user what subreddits they want to go through
subreddits = []
print("Enter the subreddit/subreddits you want to index then enter done to indicate a finish: ")
sr = ""
while sr != "done":
    sr = str(input())
    subreddits.append(sr)

# Get information like time, post types, number of posts
# print("Enter the time limit of the posts you want to grab (Ex: hour, day, week, month, year, all): ")
# time = str(input())
print("Enter the type of posts you want (Ex: top, hot, controversial, new, rising)")
postType = str(input())
print("Enter the number of posts you want to grab from each subreddit (max = 100): ")
numberOfPosts = int(input())

# Description stuff and comments
print("Do you want to use the descriptions aas well? (Enter y for yes and n for no): ")
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
allStocks = convertCSVToMap()

# Go through the subreddits and get the data
for s in subreddits:
    posts = None
    subreddit = reddit.subreddit(s)
    # get the posts based on the postTypes the user wants and the number they want. TODO add here
    if postType == "hot":
        posts = subreddit.hot(limit=numberOfPosts)
    elif postType == "top":
        posts = subreddit.top(limit=numberOfPosts)
    
    #process the comments in subreddit
    if useComments:
            processComments(reddit, subreddit)
    # Go through each post and process the title description and comments if necessary 
    for post in posts:
        addStocks(post.title, mapOfStocks, allStocks)
        if useDescription:
            addStocks(post.selftext, mapOfStocks, allStocks)

# sort the values of the mapofstocks and go through and print all of them in order
sortedVals = sorted(mapOfStocks.values())
seen = {}

#initialize the seen array
for key in mapOfStocks.keys():
    seen.update({key: False})

for i in sortedVals:
    for key in mapOfStocks.keys():
        if mapOfStocks.get(key) == i and seen.get(key) == False:
            print(key + ": " + str(i))
            seen.update({key: True})
            break