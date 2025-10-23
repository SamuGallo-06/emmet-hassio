from flask import Flask, render_template, request, jsonify
import logging
import datetime
import os
import yaml
from utilities import *
import psutil

class EmmetWebUI:
    def __init__(self, emmet_instance, m_logger, ingress_path=''):
        print(blue("[WEBUI]") + " Initializing web UI...", end="")
        self.logger = m_logger
        self.logger.info("WEBUI: Initializing web UI...")   
        self.emmet = emmet_instance
        self.ingress_path = ingress_path  # Per supportare Home Assistant ingress
        self.app = Flask(__name__)
        self.command_history = []  # Storico comandi
        print(bright_green("Done!"))
        self.SetupRoutes()
        
    def SetupRoutes(self):
        # Define web routes here
        print(blue("[WEBUI]") + " Configuring web routes...", end="")
        self.logger.info("WEBUI: Configuring web routes...")
        
        @self.app.route(f'{self.ingress_path}/')
        def index():
            return render_template('index.html', ingress_path=self.ingress_path)
        
        # API per ottenere la configurazione corrente
        @self.app.route(f'{self.ingress_path}/api/config', methods=['GET'])
        def get_config():
            try:
                with open('configuration.yaml', 'r') as file:
                    config = yaml.safe_load(file)
                # Nascondi dati sensibili
                if 'picovoice' in config and 'access-key' in config['picovoice']:
                    config['picovoice']['access-key'] = '***HIDDEN***'
                if 'homeassistant' in config and 'access-token' in config['homeassistant']:
                    config['homeassistant']['access-token'] = '***HIDDEN***'
                return jsonify({'success': True, 'config': config})
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # API per aggiornare la configurazione
        @self.app.route(f'{self.ingress_path}/api/config', methods=['POST'])
        def update_config():
            try:
                data = request.json
                section = data.get('section')
                key = data.get('key')
                value = data.get('value')
                
                if not all([section, key, value]):
                    return jsonify({'success': False, 'error': 'Missing parameters'}), 400
                
                SetConfigValue(section, key, value)
                self.logger.info(f"Config updated: {section}.{key}")
                return jsonify({'success': True, 'message': 'Configuration updated'})
            except Exception as e:
                self.logger.error(f"Error updating config: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # API per ottenere i log recenti
        @self.app.route(f'{self.ingress_path}/api/logs', methods=['GET'])
        def get_logs():
            try:
                log_dir = 'logs'
                if not os.path.exists(log_dir):
                    return jsonify({'success': True, 'logs': []})
                    
                log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
                
                if not log_files:
                    return jsonify({'success': True, 'logs': []})
                
                # Prendi il file di log più recente
                latest_log = max([os.path.join(log_dir, f) for f in log_files], key=os.path.getctime)
                
                # Leggi le ultime N righe
                lines_to_read = int(request.args.get('lines', 50))
                with open(latest_log, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-lines_to_read:]
                
                return jsonify({'success': True, 'logs': recent_lines})
            except Exception as e:
                self.logger.error(f"Error reading logs: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # API per ottenere lo stato del sistema
        @self.app.route(f'{self.ingress_path}/api/status', methods=['GET'])
        def get_status():
            try:
                status = {
                    'running': True,
                    'command_history': self.command_history[-10:],  # Ultimi 10 comandi
                    'uptime': 'N/A'  # Puoi implementare un contatore
                }
                return jsonify({'success': True, 'status': status})
            except Exception as e:
                self.logger.error(f"Error getting status: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # API per inviare un comando testuale (simulazione)
        @self.app.route(f'{self.ingress_path}/api/command', methods=['POST'])
        def send_command():
            try:
                data = request.json
                command = data.get('command', '')
                
                if not command:
                    return jsonify({'success': False, 'error': 'No command provided'}), 400
                
                # Aggiungi al registro
                self.command_history.append({
                    'command': command,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                self.logger.info(f"Web command received: {command}")
                
                # Qui potresti simulare l'esecuzione del comando
                # self.emmet.commandText = command
                # result = self.emmet.PerformAction()
                
                return jsonify({'success': True, 'message': 'Command received', 'command': command})
            except Exception as e:
                self.logger.error(f"Error processing command: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # API per monitorare risorse di sistema (utile per Pi)
        @self.app.route(f'{self.ingress_path}/api/system', methods=['GET'])
        def get_system_info():
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Temperatura CPU su Raspberry Pi
                temp = "N/A"
                try:
                    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                        temp = f"{float(f.read()) / 1000:.1f}°C"
                except:
                    pass
                
                system_info = {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used': f"{memory.used / (1024**3):.2f} GB",
                    'memory_total': f"{memory.total / (1024**3):.2f} GB",
                    'disk_percent': disk.percent,
                    'disk_free': f"{disk.free / (1024**3):.2f} GB",
                    'cpu_temp': temp
                }
                
                return jsonify({'success': True, 'system': system_info})
            except Exception as e:
                self.logger.error(f"Error getting system info: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        print(bright_green("Done!"))
        
    def Run(self, port=5000):
        print(blue("[WEBUI]") + f" Starting web interface on http://0.0.0.0:{port}")
        self.logger.info("WEBUI: Web interface starting...")
        # debug=False in produzione, use_reloader=False per evitare conflitti con thread
        # threaded=True permette di gestire richieste multiple simultaneamente (utile su Pi)
        self.app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)