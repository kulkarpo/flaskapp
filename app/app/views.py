from app import app
from flask import render_template
from datetime import datetime

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
    return render_template("public/sign_up.html")