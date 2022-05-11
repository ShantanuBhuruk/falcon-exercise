import base64
import json

import falcon
import json

user_accounts = {
    "shantanu": "password"
}


class Authorize(object):

    def __basic_authentication(self, user_name, password):
        if not user_name or not password:
            raise falcon.HTTPUnauthorized("Unauthorized", "Invalid Credentials")
        elif user_name not in user_accounts or user_accounts[user_name] != password:
            raise falcon.HTTPUnauthorized("Unauthorized", "Invalid Credentials")
        else:
            print("User Authenticated...!")

    def __call__(self, req, resp, resource, params):
        print(f"in authorize {req.auth}")
        auth_exp = req.auth if req.auth is not None else ""
        if auth_exp:
            auth_val = auth_exp.split(" ")
            if auth_val[0].lower() == "basic":
                auth = base64.b64decode(auth_val[1]).decode("utf-8").split(":")
                user_name = auth[0]
                password = auth[1]
                self.__basic_authentication(user_name, password)
                req.user_name = user_name

        else:
            raise falcon.HTTPUnauthorized("Bad Request", "Invalid Credentials")


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
            "user_id": req.user_name
        }
        resp.body = json.dumps(output)


app = falcon.App()
app.add_route("/account", ObjResource())