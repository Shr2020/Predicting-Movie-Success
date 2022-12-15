## Objective
A prediction system that will aid in forecasting the success of a movie during the early stages of its release. We will be experimenting with movies over 10 years hoping to reach a benchmark in predicting movie profitability by a considerable margin. We are using features such as budget, actors, director, producer, IMDb rating, IMDb Metascore, IMDb vote count, rotten tomatoes score, actors and director social fan following, Twitter reactions, etc.  

#### Datasets -
Dataset includes movies from years 2010-2022. Data was collected from the following sources during multiple phases of data collection - 
1. IMDb - Movie Title, Average user ratings, Run-time of the film, Film year, Budget
2. Rotten Tomatoes - Movie Title, Director, Producer, Rotten Score, Audience Score, Rating, Genre, Box Office Gross Collections
3. Box Office Mojo - Movie Title, Worldwide collections, Domestic Collections, Foreign Collections, Percentage
4. Twitter - Movie Title, Sentiment of overall tweets, Number of positive tweets, Number of negative tweets, Number of neutral tweets
5. TMDb -  Movie Title, Tmdbid, Imdbid, Adult, Budget, Tmdb Popularity, Revenue, Runtime, Actor1, Actor1 Popularity, Actor2, Actor2 Popularity, Actor3, Actor3 Popularity, Actor4, Actor Popularity, Actor5, Actor5, 5.Popularity, Director Popularity, Producer Popularity
6. Wikipedia - Release Dates, Budget
7. Google Trends - Movie Title, Google trend popularity in the week before its release

#### Data Preparation - 
1. For Twitter Data VADER library is used for analyzing tweets. 2500 tweets for each movie were analysed. VADER provides positive, negative, and neutral tweets for each movie. A mean of the number of positive and negative tweets was taken to generate a Twitter Score that we used as a feature. 
2. For Google Trends data, the mean of the data collected for each movie is calculated. 
3. The missing values in the data set are imputed in 3 different ways to create three separate datasets:
  1. Mode for movie rating, the mean value for other features.
  2. Mode for movie rating, the median value for other features.
  3. Mode for movie rating, rotten scores as 50 (since the scores are from 1-100), and mean for the rest of them.
4. Preliminary experiments showed that both 1 and 2 gave the same results and 3 did not give better results than the other two. Therfore approach 1 was used for imputation. 
5. Data normalization was done using min-max normalization. One hot encoding was performed on all categorical data like genres, release week, release day, etc.
6. DBSCAN was used to detect the outliers (before normalization) in the dataset. The total outliers came out to be 392.

7. Three different approaches were used after preparing the data - 
 1. Using the whole dataset for regression. 
 2. employing feature selection to select some features, and then performing regression. 
 3. performing feature reduction using PCA, and then performing regression. 

8. These three approaches were applied to two types of datasets: 
 1. pure dataset
 2. dataset with outliers removed. 
 
9. The experiments did not show promising results when outliers were removed so all experiments performed on the dataset without the removal of outliers.

10. With PCA the minimum number of features that could explain the 95% of variance came out to be near 30. Therefore, the total features for this approach were taken as 30.

11. For Feature Selection 6 algorithms were implemented to condense the number of features - Random Forest Regressor, Sequential Backward Selection, Sequential Forward Selection,  Mutual Information Method, and Fischer Score: Chi-Square and Constant Feature elimination. 

#### Modeling
To obtain a projected revenue, eight algorithms were used - Linear Regression, Random Forest, LGB, Gradient Boosting Regressor, Support Vector Machine, Decision Tree regressor, XGBoost, and DNN. Best results were obtained when the dataset was used without removing the outliers.


## Details
- The Folder "Data Collected" consists all the data collected through web scraping and processing etc.
- The Folder "Data Collection Scripts" consists of pythons scripts for scraping/collecting data from all data sources.
- The Folder "Final Dataset CSV" consists two files which have the total data we will be running our algorithms on. The Data_Modelling Files work on the "may-movie-data-final.csv". The File "FinalDataset.csv" is after some processing done in the modelling files.
- Data_Modeling*.ipynb files have been used to run exploratory data analysis, feature selection and feature reduction along with the ML models. These can be re-run to recreate the results of our study. 
- Data_Modelling_Mean_Values.ipynb -> Feature selection, feature reduction and data modeling run when the missing values are imputed with the mean values.
- Data_Modelling_Median_Values.ipynb -> Feature selection, feature reduction and data modeling when the missing values are imputed with the median values.
- Data_Modelling_Mean_Values_And_Outliers_Removed.ipynb - Feature selection, feature reduction and data modeling when the missing values are imputed with the mean values and outliers are removed.

