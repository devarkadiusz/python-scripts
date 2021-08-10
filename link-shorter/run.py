from flask import Flask, request, redirect
from flask_restful import Resource, Api
import hashlib
import time
import random
import json

app = Flask(__name__)
api = Api(app)

links = {}

class Index(Resource):
    def get(self):
        return links

    def put(self):
        created = time.time()
        target = request.form['data']
        hash = str(created) + "_" + str(target)
        key = hashlib.md5(hash.encode('utf-8')).hexdigest()[0:8]
        links[key] = {
            'target': target,
            'created': created,
            'active': {}
        }
        return {'key':key}
    
class GetByKey(Resource):
    def get(self, key):
        if key in links:
            return links[key]

        return redirect('/', code=404)
    
class Redirect(Resource):
    def get(self, key):
        if key in links:
            activated = time.time()
            addr = request.remote_addr
            link = links[key]
            if not addr in link['active']:
                 link['active'][addr] = []

            link['active'][addr].append(activated)

            return redirect(link['target'], code=302)
        return redirect('/', code=404)

api.add_resource(Index, '/')
api.add_resource(GetByKey, '/get/<string:key>')
api.add_resource(Redirect, '/r/<string:key>')

if __name__ == '__main__':
    app.run(debug=True)