import json

import requests


def send_message(message: str):
    payload = {
        'text': message,
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post('https://hooks.slack.com/services/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',
                        headers=headers, json=json.dumps(payload)
                        )
    if res.status_code != 200:
        print(f'failed to send message to slack. {res.status_code=}, {res.text=}')

