import requests
import requests.auth
import os
import csv
import getpass

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

# # This function gets the comments for the passed in thread in the subreddit
# # TODO need to get done
# def getComments(js, i, subreddit, base_url, headers):
#     linkname = js['data']['children'][i]['data']['name']
#     linkname = linkname[3]
#     commentStringFormat = "/r/" + subreddit + "/comments/" + linkname
#     payload = {}
#     postResponse = requests.get(base_url + commentStringFormat, headers=headers)
#     jsonVer = postResponse.json()
#     return jsonVer

# # This function processes comments
# #TODO need to get done
# def processComments(js, mapOfStocks, allStocks):
#     print(js)
#     # for i in range(js['data']['dist']):
#     # for list in js:
#     #     print(x)
#     return True


#constants
# Ask user for information about their username and stuff
print("Enter your reddit username: ")
username = str(input())
print("Enter your reddit password: ")
password = getpass.getpass()
APPID = ''
APPSECRET = ''
# print("Enter your APPID: ")
# APPID = str(input())
# print("Enter your app secret: ")
# APPSECRET = str(input())

# Get the access token
base_url = 'https://www.reddit.com/'
data = {"grant_type": "password", "username": username, "password": password}
auth = requests.auth.HTTPBasicAuth(APPID, APPSECRET)
r = requests.post(base_url + 'api/v1/access_token', data=data, headers={'user-agent': 'stock-scanner-script by ' + username}, auth=auth)
d = r.json()

# Make an api request to get user information
token = 'bearer ' + d['access_token']
base_url = 'https://oauth.reddit.com'
headers = {'Authorization': token, 'User-Agent': 'stock-scanner-script by ' + username}

# Ask the user what subreddits they want to go through
subreddits = []
print("Enter the subreddit/subreddits you want to index then enter done to indicate a finish: ")
sr = ""
while sr != "done":
    sr = str(input())
    subreddits.append(sr)

# Get information like time, post types, number of posts
print("Enter the time limit of the posts you want to grab (Ex: hour, day, week, month, year, all): ")
time = str(input())
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
# useComments = True

#go thorugh the subreddit and grab info we need
payload = {'t': time, 'limit': numberOfPosts}
mapOfStocks = {}
allStocks = convertCSVToMap()
for s in subreddits: 
    stringFormat = "/r/" + s + "/" + postType
    postResponse = requests.get(base_url + stringFormat, headers=headers, params=payload)
    js = postResponse.json()
    # print(js)
    # This goes through each piece in the json and only does title for now
    for i in range(js['data']['dist']):
        #title
        addStocks(js['data']['children'][i]['data']['title'], mapOfStocks, allStocks)
        #text in the post
        if useDescription:
            addStocks(js['data']['children'][i]['data']['selftext'], mapOfStocks, allStocks)
        #comments 
        # if useComments:
        #     commentsJson = getComments(js, i, s, base_url, headers)
        #     processComments(commentsJson, mapOfStocks, allStocks)


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