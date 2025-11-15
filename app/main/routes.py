# Import Blueprint to group related routes (pages)
# Import render_template to load and display HTML files
from flask import Blueprint, render_template

# --------------------------------------------
# Create a Blueprint for the "main" part of the site
# --------------------------------------------
# "main" → the name of this blueprint (used when registering it in create_app)
# __name__ → tells Flask where this file is located (so it can find templates)
# template_folder="templates" → tells Flask that the HTML files
# for this blueprint live inside a folder called "templates"
main_bp = Blueprint("main", __name__, template_folder="templates")


# --------------------------------------------
# Route 1: Home page ('/')
# --------------------------------------------
# When someone visits the main website (like http://127.0.0.1:5000/),
# this function will run and show the index.html file.
@main_bp.route("/")
def index():
    # Render (display) the HTML file located at:
    # app/main/templates/main/index.html
    return render_template("main/index.html")


# --------------------------------------------
# Route 2: Feature demo page ('/feature')
# --------------------------------------------
# When someone visits http://127.0.0.1:5000/feature,
# this function will run and show the feature.html file.
@main_bp.route("/feature")
def feature():
    # Render the HTML file located at:
    # app/main/templates/main/feature.html
    return render_template("main/feature.html")
