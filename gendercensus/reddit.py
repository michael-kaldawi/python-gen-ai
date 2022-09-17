import json
import requests
import requests.auth
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

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

        access_token = response.json()['access_token'] if response.json()['access_token'] is not None else None
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
    
    def rm_stopwords(self, text):
        nltk.download('stopwords')
        stops = stopwords.words('english')
        new_text = ""
        
        for word in words:
            if word not in stop_words:
                new_text = new_text + " " + word
        
        return new_text

    def rm_symbols(self, text):
        symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~,\n"
        for symbol in symbols:
            text = str(np.char.replace(word, symbol, ''))

    def preprocess(self, text):

        # convert to lowercase
        np.char.lower(text)

        # remove stop words
        text = rm_stopwords(text)
        
        # remove symbols
        text = rm_symbols(text)
        
        # remove single characters
        for word in words:
            if len(word) <= 1:
                words.remove(word)

        # stemming
        ps = PorterStemmer()
        for index, word in enumerate(words):
            new_word = ps.stem(word)
            words[index] = new_word

        # remove symbols
        for symbol in symbols:
            for index, word in enumerate(words):
                new_word = str(np.char.replace(word, symbol, ''))
                words[index] = new_word

        return words

    def df_from_response(self, res):
        # load relevant data into a dataframe
        df = pd.DataFrame()

        # loop through each post retrieved from GET request

        for post in res.json()['data']['children']:
            # append relevant data to dataframe
            df = df.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'title_bow': self.preprocess(post['data']['title']),
                'selftext': post['data']['selftext'],
                'selftext_bow': self.preprocess(post['data']['selftext']),
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
    
    # set up the next 'after' param
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
    # df.append(new_df, ignore_index=True)

# drop duplicates
# df.drop_duplicates(subset=['title'], inplace=True, ignore_index=True)

# write dataframe to file
filename = "df.csv"
df.to_csv(filename)

### aggregate the number of each pronoun in the dataframe

# first, create a dictionary with commonly recognized pronouns
pronouns = { 
    "They": ["they", "them", "their", "theirs", "themself"],
    "She": ["she", "her", "her", "hers", "herself"],
    "He": ["he", "him", "his", "his", "himself"]
    # "Xe": ["xe", "xem", "xyr", "xyrs", "xemself"],
    # "It": ["it", "it", "its", "its", "itself"],
    # "Fae": ["fae", "faer", "faer", "faers", "faeself"],
    # "Spivak": ["e", "em", "eir", "eirs", "emself"],
    # "Ze": ["ze", "hir", "hir", "hirs", "hirself"]
    }

# next, search all retrieved titles for pronouns
all_pronouns_df = pd.DataFrame()

for pronoun_set in pronouns:
    # select rows which contain a pronoun within the current pronoun set
    pronoun_df = df[df['title_bow'].apply(lambda x: any(item in x for item in pronouns[pronoun_set]))]
    
    # add a column with the pronoun set name
    pronoun_df['title_pronoun'] = pronoun_set  

    # append the data to a dataset we will save
    all_pronouns_df = pronoun_df.copy() if all_pronouns_df.empty else pd.concat([all_pronouns_df, pronoun_df], ignore_index=True) 
    
# remove duplicate entries
# all_pronouns_df.drop_duplicates(subset=['id'] , ignore_index=True)

filename = "pronouns_df.csv"
all_pronouns_df.to_csv(filename)
