from enum import unique
from elicelibrary import db
from datetime import datetime

class User(db.Model):

    __tablename__     = 'User'

    email             = db.Column(db.String(45), primary_key=True, nullable=False, unique=True)
    password          = db.Column(db.String(255), nullable=False)
    name              = db.Column(db.String(45), nullable=True)
    phone             = db.Column(db.String(45), nullable=True)

    def __init__(self, email, password, name, phone):
        self.email      = email
        self.password   = password
        self.name       = name
        self.phone      = phone

class Book(db.Model):

    __tablename__     = 'Book'

    id                = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    title             = db.Column(db.String(45), nullable=False)
    author            = db.Column(db.String(45))
    publisher         = db.Column(db.String(45))
    publication_date  = db.Column(db.String(45))
    pages             = db.Column(db.Integer)
    isbn              = db.Column(db.String(45))
    registered_date   = db.Column(db.DateTime, default=datetime.utcnow)
    description       = db.Column(db.Text())    # 길이를 정할 수 없는 문자열은 Text를 쓰면 됨
    book_link         = db.Column(db.String(255))
    book_status       = db.Column(db.Integer)
    book_img          = db.Column(db.String(45))    # 책 표지만 바뀐 경우, 또는 책이 다르지만 같은 표지를 쓰는 경우가 있기 때문에 이미지 스토리지에서 같은 이미지의 반복을 막기 위해 별도의 책 이미지 식별 용 변수를 넣음

    def __init__(self, title, author, publisher, publication_date, pages, isbn, description, book_link) :
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_date = publication_date
        self.pages = pages
        self.isbn = isbn
        self.description = description
        self.book_link = book_link
        


class Review(db.Model):
    __tablename__     = 'Review'

    review_id         = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    rating            = db.Column(db.Integer)
    content           = db.Column(db.Text())
    user_id           = db.Column(db.String(45), nullable=False)
    isbn              = db.Column(db.String(45), db.ForeignKey('Book.isbn'))   # 외부키 사용할 때는 '테이블이름.속성', 객체 이름 x



class checkoutRecords(db.Model):
    __tablename__     = 'checkoutRecords'

    checkout_id       = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id           = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable=False)
    user_id           = db.Column(db.String(45), db.ForeignKey('User.email'), nullable=False)
    checkoutdate      = db.Column(db.Date, nullable=False)
    duedate           = db.Column(db.Date, nullable=False)
    returndate        = db.Column(db.Date)
    isbn              = db.Column(db.String(45))


