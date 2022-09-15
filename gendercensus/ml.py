### find duplicate jokes
from sentence_transformers import SentenceTransformer, util
import pandas as pd

def para_mining_to_df(sentences):
    # find similar titles
    paraphrases = util.paraphrase_mining(model, sentences, corpus_chunk_size=len(sentences), top_k=3, show_progress_bar=True)

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
df = pd.read_csv('df.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')
para_df = para_mining(df=df, column="title", model=model)

# write the dataframe to a file
para_df.to_csv("paraphrase_mining.csv")
