from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from transformers import pipeline

from profanity_check import predict, predict_prob
import json,string
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

app = Flask(__name__) 
api = Api(app)

# TODO: Some Ideas for improvemts
# Allow for different models, based on different params
# Return all model results based on params


# Would be cool to dockerize
# Host endpoint on free hosting service or Azure?

# TODO: Bigram and Trigram tokenization in task2

class endpoint(Resource):
	def __init__(self):
		self.classification = pipeline('sentiment-analysis',model="distilbert-base-uncased-finetuned-sst-2-english")
        
	def preprocess_text(self,text, remove_stop_words = False, normalize_words = False, remove_noise = False):
		corpus = word_tokenize(text)
		tokens = pos_tag(corpus)

		stop_words = stopwords.words('english')
		lemmatizer = WordNetLemmatizer()
	
		result_tokens = []

		for token,tag in tokens:
      
			#First check that we should be removing stop words and if so, check if this is a stop word
			if remove_stop_words and token in stop_words:
				continue
		
			if normalize_words:
				if tag.startswith("NN"):
					pos = 'n'
				elif tag.startswith('VB'):
					pos = 'v'
				else:
					pos = 'a'
				token = lemmatizer.lemmatize(token, pos)
	
			if remove_noise and token in string.punctuation: # Noise in the text may need to be removed depending on the problem domain, here punctuation is the noise that is being removed
				continue
		
			result_tokens.append(token)

		joined_text = ' '.join(result_tokens)
		return joined_text

	def post(self):
		
		data = request.data
		data = json.loads(data)
		input_text = data["text"]
		if data["safe_request"]:
			
			prob_contains_profanity = predict_prob([input_text])
			if prob_contains_profanity > 0.9:
				response = jsonify({'valid_input':'No','reason':'Input contains profanity','sentiment': 'NA'})
				response.status_code = 200
				return response

		else:
			preprocessed_text = self.preprocess_text(input_text,data["remove_stop_words"])
			sentiment = self.classification(preprocessed_text)
			response = jsonify({'valid_input':'Yes','reason':'NA','sentiment': sentiment[0]})
		print(sentiment[0])
		response.status_code = 200
		return response

api.add_resource(endpoint,'/')

if __name__ == '__main__': 
  
    app.run(debug = True,host='0.0.0.0',port=5000) 