import requests
import requests.auth
import os
import csv

#constants
# Make sure you fix this before pushing TODO create constants as well before. 
username = ""
password = ""
APPID = ''
APPSECRET = ''

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
# TODO check if this works and see what happens
def addStocks(sentence, mapOfStocks, allstocks):
    splits = sentence.split()
    for word in splits:
        if allstocks.get(word) != None:
            if mapOfStocks.get(word) == None:
                mapOfStocks.update({word: 1})
            else: 
                mapOfStocks.update({word: mapOfStocks.get(word) + 1})
    


# Get the access token
base_url = 'https://www.reddit.com/'
data = {"grant_type": "password", "username": username, "password": password}
auth = requests.auth.HTTPBasicAuth(APPID, APPSECRET)
r = requests.post(base_url + 'api/v1/access_token', data=data, headers={'user-agent': 'stock-scanner-script by ' + username}, auth=auth)
d = r.json()

# print(d)

# Make an api request to get user information
token = 'bearer ' + d['access_token']
base_url = 'https://oauth.reddit.com'
headers = {'Authorization': token, 'User-Agent': 'stock-scanner-script by ' + username}
# response = requests.get(base_url + '/api/v1/me', headers=headers)

# if response.status_code == 200:
#     print(response.json()['name'], response.json()['comment_karma'])


#Now the code to go through wallst bets
subreddits = ['wallstreetbets']

convertCSVToMap()

#go thorugh the subreddit and grab info we need
payload = {'t': 'day', 'limit': 1}
mapOfStocks = {}
allStocks = convertCSVToMap()
for s in subreddits: 
    stringFormat = "/r/" + s + "/top"
    postResponse = requests.get(base_url + stringFormat, headers=headers, params=payload)
    js = postResponse.json()
    # print(js)
    # This goes through each piece in the json and only does title for now
    for i in range(js['data']['dist']):
        if js['data']['children'][i]['data']['title'] == '':
            continue
        addStocks(js['data']['children'][i]['data']['title'], mapOfStocks, allStocks)

