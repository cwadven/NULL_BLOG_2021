import requests
from typing import List

from chatgpt.consts import CHATGPT_URL, CHATGPT_HEADERS
from chatgpt.dtos import ChatGPTConversationEntry


def get_chatgpt_response(system_prompt: str, prompt: str,
                         conversation_history: List[ChatGPTConversationEntry] = None) -> str:
    if conversation_history is None:
        conversation_history = []

    messages = [
        {'role': 'system', 'content': system_prompt},
    ]
    for entry in conversation_history:
        messages.append({'role': entry.role, 'content': entry.content})
    messages.append({'role': 'user', 'content': prompt})

    response = requests.post(
        url=CHATGPT_URL,
        headers=CHATGPT_HEADERS,
        json={
            'model': 'gpt-3.5-turbo',
            'messages': messages,
        }
    )
    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json['choices'][0]['message']['content']
        return generated_text.strip()
    else:
        return ''
