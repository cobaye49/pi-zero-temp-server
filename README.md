# Pi Zero Temperature Server

A minimal Flask server that reads data from a DHT22 sensor and displays it on a responsive web page with a dynamic Chart.js graph.

## Features

- Reads temperature & humidity from a DHT22 sensor
- Mobile-friendly web interface
- Automatic CSV logging of historical data
- Dynamic graph using Chart.js
- Basic HTTP authentication
- Automatic startup with systemd

## Installation

```bash
python3 -m venv env_temp
source env_temp/bin/activate
pip install -r requirements.txt
```

## Launching the server

```bash
python server_temp.py
```

## Autostart with systemd

Copy `systemd/temp-web.service` to `/etc/systemd/system/` then :

```bash
sudo systemctl daemon-reload
sudo systemctl enable temp-web.service
sudo systemctl start temp-web.service
```

