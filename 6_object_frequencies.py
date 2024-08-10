import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from wordsegment import load, segment
import nltk


def obj_count(cand):
    input_file = f"data/combined_svos/sentiment_analysis/keyword/{cand}_ingroup.xlsx"
    df = pd.read_excel(input_file)
    object_list = df['Object'].tolist()

    stop_words = set(stopwords.words('english')) - {'again'} #remove "again" 
    lemmatizer = WordNetLemmatizer()
    words_not_to_lemmatize = ["ISIS", "isis"] #prevent lemmatizing isis to isi

    ind_words = []
    load()  #load segmentor
    
    counter = 0
    
    for obj in object_list:
        tokens = word_tokenize(obj.lower())
        for token in tokens:
            stripped_token = token.lstrip("#@")  #remove hash and tag in front of words

            
            # segment the hashtags and tags into individual words
            segmented_tokens = segment(stripped_token)
            
            # Process the segmented tokens
            for segmented_token in segmented_tokens:
                if segmented_token.lower() == "america": #check for the frequency of America for information purposes
                    counter += 1
                if segmented_token.isalnum() and segmented_token not in stop_words:
                    if segmented_token not in words_not_to_lemmatize:
                        ind_words.append(lemmatizer.lemmatize(segmented_token))
                    else:
                        ind_words.append(segmented_token)
        
    counts = Counter(ind_words) #counter was ChatGPT's solution
    counts_df = pd.DataFrame(counts.items(), columns=['Word', 'Count'])

    counts_df["Cand"] = cand
    counts_df = counts_df.sort_values(by='Count', ascending=False)
    
    
    output_file = f"data/combined_svos/sentiment_analysis/ingroup_object_freqlists/{cand}_object_ingroup_freqlists.xlsx"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    counts_df.head(12).to_excel(output_file, index=False) #only return the top 12 frequencies for each candidate  

    print(f"Counter for '{cand}': {counter}")  
    return counts, counter


cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]
for cand in cands:
    obj_count(cand)


combined_df = pd.DataFrame()
folder_path = "data/combined_svos/sentiment_analysis/ingroup_object_freqlists/"
    
for filename in os.listdir(folder_path):
    if filename.endswith('freqlists.xlsx'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

combined_agg_df = combined_df.groupby('Word')['Count'].sum().reset_index().sort_values(by='Count', ascending=False)
agg_output = f"data/combined_svos/sentiment_analysis/ingroup_object_freqlists/aggregated_object_freqlist.xlsx"
combined_agg_df.to_excel(agg_output, index = False)

print(combined_agg_df.head(16))

top_objects_list = []
for index, row in combined_agg_df.iterrows():
    if row['Count'] > 0:
        top_objects_list.append(row['Word'])


top_combined_list = []
for index, row in combined_df.iterrows():
    if row['Word'] in top_objects_list:
        top_combined_list.append(row)

combined_df = pd.DataFrame(top_combined_list)

output_file = os.path.join(folder_path, "unified_top_objects.xlsx")
combined_df.to_excel(output_file, index=False)

