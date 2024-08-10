import pandas as pd
import os

cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]

#combine all svo-tables into one svo-table
def unifier(folder_path, cand):
    combined_df = pd.DataFrame()
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx') and cand in filename:
            filepath = os.path.join(folder_path, filename)
            df = pd.read_excel(filepath)
            df['cand'] = cand  # add a column for the candidate

            combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

combined_df_list = []

for cand in cands:
    combined_df = unifier('data/combined_svos', cand)
    combined_df_list.append(combined_df)


final_combined_df = pd.concat(combined_df_list, ignore_index=True)

print(final_combined_df.head(3))

os.makedirs('data/combined_svos/metadata', exist_ok=True)

#table for counting genre
genrecount_df = final_combined_df['Genre'].value_counts()
output_file_genre = 'data/combined_svos/metadata/genrecount.xlsx'
genrecount_df.to_excel(output_file_genre, index=True)

#table for counting all metadata
crosstab_df = pd.crosstab(final_combined_df['cand'], final_combined_df['Genre'])
output_file = 'data/combined_svos/metadata/crosstab_genre_cand.xlsx'
crosstab_df.to_excel(output_file, index=True)

