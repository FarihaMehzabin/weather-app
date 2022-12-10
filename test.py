from email import message
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.errorhandler(500)
def internal_error(error):
    return jsonify(
        message = "Error occurred"
        ), 500

@app.route('/', methods=['GET'])
def index():
    source = request.args.get('city') #getting parameters from url. Whatever comes after ? is a parameter
    # fetching coordinates
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={source}&limit=5&appid=106c8085ba2b900cce93846e18cedece") 
    coordinates = response.json()
    # getting weather using coordinates
    weatherInfo = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]['lat']}&lon={coordinates[0]['lon']}&units=metric&appid=106c8085ba2b900cce93846e18cedece")
    weatherInfoJSON = weatherInfo.json()
    
    # return weatherInfo.json();
    #returning json to fetch
    try:
        return jsonify(
        status_code=200,
        name=coordinates[0]['name'],
        weather=weatherInfo.json()["weather"][0]["description"],
        temp=weatherInfoJSON['main']['temp'],
        feels_like = weatherInfoJSON['main']['feels_like'],
        humidity= weatherInfoJSON['main']['humidity'],
        )
    except IndexError:
        print("Couldn't get weather")
        

app.run(host='0.0.0.0', port=8080)

