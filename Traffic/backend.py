from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
from flask.json import jsonify
import uuid
from paquetes import Calle


games = {}

app = Flask(__name__, static_url_path='')

port=int(os.environ.get('PORT', 8000))

@app.route("/")
def root():
    return "ok"

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = Calle()
    return "ok", 201, {'Location': f"/games/{id}"}


@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    auto1 = model.schedule.agents[80]
    auto2 = model.schedule.agents[81]
    auto3 = model.schedule.agents[82]
    auto4 = model.schedule.agents[83]
    auto5 = model.schedule.agents[84]
    return jsonify({ "Items": [{"x": auto1.pos[0]*10, "y": auto1.pos[1]*10},{"x": auto2.pos[0]*10, "y": auto2.pos[1]*10},{"x": auto3.pos[0]*10, "y": auto3.pos[1]*10},{"x": auto4.pos[0]*10, "y": auto4.pos[1]*10},{"x": auto5.pos[0]*10, "y": auto5.pos[1]*10}]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
