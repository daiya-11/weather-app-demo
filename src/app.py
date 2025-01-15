import requests
from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# API key for OpenWeather
api_key = os.getenv('API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# MongoDB Connection
mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_uri = os.getenv('MONGO_URI', f"mongodb://{mongo_user}:{mongo_password}@mongo-service.default.svc.cluster.local:27017/weather-db-staging?authSource=admin")

# Create MongoDB client
client = MongoClient(mongo_uri)
db = client.get_database()  
collection = db['collection']  

# Route for the home page
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Weather app demo!"})

# Route to fetch weather data for a specified city    
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
         # Make an API call to OpenWeather
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": api_key,
            "units": "metric"
        })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch weather data"}), response.status_code

        data = response.json()

        # Prepare the weather data to store in MongoDB
        weather_data = {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "timestamp": data["dt"]  # Zeitstempel des Wetterberichts
        }

        # Save the weather data to MongoDB
        collection.insert_one(weather_data)

        # Return the weather data as a JSON response
        return jsonify({
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Return the weather data from the database as a JSON response
@app.route("/weather_from_db", methods=["GET"])
def get_weather_data():
    data = collection.find()
    result = []
    for record in data:
        result.append({
            "city": record["city"],
            "temperature": record["temperature"],
            "description": record["description"],
            "timestamp": record["timestamp"]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
