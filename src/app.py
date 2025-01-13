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
mongo_uri = os.getenv('MONGO_URI', f"mongodb://{mongo_user}:{mongo_password}@mongo-service:27017/weather-db-staging?authSource=admin")

# Create MongoDB client
client = MongoClient(mongo_uri)
db = client.get_database()  
collection = db['collection']  

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Weather app demo!"})

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        # Make a request to API with the city name
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": api_key,
            "units": "metric"
        })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch weather data"}), response.status_code

        data = response.json()
        return jsonify({
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_api_data', methods=['GET'])
def save_api_data():
    api_url = "https://jsonplaceholder.typicode.com/posts"
    try:
        # Make a request to retrieve data
        response = requests.get(api_url)
        data = response.json()

        # Insert data into MongoDB
        result = collection.insert_many(data)
        return jsonify({"message": f"Data saved to MongoDB! {len(result.inserted_ids)} documents inserted."})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error saving data to MongoDB: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
