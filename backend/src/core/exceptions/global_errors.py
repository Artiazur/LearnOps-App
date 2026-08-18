from backend.src.core.exceptions.base import GlobalError

class SomethingWentWrong(GlobalError):
    def __init__(self, message: str | None = None):
        self.message = message