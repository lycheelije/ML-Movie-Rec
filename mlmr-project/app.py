from flask import Flask, render_template, url_for, Request
import pickle

app = Flask(__name__, static_url_path = "/static", static_folder = "static")

#model = pickle.load(open('model.pkl', 'rb'))

## Routing
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html')

## Add additional functions here

if __name__ == "__main__":
    app.run()

