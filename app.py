from flask import Flask, render_template, request
import requests
import joblib
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
import os 
from flask import Flask, render_template

load_dotenv()

class_mapping = {
    0: 'Clear',
    1: 'Rainy',
    2: 'Cloudy'
}

app = Flask(__name__)

# Load the weather prediction model
model = joblib.load('weather_prediction_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Get latitude and longitude from the form
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    city = request.form.get('city')


    # Use OpenWeatherMap API to get weather data
    api_key = os.getenv("fk_api_key")
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
    
    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        weather_data = response.json()
        

        # Extract relevant weather information
        country = weather_data.get('sys', {}).get('country', 'N/A')
        api_city = weather_data.get('name', 'N/A')
        temperature = weather_data.get('main', {}).get('temp', 'N/A') - 273.15  # Convert from Kelvin to Celsius
        humidity = weather_data.get('main', {}).get('humidity', 'N/A')
        wind_speed = weather_data.get('wind', {}).get('speed', 'N/A')
        pressure = weather_data.get('main', {}).get('pressure', 'N/A')
        visibility = weather_data.get('visibility', 'N/A')

        # Print the extracted weather information
        print("Extracted weather information:",
              f"Temperature: {temperature}, Humidity: {humidity}, Wind Speed: {wind_speed},"
              f"Pressure: {pressure}, Visibility: {visibility}")

        # Feature scaling
        scaler = MinMaxScaler()
        features_scaled = scaler.fit_transform([[temperature, humidity, wind_speed, pressure, visibility]])

        # Make predictions using the model
        prediction_index = model.predict(features_scaled)[0]

        # Map the predicted index to the corresponding label
        prediction_label = class_mapping.get(prediction_index, 'Unknown')

        # Print the prediction
        print("Prediction:", prediction_label)


        return render_template('result.html', latitude=latitude, longitude=longitude,
                               country=country, api_city=api_city,
                               temperature=temperature, humidity=humidity,
                               wind_speed=wind_speed, pressure=pressure,
                               visibility=visibility, prediction=prediction_label)

    except requests.exceptions.RequestException as e:
        # Handle errors (e.g., connection issues, API key issues)
        error_message = f"Error fetching data from OpenWeatherMap: {e}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')