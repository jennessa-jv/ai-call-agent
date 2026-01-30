RETRY_CONFIG = {
    "retries": 3,
    "initial_delay": 5,
    "backoff": 2
}

CIRCUIT_BREAKER_CONFIG = {
    "failure_threshold": 3,
    "recovery_time": 30
}
