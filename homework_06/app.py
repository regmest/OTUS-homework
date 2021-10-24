import os

from flask import Flask, render_template
from flask_migrate import Migrate

from models.database import db
from views.books import books_app

app = Flask(__name__)
app.register_blueprint(books_app, url_prefix="/books")


SQLALCHEMY_DATABASE_URI = os.getenv("DB_CONN_URI", "postgresql+psycopg2://user:password@localhost:5432/books")
app.config.update(
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)
migrate = Migrate(app, db)

# main page
@app.route("/", endpoint="main")
def hello_world():
    return render_template("index.html")

# items
# @app.route("/item/")
# @app.route("/item/<int:item_id>/")
# def get_item(item_id: int = 42):
#     return {"item_id": item_id}
