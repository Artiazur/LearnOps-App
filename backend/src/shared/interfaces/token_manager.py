from abc import ABC, abstractmethod


class TokenManager(ABC):
    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass
    
    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        pass
        
    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass
        
    @abstractmethod
    def decode_access_token(self, token: str) -> dict:
        pass
    
    @abstractmethod
    def decode_refresh_token(self, token: str) -> dict:
        pass