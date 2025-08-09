from flask import Flask, request, jsonify
from scheduler import bot_scheduler
import json
import os

app = Flask(__name__)

CONFIG_FILE = 'config.json'

# Load config from file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

# Save config to file
def save_config(cfg):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=4)

@app.route('/start', methods=['POST'])
def start_bot():
    bot_scheduler.start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    bot_scheduler.stop()
    return jsonify({"status": "stopped"})

@app.route('/run-now', methods=['POST'])
def run_now():
    bot_scheduler.run_now()
    return jsonify({"status": "run triggered"})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        cfg = request.json
        save_config(cfg)
        bot_scheduler.reload_config(cfg)
        return jsonify({"status": "config updated"})
    else:
        return jsonify(load_config())

@app.route('/status')
def status():
    return jsonify(bot_scheduler.get_status())

@app.route('/logs')
def logs():
    return jsonify(bot_scheduler.get_logs())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
