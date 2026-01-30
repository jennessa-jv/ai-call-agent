# AI Call Agent – Error Recovery & Resilience System

## Overview
This repository implements a robust **Error Recovery & Resilience System** for an AI Call Agent that depends on multiple third-party services (e.g., ElevenLabs, LLM providers, CRM APIs).

The goal of this system is to:
- Detect failures
- Recover intelligently
- Prevent cascading outages
- Alert humans when required
- Continue operating gracefully during partial failures

This assignment focuses on **engineering maturity and system design**, not just correctness.

---

## Architecture Decisions

The system is designed with clear separation of concerns and fault isolation.

High-level flow:

Call Queue  
→ Orchestrator  
→ Circuit Breaker (per service)  
→ Retry Engine (exponential backoff)  
→ External Service (e.g., ElevenLabs)

Key decisions:
- **Per-service circuit breakers** to isolate failures and avoid cascading outages
- **Retry logic separated from business logic**
- **Error-type–driven behavior** using a custom exception hierarchy
- **Configuration-driven parameters** for retries and circuit breakers
- **Mocked external integrations** to keep the system testable and secure

---

## Error Flow

1. A call is picked from the queue
2. The orchestrator invokes an external dependency
3. Errors are classified using custom exceptions
4. Transient errors are retried with exponential backoff
5. If retries fail:
   - The call is marked as failed
   - Alerts are triggered
   - The circuit breaker opens
6. The system skips the failed call and moves to the next contact
7. Health checks continue running
8. Once the service is healthy again, the circuit breaker resets and processing resumes

---

## Error Categorization

A custom exception hierarchy is used:

- **TransientError**
  - Timeouts
  - 503 Service Unavailable
  - Network failures  
  → Eligible for retry

- **PermanentError**
  - Authentication failures
  - Invalid payloads
  - Quota exceeded  
  → Fail fast (no retries)

System behavior is driven by **error type**, not HTTP status codes alone.

---

## Retry Logic & Circuit Breaker Behavior

### Retry Logic
- Retries are configurable
- Retries apply **only to transient errors**
- Exponential backoff prevents retry storms

Retry pattern:
5 seconds → 10 seconds → 20 seconds (maximum 3 attempts)

### Circuit Breaker
Each external service has its own circuit breaker with three states:
- **CLOSED** – normal operation
- **OPEN** – fail fast, no calls allowed
- **HALF-OPEN** – probe state to test recovery

The circuit breaker opens after repeated failures and automatically resets once the service becomes healthy again.

---

## Alerting Logic

Alerts are triggered when:
- A circuit breaker opens
- A call permanently fails
- A dependency remains unavailable beyond a threshold

Supported alert channels:
- Email (mocked)
- Telegram (mocked)
- Webhook (mocked)

All alert channels are fully wired but mocked to avoid external dependencies and secrets.

---

## Logging & Observability

### Logging Destinations
- Local structured log file (`logs/system.log`)
- Google Sheets–ready logger (mocked for non-technical visibility)

### Logged Fields
- Timestamp
- Call ID
- Service name
- Error category
- Retry count
- Circuit breaker state
- Event type

Example log entry:
```json

{
  "timestamp": "2026-01-29T12:11:08Z",
  "event": "call_failed",
  "service": "ElevenLabs",
  "error_category": "Transient",
  "retry_count": 3,
  "circuit_state": "OPEN",
  "call_id": "CALL_123"
}
<img width="1621" height="1068" alt="Screenshot 2026-01-30 104755" src="https://github.com/user-attachments/assets/1e805631-1485-4b1f-a57a-5c08dfbfa090" />
<img width="1621" height="1068" alt="Screenshot 2026-01-30 104755" src="https://github.com/user-attachments/assets/dc801982-7258-49c9-b08e-7eaeb349392a" />


