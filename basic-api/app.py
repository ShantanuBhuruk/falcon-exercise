import json
import falcon


class ObjectRequest:
    def on_get(self, req, resp):
        reqParams = json.loads(req.stream.read())
        resp.status = falcon.HTTP_200
        data = {
            "Name": "Shantanu",
            "Email Id": "shantanu.bhuruk@joshsoftware.com",
            "Age": 29,
            "Designation": "Sr. Software Developer"
        }
        output = {}
        if "method" not in reqParams:
            resp.status = falcon.HTTP_400
            output["value"] = "No method specified in request"
        else:
            if reqParams["method"] == "get-name":
                output["value"] = data["Name"]
            else:
                resp.status = falcon.HTTP_404
                output["value"] = None

        resp.body = json.dumps(output)
        print("Hello There...")


api = falcon.API()
api.add_route("/test", ObjectRequest())
