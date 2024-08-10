import pandas as pd
import os

 #funtcion to search for the keyword and sort by sentiment
def object_searcher(cand, keyword):
    filepath = f'data/combined_svos/sentiment_analysis/sa_{cand}_svos.xlsx'
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return None
    
    df = pd.read_excel(filepath)
    
    df = df.dropna(subset=['Subject', 'Object']) #make sure no empty values remain
    keyword_lower = keyword.lower()
    filtered_df = df[df['Object'].str.lower().str.contains(keyword_lower)].sort_values(by="Sentiment", ascending=False)
    output_file = f"data/combined_svos/sentiment_analysis/keyword/{keyword}/{cand}_{keyword}_sa_avgs_tofilter.xlsx"
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    filtered_df.to_excel(output_file, index=False)
    return output_file

#function to filter unify the tables generated
def unify(new_folder_path, folder_path, keyword):
    combined_df = pd.DataFrame()
    
    for filename in os.listdir(folder_path):
        if filename.endswith('_tofilter.xlsx'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_excel(file_path)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    filter_list = ["We", "I", "we"] #filter for just the candidates themselves and their ingroup
    filtered_df = combined_df[combined_df['Subject'].isin(filter_list)]
    
    output_file = os.path.join(new_folder_path, f"{keyword}_assubject_FILTERED.xlsx")
    filtered_df.to_excel(output_file, index=False)
    return output_file

cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]
# search all the target words
keywords = ["job", "tax", "immigration", "border", "fight", "security", "fight", "debate", "poll", "campaign", 'stand', "movement", "momentum", "opportunity", "growth", "win"]

for keyword in keywords:
    for cand in cands:
        object_searcher(cand, keyword)

    unify(f"data/combined_svos/sentiment_analysis/keyword", 
          f"data/combined_svos/sentiment_analysis/keyword/{keyword}", 
          keyword)
