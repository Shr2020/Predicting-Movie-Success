import pandas as pd                        
from pytrends.request import TrendReq
import glob
import datetime
import time

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

for file in files:
    print(file)
    data = []
    movies = pd.read_csv(file)
    # movie_names = movies['Release Group'].to_list()
    for ind, movie in movies.iterrows():
        moviename = movie['Release Group']
        release_date = release_dates_map.get(moviename.lower(), None)
        if release_date and release_date < datetime.datetime.today():
            since = release_date - datetime.timedelta(weeks=1)
            pytrend = TrendReq()
            pytrend.build_payload(kw_list=[moviename], timeframe='%s %s' %(str(since.date()), str(release_date.date())))
            try:
                df = pytrend.interest_over_time()
                data.append({'movie': moviename, 'startdate': since.date(), 'releasedate': release_date.date(), 'mean_google_trend_popularity': df[moviename].mean()})
                time.sleep(0.5)
            except:
                print(moviename, release_date, "Failed")
        # print(df)
    df = pd.DataFrame(data, columns=['movie', 'startdate', 'releasedate', 'Text', 'mean_google_trend_popularity'])
    df.to_csv("GoogleTrends/gt_%s" % file.split('\\')[1], index=False, escapechar=r'|')