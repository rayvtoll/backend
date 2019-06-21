
# This needs to become a distributed storage location
externalVolume = '/opt/vcde/'

# Other variables
netWork = 'vcd_frontend'
#vcdImage = 'winrdplxde4'
vcdImage = 'rayvtoll/containerdesktop'

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
    dockerPs = 'docker ps --filter name=vcd-' + request.json + ' --format "{{ json .}}" | jq --slurp .'
    X = subprocess.check_output(dockerPs, shell=True).decode('utf-8')
    data = json.loads(str(X))
    for i in range(0, len(data)):
        if data[i]['Names'] == request.json:
            activeSessionString = "docker exec vcd-" + request.json + " ps -ef h | grep xrdp"
            activeSession = subprocess.check_output(activeSessionString, shell=True)
            if not "Xorg" in str(activeSession):
                os.system("docker container rm -f vcd-" + request.json)
    dockerRun = str('docker run --rm --name vcd-' + request.json + ' -d --network ' + netWork + ' -e USER=' + request.json + ' -v ' + externalVolume + request.json + '/:/home/' + request.json + '/ ' + vcdImage)
    return jsonify([{'request' : dockerRun }, {'exitcode' : os.system(dockerRun)}])

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
