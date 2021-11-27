from flask import Flask, render_template, jsonify, request, redirect, Blueprint, flash, url_for, session
from sqlalchemy import *
from app.models import *
from datetime import date, timedelta
import csv

book = Blueprint('book', __name__, url_prefix='/')

# 메인 페이지
@book.route('/')
def main_page():

    book_list = Book.query.order_by(Book.registered_date.desc()).all()
    # Book객체가 몇 개의 Review를 가지고 있는지 알고 싶을 때, Review목록의 수를 Book_id기준으로 묶은 후(grouped by), Book과 LEFT JOIN하면 됨 
    # 'SELECT * FROM Book LEFT JOIN (SELECT isbn, COUNT(rating), AVG(rating) FROM Review GROUP BY isbn) AS r ON Book.isbn = r.isbn;'


    # db에 내용 없으면 csv를 넣는 코드 - 최초에 db가 없을때만 실행됨.
    # registered_date 기준으로 한 이유는 추후 새로 책이 입고될 때 새로 입고된 책들이 상단에 뜨도록 하기 위함.
    
    if not book_list : 
    
        f = open('booklist.csv', 'r', encoding='utf-8')
        data = csv.reader(f, delimiter=',')
        booklist = []
        for row in data :
            booklist.append(row)
        f.close()

        for i in booklist[1:]:
            book_info = Book(title=i[1], publisher=i[2], author=i[3], publication_date=i[4], pages=i[5], isbn=i[6], description=i[7], book_link=i[8], book_status="1", at_user=None)
            db.session.add(book_info)
            db.session.commit()

        return redirect(url_for("book.main_page"))

    return render_template("main.html", book_list=book_list)



# 책 상세 페이지 
@book.route('/book_info/<int:book_id>', methods=["GET"])
def book_detail(book_id):
    book_info = Book.query.filter(Book.id == book_id).first()
    # isbn이 같은 리뷰 전부 불러오기
    book_review = Review.query.filter(Review.isbn == book_info.isbn).all()
    rating_sum, rating_avg = 0, 0
    if book_review :
        for review in book_review:
            rating_sum += review.rating
        rating_avg = round(rating_sum / len(book_review), 1)
    return render_template("book_detail.html", book = book_info, review_list = book_review, rating_avg = rating_avg, review_cnt = len(book_review))


# 리뷰 작성
@book.route('/review/<int:book_id>', methods=["POST"])
def write_review(book_id):   
    if 'login_id' not in session:
        flash('리뷰를 작성하시려면 로그인 해주세요.')
        return redirect(url_for('user.login'))

    write_rating = request.form['star']
    write_content = request.form['review']
    writer_id = session['login_id']
    book = Book.query.filter(Book.id == book_id).first()

    review = Review(rating=write_rating, content=write_content, user_id=writer_id , isbn=book.isbn)
    db.session.add(review)
    db.session.commit()

    flash('리뷰 등록!')
    return redirect(url_for('book.book_detail', book_id=book_id))




# 책 대여하기 기능
@book.route('/checkout/<int:book_id>', methods=["POST"])
def checkout(book_id):

    if session['login_id'] == None:
        flash("대출하시려면 로그인이 필요합니다.")
        return redirect(url_for('user.login'))

    else :
        checkoutbook = Book.query.filter(Book.id == book_id).first()
        user_id = session['login_id']

        # Book테이블에서 현재 대출신청한 책의 book_status를 바꾸기(대출중 0으로)
        if checkoutbook.book_status == "1":
            checkoutbook.book_status = "0"
            checkoutbook.at_user = user_id

        # checkoutRecords 테이블에 대출기록 추가
            checkout = checkoutRecords(book_id=checkoutbook.id, user_id=user_id, checkoutdate=date.today(), duedate=date.today()+timedelta(days=14), isbn=checkoutbook.isbn)
            db.session.add(checkout)
            db.session.commit()

            flash("대출처리되었습니다.")

            return redirect(url_for('book.main_page'))
        else :
            flash("현재는 대출하실 수 없습니다.")
            return redirect(url_for('book.main_page'))




# 대여기록/반납하기 - [대시보드]
@book.route('/dashboard', methods=["GET", "POST"])
def user_dashboard():
    if session['login_id'] == None:
        flash("대출기록을 확인하시려면 로그인을 해주세요.")
        return redirect(url_for('user.login'))
    else :
        login_id = session['login_id']

    # 현재 대출중인 책 / 과거에 대출했던 책 각각 불러오기
        checkout_list = db.session.query(checkoutRecords, Book).join(Book).filter((checkoutRecords.user_id == login_id) & (checkoutRecords.returndate == None)).all()
        checkout_count=len(checkout_list)

        return_records = db.session.query(checkoutRecords, Book).join(Book).filter((checkoutRecords.user_id == login_id) & (checkoutRecords.returndate != None)).all()
        return_count= len(return_records)

        return render_template("checkoutrecords.html", checkout_list=checkout_list, checkout_count=checkout_count, return_records=return_records, return_count=return_count)



# 반납기능
@book.route('/return/<int:book_id>', methods=["POST"])
def book_return(book_id):

    # 책 status 바꿔주기
    returnbook = Book.query.filter(Book.id == book_id).first()
    user_id = session['login_id']

    if returnbook.book_status == "0" :
        returnbook.book_status = "1" 
        returnbook.at_user = None

    # 대출기록에 return날짜 넣어주기
        return_record = checkoutRecords.query.filter((checkoutRecords.book_id == book_id)&(checkoutRecords.returndate==None)).first()
        return_record.returndate = date.today()

        db.session.commit()
        flash("반납이 완료되었습니다.")
        return redirect(url_for('book.user_dashboard'), )

    else :
        flash("관리자에게 문의하시기 바랍니다.")
        return redirect(url_for('book.user_dashboard'))
