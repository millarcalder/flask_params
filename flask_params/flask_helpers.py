import flask
import functools
import inspect

from flask_params.exceptions import ArgsException
from flask_params.type_checking import validate_arguments


def inject_query_params(ignore_args: list[str] = []):
    """
    Injects the query parameters into the decorated function checking that all required args are supplied and that no extra args are supplied.

    The query parameters are always injected in as kwargs. 
    """
    def constructor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            sig_params = {key: param for key, param in sig.parameters.items() if key not in ignore_args}

            # Look for extra args
            extra_args = []
            for key in flask.request.args.keys():
                if key not in sig_params:
                    extra_args.append(key)

            # Look for missing args
            missing_args = []
            for key, param in sig_params.items():
                if param.default == inspect._empty and key not in flask.request.args:
                    missing_args.append(key)

            # Uh oh!
            if extra_args or missing_args:
                raise ArgsException(extra_args, missing_args)

            # All good!
            return func(*args, **kwargs, **flask.request.args)

        return wrapper

    return constructor


def inject_and_validate_query_params(ignore_args: list[str] = []):
    def constructor(func):
        return inject_query_params(ignore_args=ignore_args)(validate_arguments(func))
    return constructor
