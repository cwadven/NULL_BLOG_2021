import requests
from chatgpt.consts import CHATGPT_URL, CHATGPT_HEADERS


def get_chatgpt_response(prompt):
    response = requests.post(
        url=CHATGPT_URL,
        headers=CHATGPT_HEADERS,
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
        }
    )
    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json['choices'][0]['message']['content']
        return generated_text.strip()
    else:
        return
