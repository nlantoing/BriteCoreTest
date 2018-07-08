from database import db, Client, Request, Product_Area
from requests_manager import create_app
import flask
import datetime
import contextlib

# TODO : REMOVEME and use alembic instead

@contextlib.contextmanager
def db_context():
    app = create_app()
    with app.app_context():
        yield


def init_db():
    with db_context():
        db.create_all()
        db.session.add_all([
            Client(name='Client A'),
            Client(name='Client B'),
            Client(name='Client C'),
            Client(name='Client D'),
            Client(name='Client E')])

        db.session.commit()

        db.session.add_all([
            Product_Area(name='Policies'),
            Product_Area(name='Billing'),
            Product_Area(name='Claims'),
            Product_Area(name='Reports')])

        db.session.commit()

        db.session.add(Request(
            title="Test request",
            description="Just populate the request table with one query to ease development",
            target_date = datetime.datetime.now(),
            priority=1,
            client_id=1,
            product_area_id=1))
        db.session.commit()


if __name__ == "__main__":
    init_db()
