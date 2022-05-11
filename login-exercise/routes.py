import falcon
from AuthMiddleware import AuthMiddleware
from login import LoginHandler as Login
from StudentDbOperator import StudentDBOperator


def get_app():
    app = falcon.App(middleware=[AuthMiddleware()])
    app.add_route("/login", Login())
    app.add_route("/student", StudentDBOperator())
    return app


