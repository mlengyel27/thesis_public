import pandas as pd
import os 
import regex as re

# ChatGPT was used to generate the dictionary from example lines
same_names = {
    "we": ["\\bwe\\b", "\\bWe\\b", "\\bus\\b", "\\bUs\\b"],
    "I": ["\\bI\\b", "\\bme\\b", "\\bMe\\b", "\\bmyself\\b", "\\bMyself\\b"],
    "you": ["\\byou\\b", "\\bYou\\b"],
    "Washington": ["\\bWashington\\b", "\\bD.C\\b", "\\bWashington D.C.\\b", "\\bWashington, D.C\\b"],
    "Bush": ["\\bJeb Bush\\b", "Jeb Bush", "\\bGovernor, Bush\\b", "Governor, Bush", "\\bJeb, Bush\\b", "Jeb, Bush", "\\bGov., Bush\\b", "Gov., Bush", "\\bGOVERNOR, BUSH\\b", "GOVERNOR, BUSH", "\\bGovernor Bush\\b", "Governor Bush", "\\bBush\\b", "Bush", "Jeb"],
    "Obama": ["\\bPresident, Obama\\b", "President, Obama", "\\bObama\\b", "Obama", "\\bBarack, Obama\\b", "Barack, Obama", "\\bObama, administration\\b", "Obama, administration", "\\bObama, Admin\\b", "Obama, Admin", "\\b@POTUS\\b", "@POTUS", "\\bPOTUS\\b", "POTUS", "\\bObama administration\\b", "Obama administration",  "\\bObama\\b", "Obama", "\\bBarack\\b", "Barack"],
    "Hillary": ["\\bHillary Clinton\\b", "Hillary Clinton", "\\b@HillaryClinton\\b", "@HillaryClinton", "\\b.@HillaryClinton\\b", ".@HillaryClinton", "\\bHillary\\b", "Hillary", "\\bHillary, Clinton\\b", "Hillary, Clinton", "\\bHillary\\b", "Hillary"],
    "Trump": ["\\bDonald, Trump\\b", "Donald, Trump", "\\bDonald J, Trump\\b", "Donald J, Trump", "\\bDonald J Trump\\b", "Donald J Trump", "\\bTrump\\b", "Trump", "\\b@realDonaldTrump\\b", "@realDonaldTrump", "\\b@RealDonaldTrump\\b", "@RealDonaldTrump", "\\bTRUMP\\b", "TRUMP", "\\b@realdonaldtrump\\b", "@realdonaldtrump", "\\b.@realDonaldTrump\\b", ".@realDonaldTrump"],
    "Cruz": ["\\bCruz\\b", "Cruz", "\\bSenator Cruz\\b", "Senator Cruz", "\\bSen. Cruz\\b", "Sen. Cruz", "\\bSenator, Cruz\\b", "Senator, Cruz", "\\b@tedcruz\\b", "@tedcruz", "\\bCRUZ\\b", "CRUZ", "\\bSen., Cruz\\b", "Sen., Cruz"],
    "Fiorina": ["\\bCarly Fiorina\\b", "Carly Fiorina", "\\bCarly, Fiorina\\b", "Carly, Fiorina", "\\bFiorina\\b", "Fiorina", "\\b@CarlyFiorina\\b", "@CarlyFiorina", "\\bFIORINA\\b", "FIORINA", "\\b@carlyfiorina\\b", "@carlyfiorina"],
    "Carson": ["\\bCarson\\b", "Carson", "\\bDr. Carson\\b", "Dr. Carson", "\\b@RealBenCarson\\b", "@RealBenCarson", "\\bCARSON\\b", "CARSON", "\\bDr., Carson\\b", "Dr., Carson", "\\b@realbencarson\\b", "@realbencarson"],
    "Rubio": ["\\bMarco Rubio\\b", "Marco Rubio", "\\bSenator, Marco, Rubio\\b", "Senator, Marco, Rubio", "\\bMarco\\b", "Marco", "\\bRubio\\b", "Rubio", "\\bSenator Rubio\\b", "Senator Rubio", "\\bSen. Rubio\\b", "Sen. Rubio", "\\b@marcorubio\\b", "@marcorubio", "\\bRUBIO\\b", "RUBIO", "\\bMarco, Rubio\\b", "Marco, Rubio", "\\bSen., Rubio\\b", "Sen., Rubio", "\\bSenator, Rubio\\b", "Senator, Rubio"],
    "Kasich": ["\\bKasich\\b", "Kasich", "\\bGovernor Kasich\\b", "Governor Kasich", "\\bGovernor, Kasich\\b", "Governor, Kasich", "\\bGov. Kasich\\b", "Gov. Kasich", "\\bGov., Kasich\\b", "Gov., Kasich", "\\b@JohnKasich\\b", "@JohnKasich", "\\bKASICH\\b", "KASICH", "\\bGov., Kasich\\b", "Gov., Kasich", "\\b@johnkasich\\b", "@johnkasich"],
    "Huckabee": ["\\bHuckabee\\b", "Huckabee", "\\bMike Huckabee\\b", "Mike Huckabee", "\\bMike, Huckabee\\b", "Mike, Huckabee", "\\bHuckabee\\b", "Huckabee", "\\bGovernor Huckabee\\b", "Governor Huckabee", "\\bGov. Huckabee\\b", "Gov. Huckabee", "\\b@GovMikeHuckabee\\b", "@GovMikeHuckabee", "\\bHUCKABEE\\b", "HUCKABEE", "\\bGov., Huckabee\\b", "Gov., Huckabee", "\\b@govmikehuckabee\\b", "@govmikehuckabee"],
    "Paul": ["\\bPaul\\b", "Paul", "\\bSenator Paul\\b", "Senator Paul", "\\bSen. Paul\\b", "Sen. Paul", "\\b@RandPaul\\b", "@RandPaul", "\\bPAUL\\b", "PAUL", "\\bSenator, Paul\\b", "Senator, Paul", "\\bSen., Paul\\b", "Sen., Paul", "\\b@randpaul\\b", "@randpaul"]
}

