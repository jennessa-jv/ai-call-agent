import time

def retry(fn, retries: int, initial_delay: int, backoff: int, retry_on: tuple):
    delay = initial_delay

    for attempt in range(1, retries + 1):
        try:
            return fn()
        except retry_on as e:
            print(f"⏳ Retry {attempt}/{retries} after error: {e}")
            if attempt == retries:
                raise
            time.sleep(delay)
            delay *= backoff
