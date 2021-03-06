import numpy as np
import pandas as pd
import re
from flask import Flask,render_template,url_for,request
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

app = Flask(__name__)

# home page ---
@app.route('/')
def home():
	return render_template('home.html')

# sentiment page ---
@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

# topic page ---
@app.route('/topic')
def topic():
    return render_template('topic.html')


# predict sentiment page ---
@app.route('/sentiment_predict',methods=['POST'])
def sentiment_predict():
	

	if request.method == 'POST':
		message = request.form['message']
		#data = [message]
		sentiment_obj = TextBlob(message)
		my_prediction = sentiment_obj.sentiment.polarity
	return render_template('result_sentiment.html',prediction = my_prediction)

# predict topic page ---
@app.route('/topic_predict', methods=['POST'])
def topic_predict():

    if request.method == 'POST':
        message = request.form['message']
        message_clean = re.sub(r'[^\w\s]','', message)
        message_clean = word_tokenize(message_clean)
        new_sentence =[]
        for w in message_clean:
            if w not in stop_words: new_sentence.append(w)
        counts = Counter(new_sentence)
        counts_high = {x : counts[x] for x in counts if counts[x] >= 3}
        counts_df_high = pd.DataFrame.from_dict(counts_high, orient='index', columns=['Freq'])
        counts_df_high = counts_df_high.reset_index()
        counts_df_high.columns = ['Word', 'N']
        counts_df_high = counts_df_high.sort_values(by=['N'], ascending=False)

    return render_template('result_topic.html', tables=[counts_df_high.to_html(classes='table table-striped table-dark table-hover .table-responsive',  header="true", index = False)])


if __name__ == '__main__':
	app.run(debug=True)


# -- Example
#phrase = 'the weather is beautiful!'
#sentiment_objects = TextBlob(phrase)

#print(sentiment_objects.sentiment.polarity)
#print(phrase)
# --