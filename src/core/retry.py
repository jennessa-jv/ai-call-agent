import time

def retry(fn, retries, initial_delay, backoff, retry_on):
    delay = initial_delay

    for attempt in range(1, retries + 1):
        try:
            return fn()
        except retry_on as e:
            if attempt == retries:
                raise
            time.sleep(delay)
            delay *= backoff
