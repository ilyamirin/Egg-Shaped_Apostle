from typing import Callable
from typing import Any

def log_load(fn: Callable[[], Any], resource_name: str):
    print(f'Loading {resource_name}... ', end='', flush=True)
    result = fn()
    print(f'Complete', flush=True)
    return result
