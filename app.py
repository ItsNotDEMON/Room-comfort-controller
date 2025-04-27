from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
from datetime import datetime, timezone

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)
CORS(app)


temperature = ctrl.Antecedent(np.arange(15, 46, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(10, 91, 1), 'humidity')
lighting = ctrl.Antecedent(np.arange(0, 101, 1), 'lighting')
comfort = ctrl.Consequent(np.arange(0, 11, 1), 'comfort')

temperature['cold'] = fuzz.trimf(temperature.universe, [15, 15, 25])
temperature['moderate'] = fuzz.trimf(temperature.universe, [20, 30, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 45, 45])

humidity['dry'] = fuzz.trimf(humidity.universe, [10, 10, 40])
humidity['normal'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['humid'] = fuzz.trimf(humidity.universe, [60, 90, 90])

lighting['dim'] = fuzz.trimf(lighting.universe, [0, 0, 40])
lighting['normal'] = fuzz.trimf(lighting.universe, [30, 50, 70])
lighting['bright'] = fuzz.trimf(lighting.universe, [60, 100, 100])

comfort['low'] = fuzz.trimf(comfort.universe, [0, 0, 4])
comfort['medium'] = fuzz.trimf(comfort.universe, [3, 5, 7])
comfort['high'] = fuzz.trimf(comfort.universe, [6, 10, 10])

rule1 = ctrl.Rule(temperature['moderate'] & humidity['normal'] & lighting['normal'], comfort['high'])
rule2 = ctrl.Rule(temperature['hot'] & humidity['humid'], comfort['low'])
rule3 = ctrl.Rule(temperature['cold'] & humidity['dry'], comfort['low'])
rule4 = ctrl.Rule(temperature['moderate'] & (humidity['normal'] | lighting['dim']), comfort['medium'])
rule5 = ctrl.Rule(temperature['hot'] & lighting['bright'], comfort['medium'])
rule6 = ctrl.Rule(lighting['bright'] & humidity['humid'], comfort['low'])

comfort_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
comfort_sim = ctrl.ControlSystemSimulation(comfort_ctrl)


@app.route('/weather', methods=['POST'])
def get_weather_data():
    data = request.get_json()
    location = data.get('location')

    if not location:
        return jsonify({'error': 'Location is required'}), 400

    api_key = 'ed59edf3c110165ca8faf43f8d528745'  
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        weather_data = response.json()

        if weather_data.get('cod') != 200:
            return jsonify({'error': weather_data.get('message')}), 400

        temperature_val = weather_data['main']['temp']
        humidity_val = weather_data['main']['humidity']
        lighting_val = random.randint(0, 100)  # Simulated


        temperature_val = max(15, min(temperature_val, 45))
        humidity_val = max(10, min(humidity_val, 90))
        lighting_val = max(0, min(lighting_val, 100))


        comfort_sim.input['temperature'] = temperature_val
        comfort_sim.input['humidity'] = humidity_val
        comfort_sim.input['lighting'] = lighting_val

        comfort_sim.compute()
        comfort_level = comfort_sim.output['comfort']
        suggestion = generate_suggestion(comfort_level)

        timestamp = datetime.fromtimestamp(weather_data['dt'], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        return jsonify({
        'location': location,
        'temp': temperature_val,
        'humidity': humidity_val,
        'condition': weather_data['weather'][0]['main'],
        'lighting': lighting_val,
        'comfort': round(comfort_level, 2),
        'suggestion': suggestion
        })



    except Exception as e:
        return jsonify({'error': str(e)}), 500



def generate_suggestion(comfort_level):
    if comfort_level >= 7:
        return "High comfort. Maintain current settings."
    elif 4 <= comfort_level < 7:
        return "Medium comfort. Adjusting AC to 23 degrees and lighting to 60 percent."
    else:
        return "Low comfort. Setting AC to 21 degrees and dimming lights to 40 percent."



if __name__ == '__main__':
    app.run(debug=True)
