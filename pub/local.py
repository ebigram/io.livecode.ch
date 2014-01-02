from flask import Flask
from flask import request
from flask import render_template
import os
import json
import requests

app = Flask(__name__)

@app.route("/api/run/<user>/<repo>", methods=['POST'])
def proxy_github_run(user, repo):
    data = {}
    for k,v in request.form.iteritems():
        data[k] = v
    r = requests.post('http://%s/api/run/%s/%s' % (os.environ.get('REMOTE_SERVER_NAME', 'io.livecode.ch'), user, repo), data)
    return r.text, r.status_code

@app.route('/')
def local_index():
    return render_template("local/index.html")

def local_defaults(user, repo):
    with open('templates/local/%s/.io.livecode.ch/defaults.json' % repo) as f_defaults:
        return json.load(f_defaults)

@app.route('/learn/<user>/<repo>')
def local_preview(user, repo):
    j_defaults = local_defaults(user, repo)
    return render_template('local/%s/.io.livecode.ch/_site/index.html' % repo, user=user, repo=repo, language=j_defaults.get('language'))

if __name__ == "__main__":
    app.run(debug=True)