import random

from flask import Flask, render_template, redirect, abort, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.forms import LoginForm, RegisterForm, FileForm, NoteForm
from data.models import User, Book, Note
from data.data_handlers import file_handler

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
                        user_id=selected_user.id, last_page=1)
            book.set_cover_path(book_id, form.cover.data.filename)
            book.set_book_path(book_id, form.file.data.filename)
            form.cover.data.save(f'{"static/" + book.cover_path}')
            form.file.data.save(f'{"static/" + book.book_path}')
            book.work_size = len(file_handler(f"static/{book.book_path}", 1990))
            db_sess.add(book)
            db_sess.commit()
            return redirect('/')
        return render_template('upload.html', form=form)


# @app.route('/add_note')
# def add_note():
#     if oleg.is_authenticated:
#         db_sess = db_session.create_session()
#         selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
#         form = NoteForm()
#         if form.validate_on_submit():
#             db_sess = db_session.create_session()
#             note = Note(note=form.note)
#             db_sess.add(note, user_id=oleg.id, book_id=selected_book)
#             db_sess.commit()
#             return redirect('/')
#         return render_template('upload.html', form=form)

@app.route('/library')
def library():
    if oleg.is_authenticated:
        book_names = []
        db_sess = db_session.create_session()
        selected_books = db_sess.query(Book).filter(Book.user_id == oleg.id)
        for book in selected_books:
            name = book.name
            if len(name) > 27:
                name = name[:25] + '...'
            book_names.append((name, book.id))
        return render_template('library.html', books=selected_books, book_names=book_names)
    else:
        return redirect("/login")


@app.route('/reader/<int:book_id>/<int:current_page>', methods=["GET", "POST"])
def reader_selected(book_id, current_page):
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        note_form = NoteForm()
        selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
        selected_book = db_sess.query(Book).filter(Book.id == book_id).first()
        work_size = selected_book.work_size
        if selected_book.user_id != selected_user.id:
            return redirect('/library')  # Пользователь попытался открыть чужую книгу
        if work_size < current_page or current_page < 1:
            return redirect(f'/reader/{book_id}/1')
        next_page = 1 if current_page == work_size else current_page + 1
        prev_page = current_page - 1 if current_page != 1 else work_size
        bookmarks_data = selected_book.bookmarks
        if not bookmarks_data:
            have_bookmark = False
        else:
            if str(current_page) in selected_book.bookmarks.split(';'):
                have_bookmark = True
            else:
                have_bookmark = False
        if selected_book is not None:
            db_sess.query(User).filter(User.id == selected_user.id).update({"last_book": book_id})
            db_sess.query(Book).filter(Book.id == selected_book.id).update({"last_page": current_page})
            db_sess.commit()
            return render_template('reader.html', book=selected_book, user=selected_user, book_id=book_id,
                                   page=current_page, form=note_form, have_bookmark=have_bookmark, next_page=next_page,
                                   prev_page=prev_page, page_content=file_handler(f"./static/{selected_book.book_path}", 1990)[current_page - 1])
        else:
            abort(404)
    else:
        return redirect("/login")


@app.route('/reader/<int:book_id>/make_bookmark', methods=['POST'])
def make_bookmark(book_id):
    data = request.form.items()
    db_sess = db_session.create_session()
    selected_book = db_sess.query(Book).filter(Book.id == book_id).first()
    current_page = [*data][1][1]
    bookmarks = selected_book.bookmarks
    if not bookmarks:
        new_bookmarks = f'{current_page};'
    else:
        bookmarks_list = bookmarks.split(';')
        if str(current_page) not in bookmarks_list:
            new_bookmarks = bookmarks + f'{current_page};'
        else:
            bookmarks_list.remove(str(current_page))
            new_bookmarks = ';'.join(bookmarks_list)
    db_sess.query(Book).filter(Book.id == selected_book.id).update({"bookmarks": new_bookmarks})
    db_sess.commit()
    return make_response('you are not supposed to see this, get the hell out of here')


@app.route('/reader/<int:book_id>/highlight', methods=['POST'])
def make_highlight(book_id):
    data = [*request.form.items()]
    if len(data) == 3:
        start = data[0][1]
        end = data[1][1]
        page = data[2][1]
        save_data = f'{start},{end},{page};'
        db_sess = db_session.create_session()
        selected_book = db_sess.query(Book).filter(Book.id == book_id).first()
        highlighted = selected_book.highlighted
        if not highlighted:
            highlighted = save_data
        else:
            highlighted = highlighted + save_data
        db_sess.query(Book).filter(Book.id == selected_book.id).update({"highlighted": highlighted})
        db_sess.commit()
    return make_response('you are not supposed to see this, get the hell out of here')


@app.route('/reader/<int:book_id>/make_note', methods=['POST'])
def make_note(book_id):
    data = [*request.form.items()]
    note = data[0][1]
    content = data[1][1]
    page = data[2][1]
    db_sess = db_session.create_session()
    if content:
        short_content = content[:140] + '...'
        note = Note(user_id=oleg.id, book_id=book_id, content=content, short_content=short_content, page=page,
                    note=note)
        db_sess.add(note)
        db_sess.commit()
    return make_response('you are not supposed to see this, get the hell out of here')


@app.route('/reader')
def reader_last():
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
        selected_book = db_sess.query(Book).filter(Book.id == selected_user.last_book).first()
        if selected_book is not None:
            return redirect(
                f"/reader/{selected_book.id}/{selected_book.last_page}")
        else:
            abort(404)
    else:
        return redirect("/login")


@app.route('/reader/<int:book_id>')
def reader_last_page(book_id):
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_book = db_sess.query(Book).filter(Book.id == book_id).first()
        if selected_book is not None:
            return redirect(
                f"/reader/{book_id}/{selected_book.last_page}")
        else:
            abort(404)
    else:
        return redirect("/login")


@app.route('/about/<int:book_id>')
def about(book_id):
    if oleg.is_authenticated:
        db_sess = db_session.create_session()
        selected_user = db_sess.query(User).filter(User.id == oleg.id).first()
        selected_book = db_sess.query(Book).filter(Book.id == book_id and Book.user_id == oleg.id).first()
        if selected_user.id != selected_book.user_id:
            return redirect('/library')
        selected_notes = db_sess.query(Note).filter(Note.book_id == book_id and Note.user_id == oleg.id)
        bookmarks = selected_book.bookmarks
        if bookmarks:
            bookmarks = list(sorted(list(map(int, bookmarks.split(';')[:-1]))))
            last_bookmark = bookmarks[-1]
            bookmarks.pop(-1)
        else:
            bookmarks = []
            last_bookmark = None
        if selected_book is not None:
            return render_template('info.html', book=selected_book, notes=selected_notes, bookmarks=bookmarks,
                                   last_bookmark=last_bookmark)
        else:
            abort(404)
    else:
        return redirect("/login")


@app.route('/about/<int:book_id>/delete_note/<int:note_id>')
def delete_note(book_id, note_id):
    db_sess = db_session.create_session()
    db_sess.query(Note).filter(Note.id == note_id).delete()
    db_sess.commit()
    return redirect(f'/about/{book_id}')


def main():
    db_session.global_init("db/db.db")
    app.run(debug=True)


if __name__ == '__main__':
    oleg = current_user
    main()
