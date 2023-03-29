from typing import Callable


def check_access_token(func: Callable):

    def wrapper(*args, **kwargs):
        request = args[1]
        auth = request.META.get('AUTHORIZATION')
        return func(*args, **kwargs)

    return wrapper




