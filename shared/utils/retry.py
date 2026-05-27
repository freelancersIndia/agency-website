import time
import random
from typing import Callable, TypeVar

from shared.logging.logger import logger

T = TypeVar("T")

def execute_with_retry(
    func: Callable[[], T],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> T:
    """
    Executes a function with exponential backoff and optional jitter.
    """
    delay = initial_delay
    for attempt in range(1, max_retries + 2):
        try:
            return func()
        except Exception as e:
            if attempt > max_retries:
                logger.error(f"Operation failed permanently after {max_retries} attempts: {str(e)}")
                raise e

            # Compute backoff with exponential growth
            sleep_time = delay * (backoff_factor ** (attempt - 1))
            if jitter:
                sleep_time += random.uniform(0, 0.1 * sleep_time)

            logger.warning(
                f"Attempt {attempt}/{max_retries} failed: {str(e)}. "
                f"Retrying in {sleep_time:.2f} seconds..."
            )
            time.sleep(sleep_time)
