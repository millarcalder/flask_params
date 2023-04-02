import pytest
from flask_parameters.type_checking import validate_arguments
from flask_parameters.exceptions import TypeCheckException


@pytest.mark.parametrize(
    "args,kwargs",
    [((), {}), (("foo",), {}), ((), {"arg1": "foo"}), ((), {"arg2": "bar"})],
)
def test_missing_args(args, kwargs):
    @validate_arguments
    def some_func(arg1: str, arg2: str, kwarg: int = 123):
        ...

    with pytest.raises(TypeError):
        some_func(*args, **kwargs)


@pytest.mark.parametrize(
    "args,kwargs",
    [
        (("foo", 456, "bar"), {}),
        (("foo", 456), {"extra": "bar"}),
        (("foo",), {"kwarg": 456, "extra": "bar"}),
        (("foo",), {"extra": "bar"}),
    ],
)
def test_extra_args(args, kwargs):
    @validate_arguments
    def some_func(arg1: str, kwarg: int = 123):
        ...

    with pytest.raises(TypeError):
        some_func(*args, **kwargs)


@pytest.mark.parametrize(
    "args,kwargs",
    [
        (("foo", "bar"), {}),
        (("foo", "bar"), {"kwarg": 456}),
        (("foo", "bar", 456), {}),
        (("foo",), {"arg2": "bar"}),
        ((), {"arg1": "foo", "arg2": "bar"}),
        ((), {"arg1": "foo", "arg2": "bar", "kwarg": 456}),
    ],
)
def test_valid(args, kwargs):
    @validate_arguments
    def some_func(arg1: str, arg2: str, kwarg: int = 123):
        return True

    assert some_func(*args, **kwargs)


def test_invalid_types():
    """
    This function relies on casting values for type checking which is pretty straight forward, so don't want to get
    carried away testing all possible casting errors.
    """

    @validate_arguments
    def some_func(int_arg: int, float_arg: float, list_arg: list, dict_arg: dict):
        ...

    with pytest.raises(TypeCheckException) as err:
        some_func("3.2", "foo", list_arg=123, dict_arg=3.2)

    assert err.value.errors == {
        "int_arg": {"val": "3.2", "type": str, "expected_type": int},
        "float_arg": {"val": "foo", "type": str, "expected_type": float},
        "list_arg": {"val": 123, "type": int, "expected_type": list},
        "dict_arg": {"val": 3.2, "type": float, "expected_type": dict},
    }


def test_invalid_type_and_extra_arg():
    """
    Could argue either way whether the TypeError for the extra arg or the TypeCheckException should be raised first.
    Raising the TypeCheckException first is much easier.
    """

    @validate_arguments
    def some_func(arg: int):
        ...

    with pytest.raises(TypeCheckException):
        some_func("foo", "bar")
