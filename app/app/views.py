from app import app
from flask import render_template

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