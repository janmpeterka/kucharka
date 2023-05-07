import pytest

from app import create_app
from app import db as _db

pytest_plugins = ["fixtures"]


# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "storage_state": "tests/helpers/auth.json",
#         "ignore_https_errors": True,
#     }


@pytest.fixture(scope="session")
def app():
    application = create_app(config_name="testing")

    @application.context_processor
    def utility_processor():
        from app.helpers.context_processors import human_format_date, formatted_amount

        return dict(
            human_format_date=human_format_date,
            formatted_amount=formatted_amount,
        )

    return application


@pytest.fixture(scope="session")
def db(app):
    # insert default data
    with app.app_context():
        try:
            _db.engine.execute("drop database kucharka_tests;")
            _db.engine.execute("create schema kucharka_tests;")
            _db.engine.execute("use kucharka_tests;")
            _db.engine.execute("SET FOREIGN_KEY_CHECKS = 0;")
            _db.drop_all()
            _db.create_all()
            _db.engine.execute("SET FOREIGN_KEY_CHECKS = 1;")
        except Exception:
            _db.create_all()

    return _db


@pytest.fixture(autouse=True, scope="function")
def data(db):
    _clear_db(db)
    db_create_roles(db)
    db_create_default_data()
    # db_create_data(db)


def _clear_db(db):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def db_create_roles(_db):
    from app import security

    roles = [
        security.datastore.create_role(
            name="admin",
            permissions="manage-application,manage-users,login-as,see-debug,see-other,edit-other",
        ),
        security.datastore.create_role(
            name="application_manager",
            permissions="manage-application,see-other,edit-other",
        ),
    ]

    for role in roles:
        role.save()

    users = [
        security.datastore.create_user(
            id=1, username="user", email="user@skautskakucharka.cz", password="navarit"
        ),
        security.datastore.create_user(
            id=2,
            username="application_manager",
            email="appmanager@skautskakucharka.cz",
            roles=["application_manager"],
            password="navarit",
        ),
        security.datastore.create_user(
            id=3,
            username="admin",
            email="admin@skautskakucharka.cz",
            roles=["admin"],
            password="navarit",
        ),
    ]

    for user in users:
        user.save()


def db_create_default_data():
    from app.models import IngredientCategory, Measurement

    IngredientCategory(name="Maso a masné výrobky").save()
    IngredientCategory(name="Mléčné výrobky").save()
    IngredientCategory(name="Ovoce a zelenina").save()
    IngredientCategory(name="Suché").save()
    IngredientCategory(name="Koření").save()

    Measurement(name="gramy").save()
    Measurement(name="kusy").save()
