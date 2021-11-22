import csv
from elicelibrary.models import Book, db

f = open('booklist.csv', 'r', encoding='utf-8')
data = csv.reader(f, delimiter=',')
booklist = []
for row in data :
    booklist.append(row)
f.close()


# [['\ufeffnumb', 'book_name', 'publisher', 'author', 'publication_date', 'pages', 'isbn', 'description', 'link']
for i in booklist:
    book_info = Book(title=i[1], publisher=i[2], author=i[3], publication_date=i[4], pages=i[5], isbn=i[6], description=i[7], book_link=i[8])
    db.session.add(book_info)
    db.session.commit()

