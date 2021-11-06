import logging

from http import HTTPStatus
from sqlalchemy.exc import IntegrityError, DatabaseError
from flask import Blueprint, request, render_template, url_for, redirect
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from models.book import Book
from models.database import db


log = logging.getLogger(__name__)

books_app = Blueprint("books_app", __name__, url_prefix="/books")


@books_app.route("/", endpoint="list")
def list_books():
    books = Book.query.all()
    return render_template("books/list.html", books=books)


@books_app.route("/<int:book_id>/", methods=["GET", "DELETE"], endpoint="details")
def get_book(book_id: int):

    book = Book.query.filter_by(id=book_id).one_or_none()

    if book is None:
        raise NotFound(f"Book №{book_id} doesn't exist!")

    # To get data
    if request.method == "GET":
        return render_template(
            "books/details.html",
            book=book,
        )

    # to delete data
    db.session.delete(book)
    try:
        db.session.commit()
    except DatabaseError:
        log.exception("Could not delete book %, got database error", book)
        db.session.rollback()
        raise InternalServerError("Error deleting book")
    return "", HTTPStatus.NO_CONTENT


@books_app.route("/add/", methods=["GET", "POST"], endpoint="add")
def add_book():
    if request.method == "GET":
        return render_template("books/add.html")

    book_title = request.form.get("book-title")
    book_author = request.form.get("book-author")
    if not book_title:
        raise BadRequest("Field 'Title' is required!")
        # raise BadRequest("Field 'book-title' is required!")
    elif not book_author:
        raise BadRequest("Field 'Author' is required!")

    book = Book(title=book_title, author=book_author)
    db.session.add(book)
    try:
        db.session.commit()
    except IntegrityError:
        log.exception("Couldn't add book, git integrity error")
        db.session.rollback()
        raise BadRequest("Error adding new book, probably the title is not unique")
    except DatabaseError:
        log.exception("Could not add book, got database error")
        db.session.rollback()
        raise InternalServerError("Error adding new book")

    url = url_for("books_app.details", book_id=book.id)

    return redirect(url)







