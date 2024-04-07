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
        self.cover_path = f"covers/{'.'.join([str(id), format])}"

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
    user = orm.relationship('User')