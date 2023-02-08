import flask
import functools
import inspect

from flask_params.exceptions import ArgsException
from flask_params.type_checking import validate_arguments


def inject_query_params(func):
    """
    Injects the query parameters into the decorated function checking that all required args are supplied and that no extra args are supplied.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        # Look for extra args
        extra_args = []
        for key in flask.request.args.keys():
            if key not in sig.parameters:
                extra_args.append(key)

        # Look for missing args
        missing_args = []
        for key, param in sig.parameters.items():
            if param.default == inspect._empty and key not in flask.request.args:
                missing_args.append(key)

        # Uh oh!
        if extra_args or missing_args:
            raise ArgsException(extra_args, missing_args)

        # All good!
        return func(*args, **kwargs, **flask.request.args)

    return wrapper


def inject_and_validate_query_params(func):
    return inject_query_params(validate_arguments(func))
