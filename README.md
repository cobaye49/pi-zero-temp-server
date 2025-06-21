# Pi Zero Temperature Server

Un serveur Flask minimaliste qui lit les données d'un capteur DHT22 et les expose dans une page web responsive avec graphique Chart.js.

## Fonctionnalités

- Lecture température & humidité via DHT22
- Affichage web moderne, lisible sur smartphone
- Historique CSV automatique
- Graphique dynamique (Chart.js)
- Authentification HTTP basique
- Démarrage automatique avec systemd

## Installation

```bash
python3 -m venv env_temp
source env_temp/bin/activate
pip install -r requirements.txt
```

## Lancement

```bash
python server_temp.py
```

## Autostart avec systemd

Copier `systemd/temp-web.service` vers `/etc/systemd/system/` puis :

```bash
sudo systemctl daemon-reload
sudo systemctl enable temp-web.service
sudo systemctl start temp-web.service
```

## Capture

⚠️ Ajouter une capture écran ici si souhaité
