from flask import Blueprint,render_template
about_auth = Blueprint("about_auth",__name__)

@about_auth.route("/about")
def about():
    return render_template("about.html")