import random

from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.forms import LoginForm, RegisterForm, FileForm
from data.models import User, Book

app = Flask(__name__)
app.config['SECRET_KEY'] = 'biblyozh_must_be_completed_at_any_cost'
WTF_CSRF_SECRET_KEY = 'biblyozh_must_be_completed_at_any_cost'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    if oleg.is_authenticated:
        return redirect("/library")
    else:
        return redirect("login")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/library")
        form.login.data = ''
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            form.login.data = ''
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            form.login.data = ''
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
        form = FileForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            book_id = random.randrange(100000)
            while db_sess.query(Book).filter(Book.id == book_id).first():
                book_id = random.randrange(100000)
            book = Book(id=book_id, name=form.name.data, author=form.author.data, work_size=-1,
                        user_id=selected_user.id)
            book.set_cover_path(book_id, form.cover.data.filename)
            book.set_book_path(book_id, form.file.data.filename)
            form.cover.data.save(f'{"static/" + book.cover_path}')
            form.file.data.save(f'{"static/" + book.book_path}')
            db_sess.add(book)
            db_sess.commit()
            return redirect('/')
        return render_template('upload.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/library')
def library():
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_books = db_sess.query(Book).filter(Book.user_id == oleg.id)
        return render_template('library.html', books=selected_books)
    else:
        return redirect("/login")


@app.route('/reader/<int:book_id>/<int:current_page>')
def reader_selected(book_id, current_page):
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
        selected_book = db_sess.query(Book).filter(Book.id == book_id).first()
        if selected_book is not None:
            db_sess.query(User).filter(User.id == selected_user.id).update({"last_book": book_id})
            db_sess.commit()
            return render_template('reader.html', book=selected_book, user=selected_user)
        else:
            abort(404)
    else:
        return redirect("/login")


@app.route('/reader')
def reader_last():
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
        selected_book = db_sess.query(Book).filter(Book.id == selected_user.last_book).first()
        if selected_book is not None:
            return redirect(
                f"/reader/{selected_book.id}/1")  # TODO: Доделать память для закладок, когда они будут реализованы (и поменять ссылки в reader.html, library.html)
        else:
            abort(404)
    else:
        return redirect("/login")


def main():
    db_session.global_init("db/db.db")
    app.run(debug=True)


if __name__ == '__main__':
    oleg = current_user  # TODO: Переименовать по-человечески переменную. Я никак не могу придумать нормальное название
    main()
