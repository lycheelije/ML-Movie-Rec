import os
import openai
import aicontent

import pickle
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__, static_url_path = "/static", static_folder = "static")
openai.api_key =  os.getenv("OPENAI_API_KEY")
app.config.from_object("config.Config")
#model = pickle.load(open('model.pkl', 'rb'))

## Routing
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route("/groupRec", methods=['GET', 'POST'])
def groupRec():
    if request.method == 'POST':
        submission = request.form['query']
        query = "movie recommendations for me if im feeling: {}".format(submission)
        openAIAnswerUnformatted = aicontent.openAIQuery(query)
        openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
        prompt = 'AI Suggestions for {} are:'.format(submission)
    return render_template("groupRec.html", **locals())

# def generate_prompt(query):
    

#     if 'choices' in response:
#         if len(response['choices']) > 0:
#             answer = response['choices'][0]['text']
#         else:
#             answer = 'Opps sorry, you beat the AI this time'
#     else:
#         answer = 'Opps sorry, you beat the AI this time'

#     return answer
## Add additional functions here

if __name__ == "__main__":
    app.run()

