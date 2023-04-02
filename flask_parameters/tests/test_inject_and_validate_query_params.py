from flask.testing import FlaskClient


def test_success_with_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=bar&kwarg=456")
    assert res.status_code == 200
    assert res.json["arg"] == "bar"
    assert res.json["kwarg"] == 456


def test_success_without_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=123")
    assert res.status_code == 200
    assert res.json["arg"] == "123"
    assert res.json["kwarg"] == 123


def test_failure_no_query_params(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo")
    assert res.status_code == 400
    assert res.json == {"missing_args": ["arg"]}


def test_failure_with_extra_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=bar&kwarg=456&extra=hello")
    assert res.status_code == 400
    assert res.json == {"extra_args": ["extra"]}


def test_invalid_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=123&kwarg=hello")
    assert res.status_code == 400
    assert res.json == {
        "type_errors": {
            "kwarg": {
                "val": "hello",
                "type": "<class 'str'>",
                "expected_type": "<class 'int'>",
            }
        }
    }


def test_arg_with_no_type_hinting(flask_client: FlaskClient):
    res = flask_client.get("/no_type_hinting?arg=123&kwarg=hello")
    assert res.status_code == 200
