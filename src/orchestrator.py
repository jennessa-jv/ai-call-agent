from src.core.retry import retry
from src.core.circuit_breaker import CircuitBreaker
from src.core.exceptions import TransientError
from src.services.elevenlabs import synthesize_voice
from src.observability.logger import log
from src.alerts.telegram import send as send_telegram_alert
from src.alerts.email import send as send_email
from src.alerts.webhook import send as send_webhook
from src.config import RETRY_CONFIG, CIRCUIT_BREAKER_CONFIG


circuit_breaker = CircuitBreaker(
    name="ElevenLabs",
    failure_threshold=CIRCUIT_BREAKER_CONFIG["failure_threshold"],
    recovery_time=CIRCUIT_BREAKER_CONFIG["recovery_time"],
)


def handle_call(call_id: str):
    try:
        result = circuit_breaker.call(
            lambda: retry(
                synthesize_voice,
                retries=RETRY_CONFIG["retries"],
                initial_delay=RETRY_CONFIG["initial_delay"],
                backoff=RETRY_CONFIG["backoff"],
                retry_on=(TransientError,)
            )
        )
        print(f"✅ Call {call_id} succeeded: {result}")

    except Exception as e:
        # ---- LOG ----
        log({
            "event": "call_failed",
            "call_id": call_id,
            "service": "ElevenLabs",
            "error_category": "Transient",
            "retry_count": RETRY_CONFIG["retries"],
            "circuit_state": circuit_breaker.state
        })

        # ---- ALERTS ----
        send_telegram_alert(
            f"🚨 ElevenLabs failure for call {call_id}. Moving to next contact."
        )

        send_email(
            subject="ElevenLabs Circuit Open",
            body=(
                f"Call {call_id} failed after retries.\n"
                f"Circuit state: {circuit_breaker.state}"
            )
        )

        send_webhook({
            "service": "ElevenLabs",
            "call_id": call_id,
            "event": "circuit_opened",
            "state": circuit_breaker.state
        })

        # ---- GRACEFUL DEGRADATION ----
        move_to_next_call(call_id)


def move_to_next_call(call_id: str):
    print(f"➡ Skipping call {call_id}. Moving to next contact in queue.")
