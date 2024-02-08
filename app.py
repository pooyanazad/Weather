from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = '5555555555555555555555555555555'  # Replace with your actual API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    forecast_data = []
    if request.method == 'POST':
        city_name = request.form['city']
        complete_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units=metric"
        try:
            response = requests.get(complete_url, timeout=10)  # Added timeout
            if response.status_code == 200:
                weather_data = response.json()
                for entry in weather_data['list'][:7]:  # Assume first 7 entries as "historical"
                    forecast_data.append({
                        'date': entry['dt_txt'],
                        'temp': entry['main']['temp'],
                        'weather': entry['weather'][0]['description']
                    })
            else:
                error = "City not found"
        except requests.exceptions.RequestException as e:
            error = str(e)
    return render_template('index.html', weather_data=weather_data, forecast_data=forecast_data, error=error)

@app.route('/refresh', methods=['GET'])
def refresh():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
