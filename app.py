from flask import Flask, request, jsonify,render_template
import requests
import learn
import os
from dotenv import load_dotenv



app = Flask(__name__)


load_dotenv()


def extract_sentences(api_response):
    start_index = api_response.find('ad-copy-for-shopping-website:') + len('ad-copy-for-shopping-website:')
    end_index = api_response.find('ad-copy-for-Instagram:')
    website_ad = api_response[start_index:end_index].strip()

    start_index = api_response.find('ad-copy-for-Instagram:') + len('ad-copy-for-Instagram:')
    instagram_ad = api_response[start_index:].strip()

    return [website_ad, instagram_ad]

def makeApiCall(type,des):

    API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
    PROJECT_ID = "formal-theater-393511"
    MODEL_ID = "text-bison@001"

    url = f"https://{API_ENDPOINT}/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/{MODEL_ID}:predict"

    headers = {
        "Authorization": f"Bearer {os.getenv('KEY')}",
        "Content-Type": "application/json",
        "lifetime": "LIFETIME"

    }

    payload = {
        "instances": [
            {
                "content": learn.learn(type,des) 
            }
        ],
        "parameters": {
            "temperature": 0.7,
            "maxOutputTokens": 700,
            "topP": 0.8,
            "topK": 40
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Error message:")
        print(response.text) 
        return '404'

@app.route('/')
def homePage():
    return render_template('index.html')
    
    
@app.route('/info',methods=['POST'])
def display_data():
   content= makeApiCall(request.form.get('ctype'),request.form.get('cdes'))['predictions'][0]['content']
   if(content=='this is not cloth type'):
    return render_template('error.html')
   else:    
    return render_template('secondPage.html',data=extract_sentences(content))

    

if __name__ == '__main__':
    app.run()