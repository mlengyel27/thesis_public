import pandas as pd
import os
import time
import numpy as np

def sent_avgs(cand, position, filepath):
    df = pd.read_excel(filepath)

    # Calculate mean, frequency, weighted sentiment
    stats = df.groupby([f'{position}'])['Sentiment'].agg(['mean', 'count'])
    stats['normalized'] = (stats['count'])
    stats['weighted_sentiment'] = round(stats['mean'] * stats['normalized'], 3) #include just 3 decimals

    stats = stats.sort_values(by='count', ascending=False) # sort by count
    output_file = f"data/combined_svos/sentiment_analysis/sentiment_freqlists/{cand}_{position}_sa_avgs.xlsx"
    stats.to_excel(output_file, index=True)

#loop thorugh the candidates in subject position
cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]
positions = ["Subject"]

#try to execute the function with possibility to wait for the sentiment analysis script to create the files
#solution from StackOverflow at https://stackoverflow.com/a/54506198
for cand in cands:
    filepath = f'data/combined_svos/sentiment_analysis/sa_{cand}_svos.xlsx'
    for position in positions: 
        time_to_wait = 1000  #set waiting time
        time_counter = 0 
        while not os.path.exists(filepath) and time_counter < time_to_wait:
            time.sleep(8)
            time_counter += 1
        if os.path.exists(filepath):
            sent_avgs(cand, position, filepath)
