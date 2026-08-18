from backend.src.core.exceptions.base import ServiceError


class UserAlreadyExistsError(ServiceError):
    pass


class UsernameAlreadyExistsError(ServiceError):
    pass


class InvalidCredentialsError(ServiceError):
    pass


class UserNotFoundError(ServiceError):
    pass