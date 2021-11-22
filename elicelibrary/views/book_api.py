from flask import Flask, render_template, jsonify, request, redirect, Blueprint
from elicelibrary.models import *
import csv

book = Blueprint('book', __name__)

# 메인 페이지
@book.route('/')
def main_page():
    book_list = Book.query.order_by(Book.registered_date.desc()).all()
    # db에 내용 없으면 csv를 넣는 코드
    if not book_list : 
    
        f = open('booklist.csv', 'r', encoding='utf-8')
        data = csv.reader(f, delimiter=',')
        booklist = []
        for row in data :
            booklist.append(row)
        f.close()

        for i in booklist[1:]:
            book_info = Book(title=i[1], publisher=i[2], author=i[3], publication_date=i[4], pages=i[5], isbn=i[6], description=i[7], book_link=i[8])
            db.session.add(book_info)
            db.session.commit()
    else :
        return render_template("main.html", book_list=book_list)

# 책 개별 소개 페이지 
@book.route('/book/<int:book_id>', methods=["GET"])
def book_detail():
    return render_template("book_detail.html")