import requests
import requests.auth

# Get the access token
base_url = 'https://www.reddit.com/'
# Make sure you fix this before pushing
username = ""
password = ""
data = {"grant_type": "password", "username": username, "password": password}
APPID = ''
APPSECRET = ''
auth = requests.auth.HTTPBasicAuth(APPID, APPSECRET)
r = requests.post(base_url + 'api/v1/access_token', data=data, headers={'user-agent': 'stock-scanner-script by ' + username}, auth=auth)
d = r.json()

print(d)

# Make an api request to get user information
token = 'bearer ' + d['access_token']
base_url = 'https://oauth.reddit.com'
headers = {'Authorization': token, 'User-Agent': 'stock-scanner-script by ' + username}
response = requests.get(base_url + '/api/v1/me', headers=headers)

# if response.status_code == 200:
#     print(response.json()['name'], response.json()['comment_karma'])


#Now the code to go through wallst bets
subreddits = ['wallstreetbets']
