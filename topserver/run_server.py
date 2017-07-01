"""
Backend server which returns monitoring data at the following endpoints:

/api/machines
    Returns a list of machine ids
/api/top/{machine_id}
    Returns formatted moving average data
/api/nvidia/{machine_id}
    Returns formatted moving average data
"""
from flask import Flask
import json

from .config import *
from .machine_data import MachineData

app = Flask(__name__)

MACHINE_DATA = MachineData(HOSTS, SSH_USER, [IDENTITY_FILE]*len(HOSTS))


@app.route('/api/machines')
def api_machines():
    data = MACHINE_DATA.hosts
    return json.dumps(data)


@app.route('/api/top/<string:machine_id>')
def api_top(machine_id):
    data = MACHINE_DATA.query_top(machine_id)
    return json.dumps(data)


@app.route('/api/nvidia/<string:machine_id>')
def api_nvidia(machine_id):
    data = MACHINE_DATA.query_nvidia(machine_id)
    return json.dumps(data)


@app.route('/monitor')
def monitor():
    return 'Hello'


