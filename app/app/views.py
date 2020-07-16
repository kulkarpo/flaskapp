from app import app
from flask import render_template
from datetime import datetime
from flask import redirect, request
from flask import jsonify, make_response
import os
from werkzeug.utils import secure_filename
from flask import send_file, send_from_directory, abort, safe_join

@app.route("/")
def index():
    return render_template("public/index.html")
    # return "Hello World!"

@app.route("/about")
def about():
    return render_template("/public/about.html")

    #return """
    #<h1 style='color: red;'>I'm a red h1 heading! </h1>
    #<p> This is Paragraph tag </p>
    #<code> Flask is pretty <em> Amazing </em></code>"""

@app.route("/jinja")
@app.route("/jinja")
def jinja():

    # Strings
    my_name = "Pooja"

    # Integers
    my_age = 29

    # Lists
    langs = ["Python", "Bash", "C", "C++"]

    # Dictionaries
    friends = {
        "Phani": 29,
        "Sukanya": 26,
        "Neha": 26,
        "Akshata": 29,
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/kulkarpo/flaskapp"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    date = datetime.utcnow()

    my_html = "<h1>This is some HTML</h1>"

    #suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date = clean_date(date), my_html=my_html,
    )

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":

        req = request.form
        #print(req)

        userid = request.form["userid"]
        username = request.form["username"]
        bio = request.form["bio"]
        email = request.form["email"]
        password = request.form["password"]

        users[userid] = {"name": username,
                         "twitter_handle": "@"+userid,
                         "bio": bio}

        missing = list()

        for key, value in req.items():
            if value == "":
                missing.append(key)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign_up.html", feedback=feedback)

        return redirect(request.url)

    return render_template("public/sign_up.html")


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)
    #return render_template("public/profile.html")


@app.route("/json", methods=['POST', 'GET'])
def json():

    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            print(req)
            response_body = {
                "name": req.get("name"),
                "message": req.get("message")
            }
            return make_response(jsonify(response_body), 200)

        else:
            return make_response(jsonify({"Message":"Not a json object! Try again.."}), 400)

    else:
        return "Recieved GET request"


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()
    print(req)

    res = make_response(jsonify({"message": "OK"}), 200)
    return res

@app.route("/query")
def query():
    """args = request.args
    print(args)

    for k, v in args.items():
        print(k + ":" + v)
        print(f"{k} : {v}")"""

    print(app.config)

    if request.args:
        args = request.args
        serialised = "".join(f"{k} : {v}" for k,v in args.items())
        return f"(Query) {serialised}", 200
    return "No query strings recieved", 200


app.config["IMAGE_UPLOADS"] = "/Users/pk/Documents/Studies/selflearn/flaskapp/app/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_IMAGE_FILESIZE'] = 50 * 1024 * 1024


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


def allowed_imagetype(image_filename):
    if "." in image_filename:
        ext = image_filename.rsplit(".", 1)[1]

        if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
    return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == 'POST':
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_imagetype(image.filename):
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                print("Image saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed ")
                return redirect(request.url)
    return render_template("public/upload_image.html")


app.config["CLIENT_IMG_FILES"] = "/Users/pk/Documents/Studies/selflearn/flaskapp/app/app/static/client/img"
app.config["CLIENT_PDF_FILES"] = "/Users/pk/Documents/Studies/selflearn/flaskapp/app/app/static/client/pdf"


@app.route("/get-image/<img_name>")
def get_image(img_name):
    try:
        return send_from_directory(app.config["CLIENT_IMG_FILES"], filename=img_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)