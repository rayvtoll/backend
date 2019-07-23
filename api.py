# This needs to become a distributed storage location
externalVolume = '/opt/vcde/'

# Other variables
netWork = 'vcd_frontend'
vcdImage = 'rayvtoll/containerdesktop:latest'

import os
import subprocess
from flask import Flask, jsonify, request, make_response
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def list_containers():
    dockerPs = 'docker ps --format "{{ json .}}" | jq --slurp .'
    return subprocess.check_output(dockerPs, shell=True)

@app.route('/', methods=['POST'])
def create_container():
    dockerRun = str('docker run --rm  -h vcd-' + request.json + ' --name vcd-' + request.json + ' -d --network ' + netWork + ' -e USER=' + request.json + ' -v ' + externalVolume + request.json + '/:/home/' + request.json + '/ ' + ' -v ' + externalVolume + 'Public:/home/' + request.json + '/Public ' + vcdImage)
    return jsonify([{'request' : dockerRun }, {'exitcode' : os.system(dockerRun)}])

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
