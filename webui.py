from flask import Flask, render_template, request, jsonify
import logging
import datetime
import os
import yaml
from utilities import *
import psutil

class EmmetWebUI:
    def __init__(self, emmet_instance, m_logger):
        print(blue("[WEBUI]") + " Initializing web UI...", end="")
        self.logger = m_logger
        self.logger.info("WEBUI: Initializing web UI...")   
        self.emmet = emmet_instance
        self.app = Flask(__name__)
        self.command_history = []  # Storico comandi
        print(bright_green("Done!"))
        self.SetupRoutes()
        
    def SetupRoutes(self):
        # Define web routes here
        print(blue("[WEBUI]") + " Configuring web routes...", end="")
        self.logger.info("WEBUI: Configuring web routes...")
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
    def Run(self):
        print(blue("[WEBUI]") + " Starting web interface on http://localhost:5000")
        self.logger.info("WEBUI: Web interface starting...")
        # debug=False in produzione, use_reloader=False per evitare conflitti con thread
        # threaded=True permette di gestire richieste multiple simultaneamente (utile su Pi)
        self.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)