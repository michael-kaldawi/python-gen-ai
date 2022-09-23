
import pandas as pd
import numpy as np

############## pronouns 
filename = 'df.csv'
df = pd.read_csv(filename)

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