import json
import os
import strawberry
from datetime import datetime
from typing import List
from app.models import Message, MessageInput, Error
from typing import Union


DATA_FILE = "messages.json"

# Utility functions
def load_messages() -> List[Message]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Message(**msg) for msg in data]

def save_messages(messages: List[Message]):
    with open(DATA_FILE, "w") as f:
        json.dump([msg.__dict__ for msg in messages], f, indent=2)

# Initialize from file
messages = load_messages()
next_id = max((msg.id for msg in messages), default=0) + 1

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL!"

    @strawberry.field
    def get_messages(self) -> List[Message]:
        return messages
    
MessageResponse = strawberry.union("MessageResponse", (Message, Error))

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_message(self, input: MessageInput) -> MessageResponse:
        global next_id

        if not input.content.strip():
            return Error(message="Message content cannot be empty.")

        new_message = Message(
            id=next_id,
            content=input.content.strip(),
            timestamp=datetime.now().isoformat()
        )
        messages.append(new_message)
        save_messages(messages)
        next_id += 1
        return new_message


schema = strawberry.Schema(query=Query, mutation=Mutation)
