from flask.testing import FlaskClient


def test_success_with_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/foo?arg=bar&kwarg=456")
    assert res.status_code == 200
    assert res.json["arg"] == "bar"
    assert res.json["kwarg"] == "456"


def test_success_without_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/foo?arg=123")
    assert res.status_code == 200
    assert res.json["arg"] == "123"
    assert (
        res.json["kwarg"] == 123
    )  # inject_query_params won't cast kwarg into an int, but the default value is an int


def test_failure_no_query_params(flask_client: FlaskClient):
    res = flask_client.get("/foo")
    assert res.status_code == 400
    assert res.json == {"missing_args": ["arg"]}


def test_failure_with_extra_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/foo?arg=bar&kwarg=456&extra=hello")
    assert res.status_code == 400
    assert res.json == {"extra_args": ["extra"]}
