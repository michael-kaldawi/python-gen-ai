import pandas as pd
from num2words import num2words
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
from sentence_transformers import SentenceTransformer, util

class paraphrase_mining:

    def para_mining_to_df(sentences):
        # find similar titles
        paraphrases = util.paraphrase_mining(model, sentences, top_k=3, show_progress_bar=True)

        # create a dataframe with the results
        table_builder = {'sentenceA': [], 'sentenceB': [],'score': []}
        for paraphrase in paraphrases:
            score, i, j = paraphrase
            table_builder['sentenceA'].append(sentences[i])
            table_builder['sentenceB'].append(sentences[j])
            table_builder['score'].append(score)
            # para_df.append({
            #     'sentenceA': sentences[i],
            #     'sentenceB': sentences[j],
            #     'cosine_similarity': score
            # }, ignore_index=True)
        
        para_df = pd.DataFrame(table_builder)

        return para_df

    def para_mining(df, column, model):
        sentences = df[column].to_numpy()
        para_df = para_mining_to_df(sentences)
        return para_df

class preprocess:
    
    def rm_stopwords(self, text):
        stops = stopwords.words('english')
        new_text = ""
        
        words = text.split()
        for word in words:
            if word not in stops:
                new_text = new_text + " " + word
    
        return new_text

    def rm_symbols(self, text):
        symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~,‘’“”\n"
        for symbol in symbols:
            text = str(np.char.replace(text, symbol, ' '))
        return text

    def rm_apostrophe(self, text):
        return str.replace(text, "'", " ")
    
    def rm_singlechar(self, text):
        words = text.split()
        new_text = ""
        for word in words:
            if not len(word) <= 1:
                new_text = new_text + " " + word
        return new_text

    def convert_numbers(self, text):
        words = text.split()
        for word in words:
            if word.isnumeric():
                text = text.replace(word, num2words(word))
        return text

    def stemming(self, text):
        ps = PorterStemmer()
        words = text.split()
        new_text = ""
        
        for word in words:
            new_text = new_text + " " + ps.stem(word)

        return new_text

    def preprocess(self, text):
        
        # convert to lowercase
        text = str.lower(text)

        # remove symbols
        text = self.rm_symbols(text)

        # remove apostrophe
        text = self.rm_apostrophe(text)

        # remove single characters
        text = self.rm_singlechar(text)

        # convert numbers
        text = self.convert_numbers(text)

        # remove stop words
        text = self.rm_stopwords(text)

        # stemming
        text = self.stemming(text)

        # remove symbols (2)
        text = self.rm_symbols(text)

        # convert numbers (2)
        text = self.convert_numbers(text)

        return text


# execute paraphrase mining
filename = 'df.csv'
df = pd.read_csv(filename)
model = SentenceTransformer('all-MiniLM-L6-v2')
column="title"

# para_df = para_mining(df=df, column=column, model=model)

# write the dataframe to a file
# para_df.to_csv(str("paraphrase_mining_", column, ".csv"))

#### preprocessing and bow creation
posts = df[["id", "selftext"]].to_numpy()
pp = preprocess()
preprocessed_posts = []
for index, post in posts:
    p_post = pp.preprocess(post)
    p_post_bow = p_post.split()
    
    # compute tf
    # tf = {}
    # for word in p_post_bow:
    #     if tf[word] is not None:
    #         tf[word] = tf[word] + 1
    #     else:
    #         tf[word] = 1

    preprocessed_posts.append([index, p_post, p_post_bow])

columns = ['id', 'text', 'bow']
pp_df = pd.DataFrame(preprocessed_posts, columns=columns)

# # compute idf
# idf = {}
# for post in preprocessed_posts:
#     for term in post[4]:
#         if idf[term] is not None:
#             idf[term] = idf[term] + term.value()
#         else:
#             idf[term] = term.value()

# tfidf = {}
# for post in preprocessed_posts:

pp_df.to_csv("pp_df.csv")


### compute cosign similarity of selftext

# get posts text
# sentences = df["selftext"].to_numpy()
# cos_df = pd.DataFrame(table_builder)

# # save the dataframe to file
# cos_df.to_csv("cos_df.csv")