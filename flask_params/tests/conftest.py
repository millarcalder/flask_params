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

    def inject_context(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs, ctx=Context(env="testing"))

        return wrapper

    @app.route("/foo")
    @inject_context
    @inject_query_params(ignore_args=["ctx"])
    def foo(ctx, arg: str, kwarg: int = 123) -> dict:
        assert ctx.env == "testing"
        return {"arg": arg, "kwarg": kwarg}

    @app.route("/strict_foo")
    @inject_context
    @inject_and_validate_query_params(ignore_args=["ctx"])
    def foo_strict(ctx, arg: str, kwarg: int = 123) -> dict:
        assert ctx.env == "testing"
        return {"arg": arg, "kwarg": kwarg}

    @app.route("/no_type_hinting")
    @inject_context
    @inject_and_validate_query_params(ignore_args=["ctx"])
    def no_type_hinting(ctx, arg, kwarg=123) -> dict:
        assert ctx.env == "testing"
        return {"arg": arg, "kwarg": kwarg}

    yield app


@pytest.fixture()
def flask_client(flask_app):
    return flask_app.test_client()
