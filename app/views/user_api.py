from flask import Flask, render_template, jsonify, request, redirect, Blueprint, flash, url_for, session
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


user = Blueprint("user", __name__, url_prefix='/')


#회원가입
@user.route("/join", methods=["GET", "POST"])
def join():
    if request.method == 'GET' :
        return render_template("join.html")
    elif request.method == 'POST' :
        # 회원가입 -  중복 id 없는지 확인
        user_email = User.query.filter_by(email=request.form['useremail']).first()
        if not user_email :
            password = generate_password_hash(request.form['password']) 
            new_user = User(email=request.form['useremail'], password=password, name=request.form['username'], phone=request.form['phone'])
            db.session.add(new_user)
            db.session.commit()
            flash("회원가입이 완료되었습니다")

            return redirect(url_for('user.login'))
        else :
            flash("이미 가입된 이메일입니다.")
            return redirect(url_for('user.join'))

#로그인
@user.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email        = request.form['useremail']
        password     = request.form['password']

        user_data    = User.query.filter_by(email=email).first()

        if not user_data :
            flash("가입되지 않은 이메일입니다.")
            return redirect(url_for('user.login'))
        elif not check_password_hash(user_data.password, password):
            flash("잘못된 비밀번호 입니다.")            
            return redirect(url_for('user.login'))   #+)비밀번호만 틀렸을 때 전에 입력한 아이디는 남겨주기
        else :
            session.clear()
            session['login_id'] = user_data.email
            flash("로그인 성공")  
            return redirect(url_for('book.main_page'))


#로그아웃
@user.route("/logout")
def logout():
    session["login_id"] = None
    flash("로그아웃 성공")
    return redirect(url_for('book.main_page'))
