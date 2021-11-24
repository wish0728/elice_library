from flask import Flask, render_template, jsonify, request, redirect, Blueprint, flash, url_for
from sqlalchemy.orm import query
from elicelibrary.models import *
import csv

book = Blueprint('book', __name__, url_prefix='/')

# 메인 페이지
@book.route('/')
def main_page():
    book_list = Book.query.order_by(Book.registered_date.desc()).all()
    # db에 내용 없으면 csv를 넣는 코드 - 최초에 db가 없을때만 실행됨.
    # registered_date 기준으로 한 이유는 추후 새로 책이 입고될 때 새로 입고된 책들이 상단에 뜨도록 하기 위함.

    #!) 애초에 여기서 book_list 에 book_status에 따라서 abandon도서는 한 번 걸러줘야함
    
    if not book_list : 
    
        f = open('booklist.csv', 'r', encoding='utf-8')
        data = csv.reader(f, delimiter=',')
        booklist = []
        for row in data :
            booklist.append(row)
        f.close()

        for i in booklist[1:]:
            book_info = Book(title=i[1], publisher=i[2], author=i[3], publication_date=i[4], pages=i[5], isbn=i[6][:-1], description=i[7], book_link=i[8], book_status="1")
            db.session.add(book_info)
            db.session.commit()
    
    # 책을 무슨 기준으로 보여줄거니? -> 물리적 실체가 아니라 개념적 실체를 가르는 isbn으로 보여줄거임
    # 즉 isbn이 같으면 같은 책이기 때문에 하나로 보여줄거임
    # 따라서 쿼리문으로 book_list에 넣어줄 내용이 distinct를 써서 isbn당 하나만 나오게 만들어야하는데 어떻게 하는지 모르겠네 -> 질문

    return render_template("main.html", book_list=book_list)






# 책 개별 소개 페이지 
@book.route('/book_info/<int:book_id>', methods=["GET"])
def book_detail(book_id):
    # 첵정보 불러오기
    book_info = Book.query.filter(Book.id == book_id).first()
    # isbn이 같은 리뷰 전부 불러오기
    book_review = Review.query.filter(Review.isbn == book_info.isbn).all()
    # 리뷰갯수, 리뷰 평균별점
    rating_sum, rating_avg = 0, 0
    if book_review :
        for review in book_review:
            rating_sum += review.rating
        rating_avg = rating_sum / len(book_review)
    return render_template("book_detail.html", book = book_info, review = book_review, rating_avg = rating_avg)



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
    writer_id = "123"
    isbn = "9791196440916"
    review = Review(rating=write_rating, content=write_content, user_id=writer_id , isbn=isbn)
    db.session.add(review)
    db.session.commit()

    flash('리뷰 썼어!')
    return redirect(url_for('book.book_detail', book_id=book_id))




# 대여기록
@book.route('/checkout_records', methods=["GET", "POST"])
def user_records():
    return jsonify({"result":"user_records"})

# 반납하기
@book.route('/return', methods=["GET", "POST"])
def book_return():
    return jsonify({"result":"book_return"})


