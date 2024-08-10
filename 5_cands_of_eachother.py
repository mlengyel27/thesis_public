import pandas as pd
import os

cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]
target_cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]

cands_df = []
cands_df_list = []

# search for all the instances where the candidate mentioned the other eight candidates in the subject position
for cand in cands:
    input_filepath = f"data/combined_svos/sentiment_analysis/sentiment_freqlists/{cand}_Subject_sa_avgs.xlsx"
    df = pd.read_excel(input_filepath)
    df.insert(0, "cand", cand) #include candname in first column
    
    for target_cand in target_cands:
        if target_cand not in cand:
            for index, row in df.iterrows():
                if row['Subject'] == target_cand:
                    cands_df_list.append(row)



cands_df = pd.DataFrame(cands_df_list)

output_filepath = "data/combined_svos/sentiment_analysis/each_other"
output_filename = "cands_of_eachother_as_subjects.xlsx"
os.makedirs(output_filepath, exist_ok=True)
output_file = os.path.join(output_filepath, output_filename)
cands_df.to_excel(output_file, index=False)

