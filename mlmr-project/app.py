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
openai.api_key = "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"
# openai.api_key =  os.getenv("OPENAI_API_KEY")
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

        movieData = []
        
        # Set data for query
        releaseRangeSearch = request.form['release-range-search-gr']
        genreSearch = request.form['genre-search-gr']
        ratingSearch = request.form['rating-search-gr']

        query = "Q: Find 4 horror movies, released from 2010-2022, with an average rating of 65 percent or more on Rotten Tomatoes. Remove the release date from the end of each suggestion. Remove ratings from results. Remove list numbers from results.\nA: The Conjuring, The Conjuring 2, The Purge, The Purge: Anarchy\n\nQ: Find 4 " + genreSearch +  " movies, released from " + releaseRangeSearch + ", with an average rating of " + ratingSearch + " percent or more on Rotten Tomatoes. Remove the release date from the end of each suggestion. Remove ratings from results. Remove list numbers from results.\nA:"
        
        # locals
        groupSearchResults = aicontent.groupSearchQuery(query)
        groupSearchResultsSplit = groupSearchResults.split(",")


    return render_template("groupRecommendations.html", **locals())
##########################################################################

# Group Recommendations Results ##################################################
@app.route("/groupRecommendations/results", methods=['GET', 'POST'])
def groupRecommendationsResults():
    if request.method == 'POST':

        movieData = []
        
        # Set data for query
        releaseRangeSearch = request.form['release-range-search-gr']
        genreSearch = request.form['genre-search-gr']
        ratingSearch = request.form['rating-search-gr']

        query = "Q: Find 4 horror movies, released from 2010-2022, with an average rating of 65 percent or more on Rotten Tomatoes. Remove the release date from the end of each suggestion. Remove ratings from results. Remove list numbers from results.\nA: The Conjuring, The Conjuring 2, The Purge, The Purge: Anarchy\n\nQ: Find 4 " + genreSearch +  " movies, released from " + releaseRangeSearch + ", with an average rating of " + ratingSearch + " percent or more on Rotten Tomatoes. Remove the release date from the end of each suggestion. Remove ratings from results. Remove list numbers from results.\nA:"
        
        # locals
        groupSearchResults = aicontent.groupSearchQuery(query)
        groupSearchResultsSplit = groupSearchResults.split(",")
        api_url_list = []
        for word in groupSearchResultsSplit:
            result = word.replace(' ', '%20')
            url = "https://api.themoviedb.org/3/search/movie?api_key=" + tmdb_ak + "&language=en-US&query=" + result + "&page=1&include_adult=false"
            api_url_list.append(url)

        # Use list of urls to get data
        for url in api_url_list:
            response = urllib.request.urlopen(url)
            data = response.read()
            movieData = json.loads(data)


    return render_template("groupRecommendations.html", movieData=movieData["results"])
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