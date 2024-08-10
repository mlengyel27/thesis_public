from transformers import pipeline
import os
import pandas as pd

# Initialize the sentiment analysis pipeline
classifier = pipeline("text-classification", model="soleimanian/financial-roberta-large-sentiment")

def analyze_sentiment(subject, verb, obj):
    text = f"{subject} {verb} {obj}"
    prediction = classifier(text)
    return prediction[0]

def perform_sentiment_analysis(filepath):
    df = pd.read_excel(filepath)
    
    # Analyze sentiment for each row in the dataframe, lambda was ChatGPT's solution
    df['Sentiment'] = df.apply(lambda row: analyze_sentiment(row['Subject'], row['Verb'], row['Object']), axis=1)

    # Filter out rows where 'label' is 'Neutral'
    new_df_list = []
    for index, row in df.iterrows():
        if 'neutral' not in row['Sentiment']['label'].lower():
            new_df_list.append(row)

    # Create new dataframe from the filtered list
    new_df = pd.DataFrame(new_df_list)
    return new_df

def clean_results(df):
    # Clean and convert sentiment scores, lambda x was ChatGPT's solution
    df['Sentiment'] = df['Sentiment'].apply(lambda x: float(x['score']) if x['label'].lower() == 'positive' else -float(x['score']))
    df.sort_values(by=['Sentiment'], inplace=True)
    return df

def save_results(df, output_filepath, input_filepath):
    os.makedirs(output_filepath, exist_ok=True)
    output_file = os.path.join(output_filepath, f"sa_{os.path.basename(input_filepath)}")
    df.to_excel(output_file, index=False)

cands = ["Fiorina", "Huckabee", "Paul", "Carson", "Bush", "Kasich",  "Rubio",  "Trump", "Cruz"] 
for cand in cands:
    print("next:", cand)
    os.makedirs('data/combined_svos/sentiment_analysis', exist_ok=True)
    output_filepath = 'data/combined_svos/sentiment_analysis'
    input_filepath = f'data/combined_svos/sa_{cand}_svos.xlsx'

    # Do the sentiment analysis and save the cleaned results
    filtered_df = perform_sentiment_analysis(input_filepath)
    cleaned_df = clean_results(filtered_df)
    save_results(cleaned_df, output_filepath, input_filepath)
    print( output_filepath, "saved for cand: ", cand)
