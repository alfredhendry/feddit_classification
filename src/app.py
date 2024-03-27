import requests
import json
import pandas as pd
from waitress import serve
from textblob import TextBlob
from flask import Flask, request
from flask_restx import Resource, Api
from textblob.sentiments import PatternAnalyzer

app = Flask(__name__)
api = Api(app)
        
@api.route('/get_classified_comments/', methods=["GET"])
class CommentClassifier(Resource):

    def get(self):
    
        # Default values for the parameters
        limit = config_data['limit']
        subfeddit_id = 1
        sort = False
        
        # Check if limit is number
        if 'limit' in request.args:
            try:
                limit= int(request.args.get('limit'))
            except ValueError:
                # Handle the exception
                print('Please enter int for limit')
        
        # Check if subfeddit is number
        if 'subfeddit_id' in request.args:
            try:
                subfeddit_id= int(request.args.get('subfeddit_id'))
            except ValueError:
                print('Please enter int for subfeddit_id')
        
        # Check if sorting needed     
        if 'sort' in request.args:
            sort = True
        
        # Create URL with the desired inputs
        comment_url = config_data['comment_url'].format(str(subfeddit_id), str(limit))
        
        # A GET request to the API
        response = requests.get(comment_url)
        
        comment_list = json.loads(response.text)['comments']
        
        comment_df = pd.DataFrame.from_dict(comment_list)
        #comment_df['dt']=pd.to_datetime(comment_df['created_at'])
        
        # Find the polarity of comments and classify
        comment_df['polarity'] = comment_df['text']. \
            apply(lambda x: TextBlob(x,analyzer=PatternAnalyzer()).sentiment.polarity)
        comment_df['classification'] = comment_df['polarity'].apply(lambda x: 'Negative' if x < 0 else 'Positive')
        
        # Sorting the comments by score
        if sort:
            comment_df.sort_values(by='polarity', ascending=True, inplace=True)
            
        return comment_df[['id', 'text', 'polarity', 'classification']].to_json(orient='records', lines=False)
        

if __name__ == '__main__':
    # Use the host and port specified in config file
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    print('Application running on {} and port {}'.format(config_data['host'],config_data['port'])) 
    serve(app, host=config_data['host'], port=config_data['port'])
    
    