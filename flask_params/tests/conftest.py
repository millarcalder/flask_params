import dataclasses
import functools
import pytest

from flask import Flask
from flask_params import inject_query_params
from flask_params import inject_and_validate_query_params
from flask_params import register_error_handlers


@dataclasses.dataclass
class Context:
    env: str


@pytest.fixture()
def flask_app():
    app = Flask("testing_app")
    register_error_handlers(app)

    @app.route("/foo")
    @inject_query_params
    def foo(arg: str, kwarg: int = 123) -> dict:
        return {"arg": arg, "kwarg": kwarg}

    @app.route("/strict_foo")
    @inject_and_validate_query_params
    def foo_strict(arg: str, kwarg: int = 123) -> dict:
        return {"arg": arg, "kwarg": kwarg}

    yield app


@pytest.fixture()
def flask_client(flask_app):
    return flask_app.test_client()
