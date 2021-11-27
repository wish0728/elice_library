from flask import Flask, render_template, jsonify, request, redirect, Blueprint, flash, url_for, session
from sqlalchemy.orm import query
from elicelibrary.models import *
from datetime import date, timedelta
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
            book_info = Book(title=i[1], publisher=i[2], author=i[3], publication_date=i[4], pages=i[5], isbn=i[6][:-1], description=i[7], book_link=i[8], book_status="1", at_user=None)
            db.session.add(book_info)
            db.session.commit()
        
        return render_template("main.html", book_list=book_list)

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
    return render_template("book_detail.html", book = book_info, review_list = book_review, rating_avg = rating_avg, review_cnt = len(book_review))




# 리뷰 작성
@book.route('/review/<int:book_id>', methods=["POST"])
def write_review(book_id):   
    # login한 session이 있으면 작성, 없으면 로그인 페이지로 이동

    if 'login_id' not in session:
        flash('리뷰를 작성하시려면 로그인 해주세요.')
        return redirect(url_for('user.login'))

    # user_id = session['user_id']    -> 이 로그인 세션을 어디서 어떻게 가져와야 하지?? 
    write_rating = request.form['star']
    write_content = request.form['review']
    writer_id = session['login_id']
    
    # isbn을 db에서 쿼리문으로 현재 페이지의 책 id랑 같은 애로 필터해서 걔의 isbn을 불러오기
    book = Book.query.filter(Book.id == book_id).first()

    review = Review(rating=write_rating, content=write_content, user_id=writer_id , isbn=book.isbn)
    db.session.add(review)
    db.session.commit()

    flash('리뷰 썼어!')
    return redirect(url_for('book.book_detail', book_id=book_id))




# 책 대여하기 기능 구현
@book.route('/checkout/<int:book_id>', methods=["POST"])
def checkout(book_id):

    if session['login_id'] == None:
        flash("대출하시려면 로그인이 필요합니다.")
        return redirect(url_for('user.login'))

    else :
        # 현재 대출신청한 책 Book db에서 book_status를 바꾸기(대출중 0으로)
        checkoutbook = Book.query.filter(Book.id == book_id).first()
        user_id = session['login_id']

        if checkoutbook.book_status == "1":
            checkoutbook.book_status = "0"
            checkoutbook.at_user = user_id
        # checkoutRecords db에 대출기록 추가
            # 가져올 정보: book_id, user_id, 대출날짜checkoutdate(오늘로 자동생성), 반납일duedate(2주후로 자동생성)
            # print(checkoutbook.isbn)
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

        checkout_list = db.session.query(checkoutRecords, Book).join(Book).filter(checkoutRecords.user_id == login_id).all()
        
        return_count=len(checkout_list)

        return render_template("checkoutrecords.html", checkout_list=checkout_list, cnt=return_count)



# 반납기능 구현
@book.route('/return/<int:book_id>', methods=["POST"])
def book_return(book_id):
    # 현재 책의 대출기록을 찾아야함
        # Book에서 status에 현재 로긴한 user_id 가 적혀있는 레코드 % book 해당 책이 현재 유저가 반납할 수 있는 책들임
        # -> checkoutRecords에서 
    

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

        return redirect(url_for('book.user_dashboard'), )

        # flash("반납이 처리되었습니다.")
        #return redirect(url_for('book.'))
    else :
        flash("관리자에게 문의하시기 바랍니다.")
        return redirect(url_for('book.user_dashboard'))
