import requests
import requests.auth
import pandas as pd

class reddit:

    def __init__(self):
        # initialize default client auth info
        self.client_id = "38qTQMkhmlkRSUPi6wVytg"
        self.client_token = "v5j0uuXpdq8Yg4GW78ipEbsHuXLnmA"
        self.username = "galactic4"
        self.password = "x0cvi4B1Q5%r"
        self.access_token = self.get_access_token()

    def get_access_token(self):

        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_token)
        post_data = {
                "grant_type": "password", 
                "username": self.username, 
                "password": self.password
            }
        headers = {"User-Agent": "ChangeMeClient, 0.1 by " + self.username}
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

        access_token = response.json()['access_token']
        return access_token

    def request(self, url="https://oauth.reddit.com/api/v1/me", params=[]):
        # use access token to get my info
        headers = {"Authorization": "bearer " + self.access_token, "User-Agent": "ChangeMeClient, 0.1 by " + self.username}
        print("Making a request to the reddit api.\n",
            "url: ", url, "\n",
            "headers: ", headers, "\n",
            "params: ", params, "\n" )
        response = requests.get(url, headers=headers, params=params)

        return response
    
    def df_from_response(self, res):
        # load relevant data into a dataframe
        df = pd.DataFrame()

        # loop through each post retrieved from GET request

        for post in res.json()['data']['children']:
            # append relevant data to dataframe
            df = df.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score'],
                'created_utc': post['data']['created_utc'],
                'id': post['data']['id'],
                'kind': post['kind']
            }, ignore_index=True)
        
        return df

# instantiate params
reddit = reddit()
df = pd.DataFrame()
params = {}
params['limit'] = 100

# get 10 sets of 100 posts
for i in range(0,10):

    # request data 
    response = reddit.request(url="https://oauth.reddit.com/r/jokes/new", params=params)
    
    ### set up the next 'after' param

    # get dataframe from response
    new_df = reddit.df_from_response(response)
    # take the final row (oldest entry)
    row = new_df.iloc[len(new_df)-1]
    # create fullname
    fullname = row['kind'] + '_' + row['id']
    # add/update fullname in params
    params['after'] = fullname

    # load the new data into a dataframe
    df = new_df.copy() if df.empty else pd.concat([df, new_df], ignore_index=True) 

# drop duplicates
# df.drop_duplicates(subset=['title'], inplace=True, ignore_index=True)

# write dataframe to file
filename = "df.csv"
df.to_csv(filename)