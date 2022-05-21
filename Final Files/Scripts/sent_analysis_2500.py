import pandas as pd
import numpy as np
import string
import re
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import  argparse
from langdetect import detect

class MovieSentiment:
    def __init__(self, name):
        self.movie_name = name
        self.pos = 0
        self.n = 0
        self.neg = 0
        self.tweets = 0
    
    def print_summary(self):
        print("Movie:", self.movie_name, "| Tweets analysed:", self.tweets,  "| Postive:", self.pos, "| Negative:", self.neg, "| Neutral:", self.n)
    
# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):
    try:
        sid_obj = SentimentIntensityAnalyzer()
        
        sentiment_dict = sid_obj.polarity_scores(sentence)
        overall_sent = 0
        if sentiment_dict['compound'] >= 0.05 :
            overall_sent = 1
        elif sentiment_dict['compound'] <= - 0.05 :
            overall_sent = -1
        else :
            overall_sent = 0
    except Exception as e:
        print("in Sent score:", e)
        return -2
    return overall_sent

def write_to_file(movies, movie_class, res_file):
    llist = []
    for m in movies:
        m_obj = movie_class[m]
        llist.append([m_obj.movie_name, m_obj.tweets, m_obj.pos, m_obj.n, m_obj.neg])
    df = pd.DataFrame(llist, columns =['Movie', 'Total Tweets', 'Positive Tweets', 'Neutral Tweets', 'Negative Tweets'])
    df.to_csv(res_file, mode='a')
    
def write_movie_to_file(m_obj, res_file):
    llist=[]
    llist.append([m_obj.movie_name, m_obj.tweets, m_obj.pos, m_obj.n, m_obj.neg])
    df = pd.DataFrame(llist, columns =['Movie', 'Total Tweets', 'Positive Tweets', 'Neutral Tweets', 'Negative Tweets'])
    df.to_csv(res_file, mode='a', index=False, header=False)

def write_first_movie_to_file(m_obj, res_file):
    llist=[]
    llist.append([m_obj.movie_name, m_obj.tweets, m_obj.pos, m_obj.n, m_obj.neg])
    df = pd.DataFrame(llist, columns =['Movie', 'Total Tweets', 'Positive Tweets', 'Neutral Tweets', 'Negative Tweets'])
    df.to_csv(res_file, mode='a', index=False)

def cleanup(tweet):
    s = re.sub(r'@\S+', '', tweet)
    s = re.sub(r'http\S+', '', s)
    return s

def sentiment_analysis_and_store(tweets_file, res_file):
    movies = []
    movie_class = {}
    with open(tweets_file, 'r', encoding="ISO-8859-1") as file:
        csvreader = csv.reader(file)
        line_count = 0
        processed_tweets = 0
        for row in csvreader:
            if (len(row) < 5):
                continue
            
            if line_count < 1:
                print(row)
                line_count+=1
                continue
            
            movie_name = row[0]
            
            tweet = row[3]
            if tweet == "":
                continue
            
            if processed_tweets >= 2500 and movie_name in movies:
                continue;
            if movie_name not in movies:
                movie_class[movie_name] = MovieSentiment(movie_name)
                if len(movies) > 1:
                    write_movie_to_file(movie_class[movies[-1]], res_file)
                    processed_tweets = 0
                elif len(movies) == 1:
                    write_first_movie_to_file(movie_class[movies[-1]], res_file)
                    processed_tweets = 0
                movies.append(movie_name)

            try:
                tweet = cleanup(tweet)
                lang = detect(tweet)
                if (lang != 'en'):
                    continue
            except Exception as e:
                print("lang detect error:", e)
                continue
            if tweet == "":
                continue

            overall_sent = sentiment_scores(tweet)
            if (overall_sent == -2):
                continue
            
            if overall_sent == 1:
                movie_class[movie_name].pos += 1
            elif overall_sent == -1:
                movie_class[movie_name].neg += 1
            elif overall_sent == 0:
                movie_class[movie_name].n += 1
            
            movie_class[movie_name].tweets += 1
            line_count += 1
            processed_tweets += 1
            
            if (line_count % 1000 == 0):
                print("Processed tweet: ", line_count, "\n")
    print(f'Processed {line_count - 1} lines.')
    file.close()

parser = argparse.ArgumentParser(description='Twitter sentiment analysis')
parser.add_argument('-year', '--year', metavar='YEAR', default='2010')

def main():
    args = parser.parse_args()
    path = 'Twitter'
    files = os.listdir(path)
    year = args.year
    print("file started.")
    for file in files:
        yr = file.split("_")[1].split(".")[0]
        if yr == year:
            file_path = os.path.join(path, file)
            res_filename = "Vader_2500_res"+year+".csv"
            sentiment_analysis_and_store(file_path, res_filename)
            print("Processing Done For:", file, "\n")

if __name__ == '__main__':
    main()
