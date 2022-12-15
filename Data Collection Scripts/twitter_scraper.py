from calendar import month
from operator import index
import snscrape.modules.twitter as sntwitter
import pandas as pd
import glob
import datetime

release_dates = pd.read_csv("Release dates - data.csv")
release_dates_map = {}

folderpathrt = "rotten_info/*"
filesrt = []

for file in glob.glob(folderpathrt):
    filesrt.append(file)

for file in filesrt:
    print(file)
    movies = pd.read_csv(file)

    tweets = []
    for ind, movie in movies.iterrows():
        movien = movie['Release Group']
        if not pd.isna(movie['Release Date (Theaters)']):
            release_date = ('').join(movie['Release Date (Theaters)'].strip('[]').split(',')).replace("'", "")
            rd = datetime.datetime.strptime(release_date, "%b %d %Y")
            # if release_dates_map.get(movien.lower(), ''):
            release_dates_map[movien.lower()] = rd

folderpath = "Box Office Mojo/*"
files = []

for file in glob.glob(folderpath):
    files.append(file)

for ind, row in release_dates.iterrows():
    if row['Release-Date']:
        rd = datetime.datetime.strptime(row['Release-Date'], "%Y-%m-%d")
        if not release_dates_map.get(row['Movie'].lower(), None):
            release_dates_map[row['Movie'].lower()] = rd
    
count = 0
c = 0
for file in files:
    if '2013' in file:
        print(file)
        movies = pd.read_csv(file)

        tweets = []
        for ind, movie in movies.iterrows():
            c += 1
            query_txt = movie['Release Group']
            release_date = release_dates_map.get(movie['Release Group'].lower(), None)
            if release_date:
                count += 1
                # rd = datetime.datetime.strptime(release_date, "%Y-%m-%d")
                since = release_date - datetime.timedelta(weeks=4)
                until = release_date + datetime.timedelta(weeks=1)
                query_txt += " since:%s until:%s" % (since.date(), until.date())
                print(movie['Release Group'], release_date.date())

                for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query_txt).get_items()):
                    if i>5000:
                        break
                    tweets.append([movie['Release Group'], tweet.date, tweet.id, tweet.content, tweet.user.username])

        tweets_df = pd.DataFrame(tweets, columns=['Movie Name', 'Datetime', 'Tweet Id', 'Text', 'Username'])
        tweets_df.to_csv("Twitter/tweets_%s" % file.split('\\')[1], index=False, escapechar=r'|')
    # break
# print("Box Office ", c, count)

# folderpath = "rotten_info/*"
# files = []

# for file in glob.glob(folderpath):
#     files.append(file)

# count = 0
# c = 0
# for file in files:
#     print(file)
#     movies = pd.read_csv(file)

#     tweets = []
#     for ind, movie in movies.iterrows():
#         c += 1
#         query_txt = movie['Release Group']
#         if not pd.isna(movie['Release Date (Theaters)']):
#             release_date = ('').join(movie['Release Date (Theaters)'].strip('[]').split(',')).replace("'", "")
#             count += 1
#             rd = datetime.datetime.strptime(release_date, "%b %d %Y")
#             since = rd - datetime.timedelta(weeks=4)
#             until = rd + datetime.timedelta(weeks=1)
#             query_txt += " since:%s until:%s" % (since.date(), until.date())
#         # print(movie['Release Group'], release_date)

# print("Rotten tomatoes ", c, count)


# # Creating list to append tweet data to
# tweets_list1 = []

# # Using TwitterSearchScraper to scrape data and append tweets to list
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:jack').get_items()):
#     if i>100:
#         break
#     tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    
# # Creating a dataframe from the tweets list above 
# tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
# print(tweets_df1)

# # Creating list to append tweet data to
# tweets_list2 = []

# # Using TwitterSearchScraper to scrape data and append tweets to list
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('encanto since:2021-06-01 until:2022-07-31').get_items()):
#     if i>500:
#         break
#     tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    
# Creating a dataframe from the tweets list above

# import twint

# c = twint.Config()
# c.Search = '#blacklivesmatter'
# c.Limit = 20
# twint.run.Search(c)

# from twitter_scraper import get_tweets

# for tweet in get_tweets('twitter', pages=1):
#     print(tweet['text'])
