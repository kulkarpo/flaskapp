from flask.views import MethodView
from flask import request, make_response, jsonify
import collections
from app import app

my_dict = collections.defaultdict(int)
my_dict["1"] = "one"


class myApp(MethodView):
    """
    /api/
    This class welcomes user
    TODO - temporarily add function to get all the keys in the system, remove later
    """
    def get(self):
        serialised = ""
        if my_dict:
            serialised = ", ".join(f"{k} : {v}" for k, v in my_dict.items())
        res = make_response(jsonify({"message": "Welcome to my app", "content": serialised}, 200))
        return res


class myAppCrud(MethodView):
    """
    /api/queue/<record>
    record in different methods

    request body for post in json format
    {
        key : <key>,
        value : <value>
    }

    """
    def get(self, key):
        """ expose value of a key if exists else 404"""
        if key in my_dict.keys():
            res = make_response(jsonify({key: my_dict[key]}, 200))
        else:
            res = make_response(jsonify({"message": "record not found"}, 404))
        return res

    def post(self):
        """ Create an record """
        res = ""
        if request.is_json:
            req = request.get_json()
            key = req.get("key")
            value = req.get("value")
            if key in my_dict.keys():
                res = make_response(jsonify({"message": "Key Already Exists"}, 409))
            else:
                my_dict[key] = value
                res = make_response(jsonify({"message": "Record inserted"}, 200))
        else:
            # sent as params
            args = None
            if request.args:
                args = request.args
                for k, v in args.items():
                    if k in my_dict:
                        res = make_response(jsonify({"message": "Key already present"}, 409))
                    else:
                        my_dict[k] = v
                        res = "".join(f"{k}: {v}" for k, v in my_dict.items())
                        res = make_response(jsonify({"message": "Record inserted"}, 200))
        if not res:
            res = make_response(jsonify({"message": "Format error"}, 400))

        return res

    def put(self, key):
        """ Update/replace a record """
        body = request.get_json()
        my_dict[key] = body.get("value", None)
        return make_response(jsonify({"message": "record updated", key : my_dict[key]}))

    def delete(self, key):
        """ delete a  record"""
        if key in my_dict.keys():
            del my_dict[key]
            res = make_response(jsonify({"message": "record deleted"}, {"key": key}, 200))
        else:
            res = make_response(jsonify({"message": "record not found"}, 404))
        return res



crud_view = myAppCrud.as_view('myapp_crud_api')
app.add_url_rule("/api/", view_func=myApp.as_view("myapp_api"))
app.add_url_rule('/api/myapp/', view_func=crud_view, methods=['POST',])
app.add_url_rule("/api/myapp/<key>", view_func=crud_view, methods=['GET', 'PUT', 'DELETE'])

"""
# TODO - store this in db
# dictionary to store users key:value pairs
my_dict = dict()
my_dict["1"] = "one"
my_dict["2"] = "two"


@app.route("/")
def index():
    # TODO remove this later
    serialised_content = ""
    if my_dict:
        serialised_content = ", ".join(f"{k} : {v}" for k, v in my_dict.items())
    return make_response(jsonify({"message": "Welcome to my app!"}, {"contents": serialised_content}, 200))


@app.route("/create", methods=['POST'])
def create():
    res = ""
    if request.is_json:
        req = request.get_json()
        print(req)
        key = req.get("key")
        value = req.get("value")
        print(key)
        print(value)
        if key in my_dict.keys():
            res = make_response(jsonify({"message": "Key Already Exists"}, 409))
        else:
            my_dict[key] = value
            res = make_response(jsonify({"message": "Record inserted"}, 200))
    else:
        # sent as params
        args = None
        if request.args:
            args = request.args
            for k, v in args.items():
                if k in my_dict:
                    res = make_response(jsonify({"message": "Key already present"}, 409))
                else:
                    my_dict[k] = v
                    res = "".join(f"{k}: {v}" for k, v in my_dict.items())
                    print(res)
                    res = make_response(jsonify({"message": "Record inserted"}, 200))
    if not res:
        res = make_response(jsonify({"message": "Format error"}, 400))

    return res


@app.route("/validate/<key>")
def validate(key):
    if key in my_dict.keys():
        res = make_response(jsonify({"message": "Found", key: my_dict[key]}, 200))
    else:
        res = make_response(jsonify({"message": "Not Found"}, 400))
    return res


@app.route("/read/<key>")
def get(key):
    if key in my_dict.keys():
        res = make_response(jsonify({key: my_dict[key]}, 200))
    else:
        res = make_response(jsonify({"message": "record not found"}, 400))

    return res
"""

