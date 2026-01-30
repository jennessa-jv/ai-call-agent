class ServiceError(Exception):
    def __init__(self, service: str, message: str):
        self.service = service
        super().__init__(message)

class TransientError(ServiceError):
    pass

class PermanentError(ServiceError):
    pass

class AuthError(PermanentError):
    pass

class QuotaExceededError(PermanentError):
    pass
