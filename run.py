from flask import Flask, request
from flask_restful import Resource, Api
import hashlib
import time
import random

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
        if links[key]:
            activated = time.time()
            addr = request.remote_addr
            if not addr in links[key]['active']:
                links[key]['active'][addr] = []

            list = links[key]['active'][addr]
            list.append(activated)

            return [links[key]['active'][request.remote_addr], len(links[key]['active'][request.remote_addr])]
        return {'',''}

api.add_resource(Index, '/')
api.add_resource(GetByKey, '/get/<string:key>')

if __name__ == '__main__':
    app.run(debug=True)