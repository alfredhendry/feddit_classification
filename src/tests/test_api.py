import requests
import json

# check if successful response
def test_api_working():
    with open('../config.json') as config_file:
        config_data = json.load(config_file)
    url = "http://{}:{}/get_classified_comments/".format(config_data['host'],config_data['port'])
    
    response = requests.get(url)
    assert response.status_code == 200

# check if response is json
def test_api_content_type():
    with open('../config.json') as config_file:
        config_data = json.load(config_file)
    url = "http://{}:{}/get_classified_comments/".format(config_data['host'],config_data['port'])
    
    response = requests.get(url)
    assert response.headers.get('content-type') == 'application/json'

# check if response has content  
def test_api_content_length():
    with open('../config.json') as config_file:
        config_data = json.load(config_file)
    url = "http://{}:{}/get_classified_comments/".format(config_data['host'],config_data['port'])
    
    response = requests.get(url)   
    
    assert int(response.headers.get('Content-Length')) > 0

# check if response has text     
def test_api_text():
    with open('../config.json') as config_file:
        config_data = json.load(config_file)
    url = "http://{}:{}/get_classified_comments/".format(config_data['host'],config_data['port'])
    
    response = requests.get(url)   
    
    assert response.text != None