from core.retry import retry
from core.circuit_breaker import CircuitBreaker
from core.exceptions import TransientError
from services.elevenlabs import synthesize_voice
from alerts.telegram import send as alert
from observability.logger import log

cb = CircuitBreaker("ElevenLabs", failure_threshold=3, recovery_time=30)

def handle_call(call_id):
    try:
        return cb.call(lambda: retry(
            synthesize_voice,
            retries=3,
            initial_delay=5,
            backoff=2,
            retry_on=(TransientError,)
        ))
    except Exception as e:
        log({
            "service": "ElevenLabs",
            "error": str(e),
            "circuit_state": cb.state
        })
        alert("ElevenLabs failure — moving to next call")
        move_to_next_call()

def move_to_next_call():
    print("➡ Moving to next contact in queue")
