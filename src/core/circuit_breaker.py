import time

class CircuitBreaker:
    def __init__(self, name: str, failure_threshold: int, recovery_time: int):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def call(self, fn):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF_OPEN"
                print(f"🟡 Circuit HALF-OPEN for {self.name}")
            else:
                raise Exception(f"{self.name} circuit is OPEN")

        try:
            result = fn()
            self._reset()
            return result
        except Exception:
            self._record_failure()
            raise

    def _record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        print(f"❌ Failure {self.failures}/{self.failure_threshold} for {self.name}")

        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            print(f"🔴 Circuit OPEN for {self.name}")

    def _reset(self):
        if self.state != "CLOSED":
            print(f"🟢 Circuit CLOSED for {self.name}")
        self.failures = 0
        self.state = "CLOSED"
