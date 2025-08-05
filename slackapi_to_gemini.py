import json
from config import path_slack_history,path_extract_messages,path_gemini_api_key,path_prompt_format
import google.generativeai as genai

# slackapiからのJSONファイルを読み込み、ユーザーIDとテキストを抽出
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


# extract.jsonの内容を読み込む
with open(f'{path_extract_messages}', encoding='utf-8') as f:
    data = json.load(f)

print(data)  # 内容を表示

"""
# extract.jsonの内容を空リストで上書きして削除
with open('extract.json', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False, indent=2)
"""

# geminiの初期設定
genai.configure(api_key=path_gemini_api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')

try:
    # geminiに投げるプロンプトのフォーマットを読み込む
    with open(f'{path_prompt_format}', 'r', encoding='utf-8') as f:
        prompt_format = f.read()
    
    with open(f'{path_extract_messages}', encoding='utf-8') as f:
        prompt_messages = json.load(f)

    # Geminiにプロンプトを送信して応答を生成
    response = model.generate_content(
        f"{prompt_format}\n"+  
        f"{prompt_messages}"
        )

    # 応答のテキスト部分を表示
    print(response.text)

    # 応答をgemini_responce.jsonに保存
    with open('gemini_responce.json', 'w', encoding='utf-8') as f:
        f.write(response.text)

except FileNotFoundError:
    print("エラー: ファイルが見つかりません。")
except Exception as e:
    print(f"API呼び出し中にエラーが発生しました: {e}")