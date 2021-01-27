#Directions:
# 1. Create venv: 
#       >>> python3 -m venv MusicGenreClassifier
# 2. Activate venv: *before entering MusicGenreClassifier*
#       >>> source MusicGenreClassifier/bin/activate
# 3. Run spotipy(two options):
#       a. command line:
#           >>> export SPOTIPY_CLIENT_ID=your client id
#           >>> export SPOTIPY_CLIENT_SECRET=your client secret
#           >>> export SPOTIPY_REDIRECT_URI='http://google.com/'
#       b. from path /MusicGenreClassifier/lib/python3.8/site-packages/spotipy/oauth2.py:
#           enter your client id and client secret in lines 144 and 145 
# 4. Run code:
#       >>> python3 GenreClassifier.py
# 5. Deactivate venv: 
#       >>> deactivate

import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold

sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials())

genre_arr = ['pop', 'rock', 'latin', 'rap', 'edm', 'r&b', 'country']
playlist = '''6gS3HhOiI17QNojjPuPzqc 7dowgSWOmvdpwNkGFMUs6e 1IGB0Uz7x2VY28qMagUC24 6s5MoZzR70Qef7x4bVxDO1 3pDxuMpz94eDs7WFqudTbZ 1rLnwJimWCmjp3f0mEbnkY 4mijVkpSXJziPiOrK7YX4M'''.split()
columns = ['track_id', 'mode', 'tempo','danceability','energy','loudness','valence', 'acousticness','liveness', 'instrumentalness', 'speechiness', 'genre']

index = []
to_append = []


#gathering playlist data
#
#
for g in zip(genre_arr, playlist):
    #list of playlist id's
    track_ids = sp.user_playlist_tracks('thesoundsofspotify', playlist_id = g[1], fields ='items(track(id))') 
    # lists of track ids per playlist 
    tracks_list = []    
    for track in track_ids['items']:
        tracks_list.append(track['track']['id'])
    
    # getting the audio features and information of 50 trakcs at a time
    info = sp.tracks(tracks_list[:50])  
    features = sp.audio_features(tracks_list[:50])
    for track in range(0, 50):
        track_data = []
        index.append(info['tracks'][track]['name'])        
        track_data.append(info['tracks'][track]['id'])
        track_data.append(features[track]['mode']) 
        track_data.append(features[track]['tempo'])        
        track_data.append(features[track]['danceability'])
        track_data.append(features[track]['energy'])
        track_data.append(features[track]['loudness'])
        track_data.append(features[track]['valence'])      
        track_data.append(features[track]['acousticness'])
        track_data.append(features[track]['liveness']) 
        track_data.append(features[track]['instrumentalness'])
        track_data.append(features[track]['speechiness'])     
        
        track_data.append(g[0])      
        to_append.append(track_data)
    audio_data = pd.DataFrame(to_append, index = index, columns = columns)
    audio_data.drop_duplicates(keep = False, inplace = True)      


#Perform EDA on the audio features and find each column's variance.
#To demonstrate how some of the features differ between genre groups, the audio features 
#This will allow us to see which audio attribute differs the most between genres, as well as which audio attribute has the most similarities.
#
def EDA(data):
    #Group dataset by genre and finding each attribute's mean
    data_mean = data.groupby(['genre']).mean()
    normalized_data = data_mean.apply(lambda x: x/x.max(), axis=0)
    # Get the variances of each column and put each value in an array
    selector = VarianceThreshold()
    selector.fit_transform(normalized_data)
    variances = selector.variances_
    # Create a row to be appended to the dataframe
    new_row = pd.DataFrame(variances.reshape(-1, len(variances)), columns = normalized_data.columns)
    # Add the row, then sort the columns by variance (descending)
    normalized_data = normalized_data.append(new_row).rename({0: 'variance'})
    normalized_data = normalized_data.sort_values(by = 'variance', ascending = False, axis = 1)


#standardize features by removing the mean and scaling to unit variance
le_y = LabelEncoder()
X = audio_data.drop(columns = ['track_id', 'genre'], axis = 1)
scaler = preprocessing.StandardScaler().fit(X)
X = scaler.transform(X)

# Implementing randoom forest tree classifier
# Return the forest score
#
def classify(data):    
    # encoding the genre lables to int    
    y = data.genre
    y = le_y.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 42) 
    kf = KFold( n_splits = 8, random_state = 42, shuffle = True)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

    forest = RandomForestClassifier(n_estimators = 500, max_depth = 50, random_state = 42)
    forest = forest.fit(X_train, y_train)  
    forest_score = forest.score(X_test, y_test) 
    
    return forest, forest_score


#Locates any song in spotify
#
#
def searchSong(artist, track):
    bag,score = classify(audio_data)
    columns = ['mode', 'tempo', 'dance', 'energy', 'loud', 'speech', 'acoustic', 'instrumental', 'live', 'valence']
    ft_list = []
    # Search for song, get the first result's id
    results = sp.search(artist + ' ' + track)
    track_id = results['tracks']['items'][0]['id']
    artist = results['tracks']['items'][0]['artists'][0]['name']
    track = results['tracks']['items'][0]['name']
    preview_url = results['tracks']['items'][0]['preview_url']
    images_array = results['tracks']['items'][0]['album']['images']
    album_art = images_array[1]['url']
    
    # Use id to find audio features of song
    f = sp.audio_features(tracks = [track_id])
    for i in f:  
        track_ft = []
        track_ft.append(i['mode'])
        track_ft.append(i['tempo'])
        track_ft.append(i['danceability'])
        track_ft.append(i['energy'])
        track_ft.append(i['loudness'])
        track_ft.append(i['valence'])
        track_ft.append(i['acousticness'])
        track_ft.append(i['liveness'])
        track_ft.append(i['instrumentalness'])
        track_ft.append(i['speechiness']) 
        ft_list.append(track_ft)
    track_data = pd.DataFrame(ft_list, index = [track], columns = columns)
    track_data = scaler.transform(track_data)
    tree_proba = bag.predict_proba(track_data)[0]
    tree_proba = tree_proba.tolist()
    tree_proba = [i * 100 for i in tree_proba]
    tree_proba = [round(i,2) for i in tree_proba]
    
    genre = str(le_y.inverse_transform(bag.predict(track_data))[0])    
    return artist, track, genre, preview_url, album_art, tree_proba, score
