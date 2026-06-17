from src.core.exceptions.base import ServiceError


class UserAlreadyExistsError(ServiceError):
    pass


class UsernameAlreadyExistsError(ServiceError):
    pass


class UserNotFoundError(ServiceError):
    pass