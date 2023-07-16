import time

from excelgpt.util.log import logger

total_cost = 0
input_tokens = 0
output_tokens = 0


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f"Function {func.__name__} took {end_time - start_time:.6f}s to run.")
        return result

    return wrapper