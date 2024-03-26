from flask import Flask

from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'biblyozh_must_be_completed_at_any_cost'


def main():
    db_session.global_init("db/db.db")
    session = db_session.create_session()
    app.run()


if __name__ == '__main__':
    main()
