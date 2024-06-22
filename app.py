from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "61638396e17f9149afc1c296f5c5af71"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City name is required"}), 400
    
    try:
        current_weather_url = f"{BASE_URL}weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        current_response = requests.get(current_weather_url, params=params)
        current_data = current_response.json()
        
        daily_forecast_url = f"{BASE_URL}forecast"
        daily_params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        daily_response = requests.get(daily_forecast_url, params=daily_params)
        daily_data = daily_response.json()

        current = {
            "city": current_data['name'],
            "temperature": current_data['main']['temp'],
            "feels_like": current_data['main']['feels_like'],
            "weather": current_data['weather'][0]['main'],
            "description": current_data['weather'][0]['description'],
            "weather_icon": f"http://openweathermap.org/img/wn/{current_data['weather'][0]['icon']}@2x.png",
            "wind_speed": current_data['wind']['speed'],
            "humidity": current_data['main']['humidity'],
            "pressure": current_data['main']['pressure'],
            "visibility": current_data['visibility'] / 1000,
            "dew_point": current_data['main']['temp'] - ((100 - current_data['main']['humidity']) / 5)
        }

        hourly = []
        for forecast in daily_data['list'][:6]:
            hourly.append({
                "time": forecast['dt_txt'],
                "temperature": forecast['main']['temp'],
                "weather": forecast['weather'][0]['main'],
                "weather_icon": f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"
            })
        
        daily = []
        for forecast in daily_data['list'][::8][:5]:
            daily.append({
                "date": forecast['dt_txt'].split()[0],
                "min_temp": forecast['main']['temp_min'],
                "max_temp": forecast['main']['temp_max'],
                "weather": forecast['weather'][0]['main'],
                "weather_icon": f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"
            })
    
        return jsonify({
            "current": current,
            "hourly": hourly,
            "daily": daily
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
