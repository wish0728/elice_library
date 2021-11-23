from flask import Flask, render_template, jsonify, request, redirect, Blueprint
from flask.helpers import url_for
from sqlalchemy.orm import query
from elicelibrary.models import *
import csv

book = Blueprint('book', __name__, url_prefix='/')

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
def book_detail(book_id):
    book_info = Book.query.filter(Book.id == book_id).first()
    book_review = Review.query.filter(Review.isbn == book_info.isbn).all()
    return render_template("book_detail.html", book = book_info, book_review = book_review)


# 리뷰 작성
@book.route('/review/<int:book_id>', methods=["POST"])
def write_review(book_id):   
    # login한 session이 있으면 작성, 없으면 로그인 페이지로 이동
    '''
    if not session['login_id']:
        return redirect(url_for(user.login))
    '''


    # user_id = session['user_id']    -> 이 로그인 세션을 어디서 어떻게 가져와야 하지?? 
    write_rating = request.form['star']
    write_content = request.form['review']
    # writer_id = 
    # isbn = 
    review = Review(rating=write_rating, content=write_content, user_id=writer_id , isbn=isbn)
    db.session.add(review)
    db.session.commit()







# 대여기록
@book.route('/checkout_records', methods=["GET", "POST"])
def user_records():
    return jsonify({"result":"user_records"})

# 반납하기
@book.route('/return', methods=["GET", "POST"])
def book_return():
    return jsonify({"result":"book_return"})


