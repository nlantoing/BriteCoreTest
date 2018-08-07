from database import db, User, Category, Project, Task
from app import create_app
import flask
import datetime
import contextlib

# TODO : REMOVEME and use alembic instead

@contextlib.contextmanager
def db_context(app):
    if app is None:
        app = create_app()
    with app.app_context():
        yield


def init_db(app=None):
    with db_context(app):
        db.create_all()
        db.session.add(User(
            name='Guest',
            salt='abc',
            password='test'))
        db.session.commit()

        db.session.add_all([
            Project(name='TaskManager'),
            Project(name='Astrarium'),
            Project(name='JavascriptBinaryTree'),
            Project(name='PathFinder')])

        db.session.commit()

        db.session.add_all([
            Category(name='Frontend'),
            Category(name='Backend'),
            Category(name='View'),
            Category(name='Admin')])
        db.session.commit()


        db.session.add(Task(
            title="Test request",
            description="Just populate the request table with one query to ease development",
            target_date = datetime.datetime.now(),
            priority=1,
            user_id=1,
            project_id=1,
            category_id=1))
        db.session.commit()


if __name__ == "__main__":
    init_db()
