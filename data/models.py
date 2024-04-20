import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    last_book = sqlalchemy.Column(sqlalchemy.Integer)


class Book(SqlAlchemyBase):
    def set_cover_path(self, id, original_filename):
        format = secure_filename(original_filename).split(".")[-1]
        if id != "default":
            self.cover_path = f"covers/{'.'.join([str(id), format])}"
        else:
            self.cover_path = f"covers/default.png"

    def set_book_path(self, id, original_filename):
        format = secure_filename(original_filename).split(".")[-1]
        self.book_path = f"../static/books/{'.'.join([str(id), format])}"

    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    author = sqlalchemy.Column(sqlalchemy.String)
    cover_path = sqlalchemy.Column(sqlalchemy.String)
    book_path = sqlalchemy.Column(sqlalchemy.String)
    progress = sqlalchemy.Column(sqlalchemy.Integer)
    bookmarks = sqlalchemy.Column(sqlalchemy.String)
    last_page = sqlalchemy.Column(sqlalchemy.Integer)
    highlighted = sqlalchemy.Column(sqlalchemy.String, default='')
    user = orm.relationship('User')


class Note(SqlAlchemyBase):

    __tablename__ = "notes"

    # Сохраняет в строку два значения через `-`: `начало_курсора_выделения-конец_курсора_выделения` выбранной области
    def define_selected_part(self, start, end):
        self.selected_part = f"{start}-{end}"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    book_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("books.id"))
    content = sqlalchemy.Column(sqlalchemy.String, default="Вы не выделили текст при создании заметки") # То, что выделил пользователь
    note = sqlalchemy.Column(sqlalchemy.String) # То, что пользователь может написать, а может и не написать
    short_content = sqlalchemy.Column(sqlalchemy.String)
    page = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relationship('User')
    book = orm.relationship('Book')
