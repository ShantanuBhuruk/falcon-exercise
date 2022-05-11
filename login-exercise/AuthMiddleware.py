import falcon
import jwt
from UserRepository import UserRepository


class AuthMiddleware:
    user_repository = UserRepository()

    def process_request(self, req, resp):
        if "/login" in req.path:
            return
        if req.get_header('Authorization'):
            auth_header = req.get_header('Authorization').split(" ")
            token = auth_header[1]
        else:
            description = "Missing Authorization Header"
            raise falcon.HTTPUnauthorized("Unauthorized", description)

        print("Token : {}".format(token))
        if not token:
            description = "Please provide an auth token as part of the request."
            raise falcon.HTTPUnauthorized("Unauthorized", description)
        if not self._is_token_valid(token):
            description = "The provided auth token is not valid.Please request a new token and try again."
            raise falcon.HTTPUnauthorized("Unauthorized", description)

    def _is_token_valid(self, token):
        try:
            payload = jwt.decode(token, "secret", algorithms="HS256")
            user = self.user_repository.get_user_by_id(payload["user_id"])
            print("Authenticated, User : {}".format(user))
            return True
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False
