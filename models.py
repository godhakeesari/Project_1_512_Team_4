import strawberry
from typing import Union

@strawberry.type
class Error:
    message: str

@strawberry.type
class Message:
    id: int
    content: str
    timestamp: str

@strawberry.input
class MessageInput:
    content: str
