import spacy
import os
import pandas as pd
import textacy
from spacy.tokens import Doc
import contractions

# Load models
nlp_coref = spacy.load("en_coreference_web_trf")
nlp = spacy.load("en_core_web_trf")

#switching up characters that are non printable
def clean_text(text):
    return ''.join(char for char in text if char.isprintable())

# expand contractions:
def de_contract(text):
    return contractions.fix(text)

# the coreference resolution function source: Hacker, T. (2022). Coref in spaCy.py. GitHub. 
# Retrieved from https://gist.github.com/thomashacker/b5dd6042c092e0a22c2b9243a64a2466 (Accessed April 12, 2024)
def resolve_references(doc: Doc) -> str:
    """Function for resolving references with the coref output.
    Args:
        doc (Doc): The Doc object processed by the coref pipeline.
    Returns:
        str: The Doc string with resolved references.
    """
    token_mention_mapper = {}
    output_string = ""
    clusters = [val for key, val in doc.spans.items() if key.startswith("coref_cluster")]

    for cluster in clusters:
        first_mention = cluster[0].text
        for mention_span in list(cluster)[1:]:
            start_idx = mention_span.start
            end_idx = mention_span.end
            for token in range(start_idx, end_idx):
                if doc[token].idx not in token_mention_mapper:
                    token_mention_mapper[doc[token].idx] = ""
            token_mention_mapper[doc[start_idx].idx] = first_mention + " "

    previous_token = None
    for sent in doc.sents:
        resolved_sent = ""
        for token in sent:
            if token.idx in token_mention_mapper:
                resolved_sent += token_mention_mapper[token.idx]
            else:
                # Add space before capitalized word if previous token was a word character
                if previous_token and previous_token.is_alpha and token.text[0].isupper():
                    resolved_sent += " "
                resolved_sent += token.text + token.whitespace_
            previous_token = token
        output_string += resolved_sent.strip() + " "

    return output_string.strip()

#the whole text processing pipeline
def load_and_process_text_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read() #open all text files
            # Find genre
            print(f"Processing this filename: {filename}")
            if 'TWT' in filename:
                genre = 'tweet'
            elif 'PRES' in filename:
                genre = 'pressr'
            else:
                genre = 'debate'
            print(f"Found this genre: {genre}")


            #find date:
            date = filename[:10]

            # put texts through cleaning function
            cleaned_text = clean_text(text)

            #expand contractions
            cleaned_text = de_contract(cleaned_text)

            # resolve corefs within texts
            doc_coref = nlp_coref(cleaned_text)

            # Rload resolved texts into variable
            resolved_text = resolve_references(doc_coref)

            # process it with normal spacy model
            doc = nlp(resolved_text)

            # extract the svo list with textacy (.extend was ChatGPT's solution)
            svo_list = []
            for sent in doc.sents:
                svo_list.extend(textacy.extract.subject_verb_object_triples(sent))
            
            # check if svo-s are there, load into dataframe and save it to a new folder as individual excel files
            if svo_list:
                df = pd.DataFrame(svo_list, columns=['Subject', 'Verb', 'Object'])
                df['Genre'] = genre
                df['Date'] = date
                new_folder_path = os.path.join(folder_path, "corefresolved/svo_extractions")
                os.makedirs(new_folder_path, exist_ok=True)
                output_file = os.path.join(new_folder_path, f"{os.path.splitext(filename)[0]}.xlsx")
                df.to_excel(output_file, index=False)
                print(f"SVO extranced from: {output_file}") #communicate

cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]


for cand in cands:
    folder_path = f'data/{cand}'
    load_and_process_text_files(folder_path)
