from flask import Flask, render_template, jsonify, request, redirect, Blueprint

from elicelibrary.models import Book

book = Blueprint('book', __name__)

# 메인 페이지
@book.route('/')
def main_page():
    book_list = Book.query.order_by(Book.registered_date.desc())
    return render_template("main.html", book_list=book_list)

# 책 개별 소개 페이지 
@book.route('/book/<int:book_id>', methods=["GET"])
def book_detail():
    return render_template("book_detail.html")