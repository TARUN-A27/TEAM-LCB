import time 
import functools
import logging

logger = logging.getLogger(__name__)

class Timer:
    def __init__(self,label: str = None, log_level: int = logging.INFO):
        self.label = label or "elapsed"
        self.log_level = log_level
        self.start = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type,exc, tb):
        self.elapsed = time.perf_counter() - self.start
        logger.log(self.log_level, msg)

def timeit(label: str = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start =time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                logger.info(f"[TIMEIT]{fname}: {elapsed:.4f} s")
        return wrapper
    return decorator