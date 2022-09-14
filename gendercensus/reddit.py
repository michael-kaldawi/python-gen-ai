import json
import requests
import requests.auth

# initialize client auth info
client_id = "38qTQMkhmlkRSUPi6wVytg"
client_token = "v5j0uuXpdq8Yg4GW78ipEbsHuXLnmA"
username = "galactic4"
password = "x0cvi4B1Q5%r"

# retrieve an access token
client_auth = requests.auth.HTTPBasicAuth(client_id, client_token)
post_data = {
        "grant_type": "password", 
        "username": username, 
        "password": password
    }
headers = {"User-Agent": "ChangeMeClient/0.1 by " + username}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

# use access token to get my info
access_token = response.json()['access_token'] if response.json()['access_token'] is not None else None
headers = {"Authorization": "bearer " + access_token, "User-Agent": "ChangeMeClient/0.1 by " + username}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

# print my info
# print(json.dumps(response.json(), indent=2))

# get some posts
headers = {"Authorization": "bearer " + access_token, "User-Agent": "ChangeMeClient/0.1 by " + username}
response = requests.get("https://oauth.reddit.com/r/jokes/top", headers=headers)

print(json.dumps(response.json(), indent=2))
