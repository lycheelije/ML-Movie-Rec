import os
import openai
import aicontent
import urllib.request
import json
import pickle
from flask import Flask, render_template, redirect, request, session, url_for

app = Flask(__name__, static_url_path = "/static", static_folder = "static")

## API Keys 
tmdb_ak = "a0bba4b02d48ae656ebb937c0d8d7443"
openai.api_key =  os.getenv("OPENAI_API_KEY")
app.config.from_object("config.Config")

########################################################################## 
## Routing ###############################################################
##########################################################################

# Home/Index #############################################################
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')
##########################################################################



# Search Bar #############################################################
@app.route("/search", methods=['GET', 'POST'])
def search():
    # Preview Discover Titles
    url = "https://api.themoviedb.org/3/discover/movie?api_key=" + tmdb_ak + "&language=en-US&sort_by=popularity.desc&include_video=false&page=1&with_original_language=en"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    return render_template ("search.html", movies=dict["results"])
##########################################################################



# Personal Recommendations #############################################
@app.route("/personalRecommendations", methods=['GET', 'POST'])
def personalRecommendations():
    return render_template('personalRec.html')
##########################################################################




# Group Recommendations ##################################################
@app.route("/groupRecommendations", methods=['GET', 'POST'])
def groupRecommendations():
    if request.method == 'POST':
        submission = request.form['query']
        query = "movie recommendations for me if im feeling: {}".format(submission)
        openAIAnswerUnformatted = aicontent.openAIQuery(query)
        openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
        prompt = 'AI Suggestions for {} are:'.format(submission)
    return render_template("groupRecommendations.html", **locals())
##########################################################################



# Movie Details ##########################################################
@app.route("/movie", methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':

        selectedMovieId = request.form.get('movieId')

        url = "https://api.themoviedb.org/3/movie/" + selectedMovieId + "?api_key=" + tmdb_ak + "&language=en-US"
        response = urllib.request.urlopen(url)
        data = response.read()
        movieData = json.loads(data)

        url = "https://api.themoviedb.org/3/movie/" + selectedMovieId + "/credits?api_key=" + tmdb_ak + "&language=en-US"
        response = urllib.request.urlopen(url)
        data = response.read()
        movieCastData = json.loads(data)
        
        url = "https://api.themoviedb.org/3/movie/" + selectedMovieId + "/recommendations?api_key=" + tmdb_ak + "&language=en-US&page=1&with_original_language=en"
        response = urllib.request.urlopen(url)
        data = response.read()
        similarMovies = json.loads(data)

        url = "https://api.themoviedb.org/3/movie/" + selectedMovieId + "/watch/providers?api_key=" + tmdb_ak
        response = urllib.request.urlopen(url)
        data = response.read()
        streamingProviders = json.loads(data)

        return render_template ("movie.html", movies=movieData, cast=movieCastData, similar=similarMovies["results"], streamingProviders=streamingProviders["results"])
##########################################################################



# T&C's ##################################################################
@app.route("/tnc", methods=['GET', 'POST'])
def tnc():
    return render_template('termsandconditions.html')
##########################################################################



# Run ####################################################################
if __name__ == "__main__":
    app.run()
##########################################################################