# FlaskSentimentPipeline

## This was run with python version 3.10.9

### Follow the steps below to run both task1 and task2
1. To ensure libraries are of their correct versions, first run the following command in the same folder as the files:
	pip install -r requirements.txt
2. To run the endpoint that will receive post requests, run the following command:
	python endpoint.py
3. After running the previous command, you should see the following output in the terminal:
	![Image of endpoint being run successfully ](/endpointUp.png)

	If you do not see the following image, ensure that the versions of your libraries match that in the requirements.txt
4. Open an API platform such as Postman, which will allow you to test the endpoint.
5. Create a new post request with the following URL: http://127.0.0.1:5000/
6. The endpoint takes the following parameters in the request body:
	- text: The text that the sentiment analysis should be performed on.
	- safe_request(Boolean): If the text should be checked to contain any profanity and refused if it does.
	- remove_stop_words(Boolean): To remove stop words as part of the preprocessing pipeline.
	- normalize_words(Boolean): To normalize all the words, using lemming, as part of the preprocessing pipeline.
	- remove_noise(Boolean): To remove the noise in the text, for now it just removes punctuation, as part of the preprocessing pipeline.
7. If the request is valid the response will be in the following form:
	- valid_input: If the input was valid or not.
	- reason: If the input was not valid, why was it not, if it was it'll say "NA".
	- sentiment: Which contains  both the label and the score or confidence in that label.

