from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 

app = Flask(__name__) 
api = Api(app)

class sentiment():
    def __init__(self,text):
        self.text = text

class endpoint(Resource):
    
    def get(self):
        return jsonify({'message': 'I\'m up'}) 
    
    def post(self):
        
        text = request.get_json()
        response = jsonify({'sentiment': text})
        response.status_code = 200
        
        return response

api.add_resource(endpoint,'/')

if __name__ == '__main__': 
  
    app.run(debug = True,host='0.0.0.0',port=5000) 