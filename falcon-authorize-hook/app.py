import json

import falcon
import json


class Authorize(object):

    def __call__(self, req, resp, resource, params):
        if req.method == "GET":
            req.user_id = 2
        else:
            raise falcon.HTTPBadRequest("Bad Request", "You don't have Admin rights :(")


class ObjResource:
    @falcon.before(Authorize())
    def on_get(self, req, resp):
        print("Triggered Get")
        output = {
            "user_id": req.user_id
        }
        resp.media = output

    @falcon.before(Authorize())
    def on_post(self, req, resp):
        print("Triggered Post")
        output = {
            "user_id": req.user_id
        }
        resp.body = json.dumps(output)

api = falcon.API()
api.add_route("/user", ObjResource())