#substitute the synonyms
def resolve_synonyms(df, name_dict):
    for name, synonyms in name_dict.items():
        for synonym in synonyms:
            # the lambda function was ChatGPT's solution
            df['Subject'] = df['Subject'].apply(lambda x: name if re.search(synonym, x) else x)
    return df

#strip brackets that were automatically added by the SVO extractor
def strip_brackets(text):
    return re.sub(r'\[|\]', '', str(text))

def combine_excel_files(folder_path, output_file, name_dict):
    combined_df = pd.DataFrame()

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(folder_path, filename)
            # Read the Excel file into a DataFrame
            df = pd.read_excel(filepath)

            # Strip brackets from Subject, Verb, and Object columns
            df['Subject'] = df['Subject'].apply(strip_brackets)
            df['Verb'] = df['Verb'].apply(strip_brackets)
            df['Object'] = df['Object'].apply(strip_brackets)

            # Append the DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Drop duplicates
    combined_df.drop_duplicates(inplace=True)

    # Resolve synonyms
    combined_df = resolve_synonyms(combined_df, name_dict)

    # Save the combined df to excel
    combined_df.to_excel(output_file, index=False)

# Create folder paths
cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]

for cand in cands:
    folder_path = f"data/{cand}/corefresolved/svo_extractions"
    output_folder = f"data/ombined_svos/"
    os.makedirs(output_folder, exist_ok=True)
    output_filename = f"{cand}_svos.xlsx"
    output_file = os.path.join(output_folder, output_filename)
    if os.path.exists(folder_path): #communicate
        print(f"{folder_path}")
        combine_excel_files(folder_path, output_file, name_dict=same_names)
        print(f"{output_file} done")
    else:
        print(f"{folder_path} not found.")