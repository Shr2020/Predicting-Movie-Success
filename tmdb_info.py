from tmdbv3api import TMDb
from tmdbv3api import Movie
import glob
import pandas as pd

tmdb = TMDb()
tmdb.api_key = 'bcbe1d25e50f5f28434c347ca911d198'

tmdb.language = 'en'
tmdb.debug = True

folderpath = "Box Office Mojo/*"
files = []

for file in glob.glob(folderpath):
    files.append(file)

gender_map = {1: 'Female', 2: 'Male'}
movieobj = Movie()


for file in files:
    budgetinfo = []
    movies = pd.read_csv(file)
    for ind, movie in movies.iterrows():
        moviename = movie['Release Group']
        result = movieobj.search(moviename)
        if result:
            movieid = result[0]['id']
            details = movieobj.details(movieid)
            
            info = {'movie': moviename, 'tmdbid': movieid, 
            'adult': details['adult'], 'budget': details['budget'], 
            'tmdb_popularity': details['popularity'], 'revenue': details['revenue'], 'runtime': details['runtime']}
        # print(result)
        else:
            info = {'movie': moviename, 'tmdbid': '', 
            'adult': '', 'budget': '', 
            'tmdb_popularity': '', 'revenue': '', 'runtime': ''}
        budgetinfo.append(info)

    df = pd.DataFrame(budgetinfo, columns=['movie', 'tmdbid', 'adult', 'budget', 'tmdb_popularity', 'revenue', 'runtime'])
    df.to_csv('TMDB/tmdb_%s' % file.split('\\')[1], index=False)