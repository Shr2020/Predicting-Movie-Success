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
    castinfo = []
    movies = pd.read_csv(file)
    for ind, movie in movies.iterrows():
        moviename = movie['Release Group']
        result = movieobj.search(moviename)
        if result:
            movieid = result[0]['id']
            details = movieobj.details(movieid)
            
            # info = {'movie': moviename, 'tmdbid': movieid, 
            # 'adult': details['adult'], 'budget': details['budget'], 
            # 'tmdb_popularity': details['popularity'], 'revenue': details['revenue'], 'runtime': details['runtime']}

            cast = details['casts']['cast']
            cast_info = {'movie': moviename, 'tmdbid': movieid, 'imdbid': details['imdb_id']}

            for i in range(5):
                if i < len(cast):
                    cast_info['actor%s' % str(i+1)] = cast[i]['name']
                    cast_info['actor%s_popularity' % str(i+1)] =  cast[i]['popularity']
                else:
                    cast_info['actor%s' % str(i+1)] = ''
                    cast_info['actor%s_popularity' % str(i+1)] =  ''
        else:
            # info = {'movie': moviename, 'tmdbid': '', 
            # 'adult': '', 'budget': '', 
            # 'tmdb_popularity': '', 'revenue': '', 'runtime': ''}
            cast_info = {'movie': moviename, 'tmdbid': '', 'imdbid': '', 
                         'actor1': '', 'actor1_popularity': '',
                         'actor2': '', 'actor2_popularity': '',
                         'actor3': '', 'actor3_popularity': '',
                         'actor4': '', 'actor4_popularity': '',
                         'actor5': '', 'actor5_popularity': ''}
        # budgetinfo.append(info)
        castinfo.append(cast_info)

    # df = pd.DataFrame(budgetinfo, columns=['movie', 'tmdbid', 'adult', 'budget', 'tmdb_popularity', 'revenue', 'runtime'])
    # df.to_csv('TMDB/tmdb_%s' % file.split('\\')[1], index=False)

    df = pd.DataFrame(castinfo, columns=['movie', 'tmdbid', 'imdbid', 'actor1', 'actor1_popularity', 'actor2', 
    'actor2_popularity', 'actor3', 'actor3_popularity', 'actor4', 'actor4_popularity', 'actor5', 'actor5_popularity'])
    df.to_csv('TMDB/tmdb_cast_%s' % file.split('\\')[1], index=False)
