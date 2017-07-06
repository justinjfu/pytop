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
from flask import redirect, url_for
import json

from config import *
from machine_data import MachineData

app = Flask(__name__)

MACHINE_DATA = MachineData(HOSTS, SSH_USER, [IDENTITY_FILE]*len(HOSTS), update_interval=UPDATE_INTERVAL)

@app.route('/')
def hello():
    return 'hello'


@app.route('/api/machines')
def api_machines():
    data = MACHINE_DATA.hosts
    return json.dumps(data)

def sanitize_input(s):
    return s.replace(';','')

@app.route('/api/top/<string:machine_id>')
def api_top(machine_id):
    data = MACHINE_DATA.query_top(sanitize_input(machine_id))
    return json.dumps(data)


@app.route('/api/nvidia/<string:machine_id>')
def api_nvidia(machine_id):
    data = MACHINE_DATA.query_nvidia(sanitize_input(machine_id))
    return json.dumps(data)


@app.route('/monitor')
def monitor():
    return redirect(url_for('static', filename='index.html'))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("-o", default=False, action='store_true',
        help='Open a brower tab automatically')
    args = parser.parse_args()

    url = "http://localhost:%d"%(args.port)
    if args.o:
        # automatically open a new tab and show the plots
        import webbrowser
        webbrowser.open(url,new=2)

    app.run(host='0.0.0.0', port=args.port, threaded=True)
