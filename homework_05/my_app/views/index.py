from flask import Blueprint, render_template


about_app = Blueprint("about_app", __name__, url_prefix="/about/")


@about_app.route("/", endpoint="about")
def about_text():
    return render_template("about.html")
