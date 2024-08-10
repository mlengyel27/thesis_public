import pandas as pd
import os

# Read the CSV file
df = pd.read_csv("tweets.csv")


def tweet_extract(candname):
    filepath = f"data/{candname}"
    os.makedirs(filepath, exist_ok=True)
    
    # Filter the DataFrame for the candidate
    tweets = df[df["cand"].str.contains(candname)]
    tweettexts = tweets["text"].tolist() #tolist was ChatGPT's solution
    tweetdates = tweets["date"].tolist()
    
    counter = 1
    for tweet, tweetdate in zip(tweettexts, tweetdates):
        if isinstance(tweet, str): #isinstance is ChatGPT' solution
            date_str = tweetdate.replace("/", "-")  # Ensure the date format is valid for filenames
            with open(os.path.join(filepath, f"{date_str}_TWT_{candname}_{counter}.txt"), 'w', encoding='utf-8') as out_file:
                out_file.write(tweet)
            counter += 1

# List of candidates
cands = [ "Kasich","Rubio",  "Huckabee",  "Trump", "Cruz", "Paul", "Bush", "Fiorina", "Carson"] 


for cand in cands:
    tweet_extract(cand)
