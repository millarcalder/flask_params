import functools
import inspect

from dataclasses import dataclass
from inspect import Parameter
from typing import Any

from flask_params.exceptions import TypeCheckException


@dataclass
class _TypeCheckResponse:
    valid: bool
    casted_val: Any = None
    error: dict | None = None


def _type_check(val: any, param: Parameter) -> _TypeCheckResponse:
    val_type = type(val)
    expected_type = param.annotation

    try:
        return _TypeCheckResponse(valid=True, casted_val=expected_type(val))
    except:
        return _TypeCheckResponse(
            valid=False,
            error={"val": val, "type": val_type, "expected_type": expected_type},
        )


def validate_arguments(func):
    """
    Checks the types of each arg and kwarg, if an arg is not of the correct type it attempts to cast the value to the correct type.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        sig_args = {
            list(sig.parameters.keys())[i]: list(sig.parameters.values())[i]
            for i in range(len(args))
            if i < len(sig.parameters)
        }

        casted_args = []
        casted_kwargs = {}
        errors = {}

        # Type check the args
        for i in range(len(args)):
            # Extra arg - leave it up to the python interpretter to raise a TypeError
            if i >= len(sig_args):
                casted_args.append(args[i])
                continue

            param = list(sig_args.values())[i]
            val = args[i]
            res = _type_check(val, param)

            if res.valid:
                casted_args.append(res.casted_val)
            else:
                errors[param.name] = res.error

        # Type check the kwargs
        for key, val in kwargs.items():
            # Extra kwarg - leave it up to the python interpretter to raise a TypeError
            # (the kwarg is either not in the method signature or also passed as an arg)
            if key not in sig.parameters or key in sig_args:
                casted_kwargs[key] = val
                continue

            param = sig.parameters[key]
            res = _type_check(val, param)

            if res.valid:
                casted_kwargs[key] = res.casted_val
            else:
                errors[key] = res.error

        # Uh oh!
        if errors:
            raise TypeCheckException(errors)

        # All good!
        return func(*casted_args, **casted_kwargs)

    return wrapper
