from typing import Annotated, get_type_hints, get_origin, get_args
from pprint import pprint
from functools import wraps

def check_value_range(func):
    @wraps(func)
    def wrapper(x):
        hints = get_type_hints(func, include_extras=True)
        x_hint = hints['x']
        if get_origin(x_hint) is Annotated:
            x_type, *x_args = get_args(x_hint)
            low, high = x_args[0]
            if not low <= x <= high:
                raise ValueError(f'{x} should be {low} - {high}')
        return func(x)
    return wrapper



@check_value_range
def double(x: Annotated[int, (0, 100)]) -> int:

    return x *  2










x = int(input("enter x: "))
print(double(x))