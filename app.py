#enter in command line:
# >>> pip3 install flask
# >>> export FLASK_APP=app
# >>> export FLASK_ENV=development
# >>> flask run

from flask import Flask, request, redirect, render_template
from GenreClassifier import searchSong

#Flask
#
#
app = Flask(__name__)
app.run(debug=False)

@app.route('/GenreClassifier')
def GenreClassifier():
    data = {'artist': "Ed Sheeran", 'track': "Shape Of You", 'genre': "Pop", 
    'preview_url': "https://p.scdn.co/mp3-preview/84462d8e1e4d0f9e5ccd06f0da390f65843774a2?cid=c4347d8d90204958ba2c4fb3e8af77e0",
    'album_art': "https://i.scdn.co/image/ab67616d00001e02ba5db46f4b838ef6027e6f96", 'probability': ['2.40',  '4.20', '30.4', '20.6', '31.2', '7.00', '4.20'], 'accuracy': '60.0'}
    return render_template('GenreClassifier.html', data=data)

@app.route('/GenreClassifier/search', methods = ['POST'])    
def search(): 
    a = request.form['artist'].title()
    t = request.form['track'].title()
    find = searchSong(a,t)
    artist = find[0]
    track = find[1]
    genre = find[2].title()
    preview_url = find[3]
    album_art = find[4] 
    probability = find[5]
    accuracy = find[6]*100
    data = {'artist': artist, 'track': track, 'genre': genre, 'preview_url': preview_url, 'album_art': album_art, 'probability': probability, 'accuracy':accuracy} 
    return render_template('GenreClassifier.html', data=data)
    # return redirect('/')
