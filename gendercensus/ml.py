### find duplicate jokes
from sentence_transformers import SentenceTransformer, util
import pandas as pd

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

class tf_idf:
    
    def rm_stopwords(self, text):
        nltk.download('stopwords')
        stops = stopwords.words('english')
        new_text = ""
        
        # need to update - using single string of text here, not a collection of words
        for word in text:
            if word not in stops:
                new_text = new_text + " " + word
    
        return new_text

    def rm_symbols(self, text):
        symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~,\n"
        for symbol in symbols:
            text = str(np.char.replace(word, symbol, ' '))
        return text

    def rm_apostrophe(self, text):
        np.char.replace(text, "'", "")
        return text    
    
    # update for string input, not BoW
    def rm_singlechar(self, text):
        for word in words:
            if len(word) <= 1:
                words.remove(word)
        return text

    def convert_numbers(self, text):
        pass

    # update for input type
    def stemming(self, text):
        ps = PorterStemmer()
        for index, word in enumerate(words):
            new_word = ps.stem(word)
            words[index] = new_word


    def preprocess(self, text):
        
        # convert to lowercase
        np.char.lower(text)

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

        return words


# execute paraphrase mining
filename = 'df.csv'
df = pd.read_csv(filename)
model = SentenceTransformer('all-MiniLM-L6-v2')
column="title"

# para_df = para_mining(df=df, column=column, model=model)

# write the dataframe to a file
# para_df.to_csv(str("paraphrase_mining_", column, ".csv"))


### compute cosign similarity of selftext

# get posts text
print("converting dataframe column to array")
sentences = df["selftext"].to_numpy()
print("completed")



cos_df = pd.DataFrame(table_builder)
print("completed")

# save the dataframe to file
cos_df.to_csv("cos_df.csv")




############## pronouns 

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
