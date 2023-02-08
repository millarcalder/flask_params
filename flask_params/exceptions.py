import json

from flask import Flask
from flask import jsonify
from typing import Any


class TypeCheckException(Exception):
    def __init__(self, errors: dict):
        self.errors = errors


class ArgsException(Exception):
    def __init__(self, extra_args: list[str], missing_args: list[str]):
        self.extra_args = extra_args
        self.missing_args = missing_args


class _TypeJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if type(o) == type:
            return str(o)
        return super().default(o)


def register_error_handlers(app: Flask):
    @app.errorhandler(TypeCheckException)
    def handle_validation_error(e: TypeCheckException):
        # don't want to go adding a custom json encoder to the entire flask application
        return (
            jsonify(
                json.loads(json.dumps({"type_errors": e.errors}, cls=_TypeJsonEncoder))
            ),
            400,
        )

    @app.errorhandler(ArgsException)
    def handle_validation_error(e: ArgsException):
        res = {}
        if e.extra_args:
            res["extra_args"] = e.extra_args
        if e.missing_args:
            res["missing_args"] = e.missing_args
        return jsonify(res), 400
