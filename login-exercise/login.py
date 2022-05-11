import falcon
import jwt
import json
from UserRepository import UserRepository


class LoginHandler:

    user_repository = UserRepository()

    def __init__(self):
        pass

    def login(self, req, resp):
        req_params = json.loads(req.stream.read())
        print("In Login::")
        print(req_params)
        if not req_params or not req_params["Username"] or not req_params["Password"]:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter valid Username and Password")
        else:
            self.__authenticate(req_params["Username"], req_params["Password"], req, resp)

    def __authenticate(self, user_name, password, req, resp):
        print("Username: {} and Password: {}".format(user_name, password))
        if not user_name or not password:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter valid Username and Password")
        elif not self.user_repository.is_user_valid(user_name, password):
            raise falcon.HTTPUnauthorized("Unauthorized", "Invalid Credentials")
        else:
            user_id = self.user_repository.get_user_id(user_name)
            if user_id:
                payload = {
                    "user_id": user_id
                }
                secret = "secret"
                algo = "HS256"
                encoded = jwt.encode(payload=payload, key=secret, algorithm=algo)
                resp.media = {'token': encoded}
                resp.status = falcon.HTTP_200
            else:
                resp.media = {"Error": "User Not Found"}
                resp.status = falcon.HTTP_200
            print("User Authenticated...!")

    def on_post(self, req, resp):
        self.login(req, resp)


def main():
    pass


if __name__ == "__main__": main()
