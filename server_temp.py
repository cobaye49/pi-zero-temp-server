from flask import Flask, Response, request
import Adafruit_DHT
import csv
from datetime import datetime

app = Flask(__name__)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
USERNAME = "admin"
PASSWORD = "monmotdepasse"

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response("Authentification requise", 401,
                    {"WWW-Authenticate": 'Basic realm="Accès Pi Zero"'})

def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

def log_data(temp, hum):
    with open("/home/cobaye/dht22_history.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), temp, hum])

def read_history(n=20):
    try:
        with open("/home/cobaye/dht22_history.csv", "r") as f:
            lines = f.readlines()[-n:]
            timestamps, temps = [], []
            for line in lines:
                date_str, temp, _ = line.strip().split(",")
                dt = datetime.fromisoformat(date_str)
                timestamps.append(dt.strftime("%H:%M"))
                temps.append(float(temp))
            return timestamps, temps
    except Exception as e:
        return [], []

@app.route('/')
@requires_auth
def index():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        log_data(temperature, humidity)
        timestamps, temps = read_history()
        labels_js = ",".join([f'"{t}"' for t in timestamps])
        temps_js = ",".join([str(t) for t in temps])
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        return f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; text-align: center; padding: 40px; }}
                .card {{ display: inline-block; background: white; padding: 20px 40px; border-radius: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.1); margin-bottom: 40px; }}
                .title {{ font-size: 32px; margin-bottom: 20px; }}
                .value {{ font-size: 48px; font-weight: bold; margin: 10px 0; }}
                .subtitle {{ font-size: 20px; color: #888; }}
                canvas {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <div class='card'>
                <div class='title'>🌡️ Température Pi Zero</div>
                <div class='value'>Température : {temperature:.1f} °C</div>
                <div class='value'>Humidité : {humidity:.1f} %</div>
                <div class='subtitle'>Dernier relevé : {now}</div>
            </div>
            <canvas id='historyChart' width='300' height='150'></canvas>
            <script>
              const ctx = document.getElementById('historyChart').getContext('2d');
              const chart = new Chart(ctx, {{
                type: 'line',
                data: {{
                  labels: [{labels_js}],
                  datasets: [{{
                    label: 'Température (°C)',
                    data: [{temps_js}],
                    fill: false,
                    borderColor: '#ff5722',
                    tension: 0.2
                  }}]
                }},
                options: {{
                  responsive: true,
                  scales: {{
                    y: {{ beginAtZero: false }}
                  }}
                }}
              }});
            </script>
        </body>
        </html>
        """
    else:
        return "Erreur de lecture du capteur", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
