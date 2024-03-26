import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    author = sqlalchemy.Column(sqlalchemy.String)
    filename = sqlalchemy.Column(sqlalchemy.String)
    progress = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relationship('User')