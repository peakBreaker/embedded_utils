"""Just a simple script to run on a server to post logs to which you can view
from anywhere.  Very handy if you leave a device running and logging over a
weekend and you want to check on it every now and then"""

from flask import Flask, request, send_from_directory
import os
from datetime import date
import json
app = Flask(__name__)

key = 'SECRET_KEY'


@app.route('/postJson', methods=['POST'])
def parse_logs():
    "parses the logs and saves them to a file"
    print("Got post request!")
    data = request.data
    print("#### DATA ####")
    data = str(data)[2:-1]
    print(data)
    if key in data:
        data = data.replace("'key': SECRET_KEY, ", "")
        filename = ('./logs/logs%s.json' % date.today().isoformat())
        with open(filename, 'a') as f:
            f.write(data + "\n")
        return "Thank you for the data!"
    else:
        return "Invalid data"


@app.route('/logs/<path:path>')
def send_js(path):
    return send_from_directory('./logs/', path)


@app.route("/")
def view_logs():
    "Returns the logs to the user"
    logs = os.listdir('./logs/')
    print(logs)
    logsHTML = '<h1> :: LOGS :: </h1>'
    for log in logs:
        logsHTML += ('<a href=/logs/%s>%s</a> <br>' % (log, log))
    return logsHTML


if __name__ == "__main__":
    context = ('./certs/domain.crt', './certs/domain.key')
    app.run(host='0.0.0.0', port=80, ssl_context=context, threaded=True, debug=True)
