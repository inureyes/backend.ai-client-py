import requests
import argparse
import base64
import json
import os
from tabulate import tabulate

parser = argparse.ArgumentParser(description='Predict using specific model')
parser.add_argument('model', metavar='MODEL', type=str,
                   help='Model name to use.')
parser.add_argument('payload', metavar='PAYLOAD', type=str,
                   help='JSON-type payload to request prediction to model.')
parser.add_argument('--info',  action='store_true', default=False,
                 help='Abstract model information of given session ID')
parser.add_argument('--detail',  action='store_true', default=False,
                 help='Detailed model information of given session ID')

args = parser.parse_args()


def main():
  MODEL_NAME = os.environ.get('MODEL_NAME')
  if args.info:
    response = requests.get('http://localhost:8501/v1/models/model_'+MODEL_NAME)
    print(response.json())
    if args.detail:
      response = requests.get('http://localhost:8501/v1/models/model_'+MODEL_NAME+'/metadata')
      print(response.json())

  else:
    SERVER_URL = 'http://localhost:8501/v1/models/model_'+MODEL_NAME+':predict'
    predict_request = '{"instances": [%s]}' % args.payload
    
    #predict_request = '{"instances" : [{"b64": "%s"}]}' % base64.b64encode(
    #    dl_request.content)
    
    #IMAGE_URL = 'https://tensorflow.org/images/blogs/serving/cat.jpg'
    #dl_request = requests.get(IMAGE_URL, stream=True)
    #dl_request.raise_for_status()
    #SERVER_URL = 'http://localhost:8501/v1/models/model_'+MODEL_NAME+':predict'
    #predict_request = '{"instances" : [{"b64": "%s"}]}' % base64.b64encode(dl_request.content).decode()
    #predict_request = args.payload
    response = requests.post(SERVER_URL, data=predict_request)
    #response.raise_for_status()
    #print(response.content)
    prediction = response.json()
    print(prediction)
  
if __name__ == '__main__':
  main()
