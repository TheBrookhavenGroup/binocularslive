"""
curl --request POST --url http://localhost:8000/bye/ \
     --header "Authorization: Bearer 66cc3a57c348b6b4947bac1a05916a1dcec060c3" \
     --header 'Content-Type: application/json' \
     --data '{"text": "Is this real?"}'

You will have to change the bearer key above to an active one.
"""

import requests

key = "66cc3a57c348b6b4947bac1a05916a1dcec060c3"
header = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
data = {'text': 'Some very long text that may have been written by AI.'}

response = requests.post('http://localhost:8000/api/',
                         headers=header,
                         json=data)
print(response.content)
