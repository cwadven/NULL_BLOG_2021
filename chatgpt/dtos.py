from dataclasses import dataclass


@dataclass
class ChatGPTConversationEntry:
    role: str
    content: str
