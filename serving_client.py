import requests
import argparse

parser = argparse.ArgumentParser(description='Predict using specific model')
parser.add_argument('model', metavar='MODEL', type=str,
                   help='Model name to use.')
parser.add_argument('payload', metavar='PAYLOAD', type=str,
                   help='JSON-type payload to request prediction to model.')

args = parser.parse_args()

SERVER_URL = 'http://localhost:8501/model_'+args.model+':predict'

def main():
  predict_request = args.payload
  response = requests.post(SERVER_URL, data=predict_request)
  response.raise_for_status()
  prediction = response.json()
  print(prediction)

if __name__ == '__main__':
  main()
