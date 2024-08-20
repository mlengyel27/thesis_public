This repository contains the scripts of my Quantitative Narrative Analysis pipeline built for my Masters Thesis research at KU Leuven. Scripts titled in order of execution. All scripts are written by me, outside sources are referenced in the comments.

**Scripts used for data collection**

*00_debate_scraper.py*  extracts the texts of the 12 Republican primary debates of 2016 from the website of the American Presidency Project. It sorts the lines by candidate and saves them as .txt files with their genre and date included in the filename.

*00_campaign_scraper.py* extracts campaign press releases from the website of the American Presidency Project based on customizable parameters and saves them as .txt files with their genre and publication date included in the filename.

*00_rdsconverter.R*  	converts the tweets.rds file into a .csv file.

*00_tweetsorter.py* 	extracts the tweets and dates from the tweets.csv file, sorts them by candidate, and saves their text as .txt files with the genre and publication date included in the filename.

**Scripts used for preprocessing**

*1_preprocess_svo_extract.py*   processes the individual .txt files by removing non-printable characters, putting them through the Spacy NLP pipeline, expanding contractions, resolving coreferences, extracting the SVO-triplets, adding columns for genre and date, and then saving them as .xlsx files.

*2_svo_unifier.py*  	unifies the individual files per candidate into one .xlsx file, merges synonyms, removes the square brackets added by the SVO-extractor, and removes duplicate entries.
	
**Scripts used for analysis**

*3_sentiment_analysis.py*  	runs the unified .xlsx files through the sentiment analysis model, drops the neutral values, and saves the results as .xlsx files.

*4_sentiment_frequencies.py*  	calculates the average sentiment, frequency, and weighted sentiment for the triplets of the candidates in the subject position, then saves the output as .xlsx files.

*5_cands_of_eachother.py*  reads the resulting .xlsx files of every candidate, filters for rows where the other eight candidates are in the Subject position, combines and saves these into a new .xlsx file.

*6_object_frequencies.py*  	preprocesses the object column of each candidate’s SVO-table by tokenizing, removing stopwords, and lemmatizing the words. It then saves the 20 most frequent ones into a new .xlsx file for every candidate, unifies these files, aggregates the word counts, filters for objects with over 5 occurrences, and saves the results in a new .xlsx file.

*7_object_searcher.py*  	combines the SVO-triplets of each candidate that contains a given keyword in the object position into a single .xlsx file and filters for the rows that contains the candidates and their ingroups as subjects.
	
**Scripts used to collect metadata on the dataset**

*metadata.py*  	combines the unified .xlsx SVO-tables into a single file, generates, and saves two reports on the count of each genre and the cross-tabulation of candidates by genre.

