import time

class CircuitBreaker:
    def __init__(self, name, failure_threshold, recovery_time):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure = None

    def call(self, fn):
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.recovery_time:
                self.state = "HALF_OPEN"
            else:
                raise Exception(f"{self.name} circuit open")

        try:
            result = fn()
            self._reset()
            return result
        except Exception:
            self._record_failure()
            raise

    def _record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

    def _reset(self):
        self.failures = 0
        self.state = "CLOSED"
