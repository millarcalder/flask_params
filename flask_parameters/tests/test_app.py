from flask.testing import FlaskClient


def test__with_type_hints__success_with_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=bar&kwarg=456")
    assert res.status_code == 200
    assert res.json["arg"] == "bar"
    assert res.json["kwarg"] == 456


def test__with_type_hints__success_without_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=123")
    assert res.status_code == 200
    assert res.json["arg"] == "123"
    assert res.json["kwarg"] == 123


def test__with_type_hints__failure_no_query_params(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo")
    assert res.status_code == 400
    assert res.json == {"missing_args": ["arg"]}


def test__with_type_hints__failure_with_extra_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/strict_foo?arg=bar&kwarg=456&extra=hello")
    assert res.status_code == 400
    assert res.json == {"extra_args": ["extra"]}


def test__with_type_hints__invalid_kwarg(flask_client: FlaskClient):
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


def test__with_type_hints__arg_with_no_type_hinting(flask_client: FlaskClient):
    res = flask_client.get("/no_type_hinting?arg=123&kwarg=hello")
    assert res.status_code == 200


def test__with_type_hints__url_arguments(flask_client: FlaskClient):
    res = flask_client.get("/url_arguments/123?arg=hello&kwarg=456")
    assert res.status_code == 200
    assert res.json == {"url_argument": 123, "arg": "hello", "kwarg": 456}


def test__with_type_hints__url_arguments_with_invalid_url_argument(
    flask_client: FlaskClient,
):
    res = flask_client.get("/url_arguments/invalid?arg=hello&kwarg=456")
    assert res.status_code == 404


def test__with_type_hints__url_arguments_with_extra_arg(flask_client: FlaskClient):
    res = flask_client.get("/url_arguments/123?arg=hello&kwarg=456&url_argument=456")
    assert res.status_code == 400
    assert res.json == {"extra_args": ["url_argument"]}


def test__no_type_hints__success_with_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/foo?arg=bar&kwarg=456")
    assert res.status_code == 200
    assert res.json["arg"] == "bar"
    assert res.json["kwarg"] == "456"


def test__no_type_hints__success_without_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/foo?arg=123")
    assert res.status_code == 200
    assert res.json["arg"] == "123"
    assert (
        res.json["kwarg"] == 123
    )  # inject_query_params won't cast kwarg into an int, but the default value is an int


def test__no_type_hints__failure_no_query_params(flask_client: FlaskClient):
    res = flask_client.get("/foo")
    assert res.status_code == 400
    assert res.json == {"missing_args": ["arg"]}


def test__no_type_hints__failure_with_extra_kwarg(flask_client: FlaskClient):
    res = flask_client.get("/foo?arg=bar&kwarg=456&extra=hello")
    assert res.status_code == 400
    assert res.json == {"extra_args": ["extra"]}
