import json
import falcon
from StudentDbOperator import StudentDBOperator
api = falcon.API()
api.add_route("/student", StudentDBOperator())
