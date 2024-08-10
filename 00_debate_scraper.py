import requests
from bs4 import BeautifulSoup
import os

# Dictionary of the 12 debate dates
debate_dates = {
    "miami-florida": "2016-03-10",
    "detroit-michigan": "2016-03-03",
    "houston-texas": "2016-02-25",
    "greenville-south-carolina": "2016-02-13",
    "manchester-new-hampshire-0": "2016-02-06",
    "des-moines-iowa-0": "2016-01-28",
    "north-charleston-south-carolina": "2016-01-14",
    "las-vegas-nevada-0": "2015-12-15",
    "milwaukee-wisconsin": "2015-11-10",
    "boulder-colorado": "2015-10-28",
    "simi-valley-california-0": "2015-09-16",
    "cleveland-ohio": "2015-08-06"
}

# Function to scrape debates from TAPP
def debate_scraper(target_cand, debate):
    debates_pages_url = f"https://www.presidency.ucsb.edu/documents/republican-candidates-debate-{debate}"
    response = requests.get(debates_pages_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    target_string = f"{target_cand.upper()}:"
    paragraphs = soup.find_all('p')
    target_paragraphs = []
    appending_toggle = False # Toggle off

    # This part creates the text files with the lines of the target candidate
    for p in paragraphs:
        text = p.get_text().strip()
        if text.startswith(target_string):
            target_paragraphs.append(p)
            appending_toggle = True # Switch toggle on
        elif appending_toggle:
            if p.find('strong'): #a new speaker marked when their name is bold
                appending_toggle = False  # Arrived at other candidate, switch toggle off
            else:
                target_paragraphs.append(p)

    filepath = f"data/{target_cand}"
    os.makedirs(filepath, exist_ok=True)
    
    debate_date = debate_dates.get(debate, "date") #.get was ChatGPT's solution
    with open(f"{filepath}/{debate_date}_DEB_{target_cand}_{debate}.txt", 'w', encoding='utf-8') as out_file:
        for paragraph in target_paragraphs:
            out_file.write(paragraph.get_text() + '\n')

    return target_paragraphs

debates = ["miami-florida", "detroit-michigan", "houston-texas", "greenville-south-carolina", "manchester-new-hampshire-0", 
           "des-moines-iowa-0", "north-charleston-south-carolina", "las-vegas-nevada-0", "milwaukee-wisconsin",
           "boulder-colorado", "simi-valley-california-0", "cleveland-ohio"]
cands = ["Bush", "Cruz", "Fiorina", "Carson", "Rubio", "Kasich", "Huckabee", "Paul", "Trump"]

for debate in debates:
    for cand in cands:
        debate_scraper(cand, debate)
