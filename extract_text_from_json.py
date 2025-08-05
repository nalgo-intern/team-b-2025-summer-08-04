import json
from config import path_slack_history

with open(f'{path_slack_history}', encoding='utf-8') as f:
    data = json.load(f)

results = []
for msg in data.get('messages', []):
    user = msg.get('user')
    text = msg.get('text')
    if user and text:
        results.append({'user': user, 'text': text})

# オブジェクトごとに改行
json_string = json.dumps(results, ensure_ascii=False).replace('}, {', '},\n{')

with open('extract.json', 'w', encoding='utf-8') as f:
    f.write(json_string)