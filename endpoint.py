from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from transformers import pipeline
from profanity_check import predict, predict_prob
import json

app = Flask(__name__) 
api = Api(app)

# TODO: Some Ideas for improvemts
# Allow for different models, based on different params
# Return all model results based on params
# Preprocessing, check for any unsafe words

# Would be cool to dockerize
# Host endpoint on free hosting service or Azure?

class endpoint(Resource):
	def __init__(self):
		self.classification = pipeline('sentiment-analysis',model="distilbert-base-uncased-finetuned-sst-2-english")
        
	def get(self):
		return jsonify({'message': 'I\'m up'}) 

	def post(self):
		
		data = request.data
		data = json.loads(data)
		input_text = data["text"]
		prob_contains_profanity = predict_prob([input_text])
  
		if prob_contains_profanity > 0.9:
			response = jsonify({'valid_input':'No','reason':'Input contains profanity','sentiment': 'NA'})
		else:
			sentiment = self.classification(input_text)
			response = jsonify({'valid_input':'Yes','reason':'NA','sentiment': sentiment})
   
		response.status_code = 200
		return response

api.add_resource(endpoint,'/')

if __name__ == '__main__': 
  
    app.run(debug = True,host='0.0.0.0',port=5000) 