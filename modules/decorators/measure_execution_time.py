import time
from functools import wraps


def measure_execution_time(func):
    """
    Decorator to measure the execution time of a function.

    :param func: The function to be measured.
    :return: Wrapped function with execution time measurement.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"[@] Function '{func.__name__}' executed in {execution_time:.4f} seconds."
        )
        return result

    return wrapper
