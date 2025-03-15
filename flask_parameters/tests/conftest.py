import dataclasses
import functools
import pytest

from flask import Flask
from flask_parameters import Flask as FlaskParameters
from flask_parameters import inject_query_params
from flask_parameters import inject_and_validate_query_params
from flask_parameters import register_error_handlers


@dataclasses.dataclass
class Context:
    env: str


@pytest.fixture()
def flask_app():
    app = Flask("testing_app")
    register_error_handlers(app)

    # This is checking that other decorators can be used in conjunction
    # with the query parameter decorators.
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

    @app.route("/url_arguments/<int:url_argument>")
    @inject_context
    @inject_and_validate_query_params(ignore_args=["ctx"])
    def url_arguments(ctx, url_argument: int, arg: str, kwarg: int = 123) -> dict:
        assert ctx.env == "testing"
        return {"url_argument": url_argument, "arg": arg, "kwarg": kwarg}

    yield app


@pytest.fixture()
def flask_parameters_app():
    app = FlaskParameters("testing_app")

    # This is checking that other decorators can be used in conjunction
    # with the query parameter decorators.
    def inject_context(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs, ctx=Context(env="testing"))

        return wrapper

    @app.route("/foo", ignore_args=["ctx"])
    @inject_context
    def foo(ctx, arg, kwarg=123) -> dict:
        assert ctx.env == "testing"
        return {"arg": arg, "kwarg": kwarg}

    @app.route("/strict_foo", ignore_args=["ctx"])
    @inject_context
    def foo_strict(ctx, arg: str, kwarg: int = 123) -> dict:
        assert ctx.env == "testing"
        return {"arg": arg, "kwarg": kwarg}

    @app.route("/url_arguments/<int:url_argument>", ignore_args=["ctx"])
    @inject_context
    def url_arguments(ctx, url_argument: int, arg: str, kwarg: int = 123) -> dict:
        assert ctx.env == "testing"
        return {"url_argument": url_argument, "arg": arg, "kwarg": kwarg}

    yield app


@pytest.fixture()
def flask_client(flask_app):
    return flask_app.test_client()


@pytest.fixture()
def flask_parameters_client(flask_parameters_app):
    return flask_parameters_app.test_client()
