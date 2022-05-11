import json
import falcon
from StudentDbOperator import StudentDBOperator
app = falcon.App()
app.add_route("/student", StudentDBOperator())
