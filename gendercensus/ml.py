### find duplicate jokes
from sentence_transformers import SentenceTransformer, util
import pandas as pd

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
