import json
from config import path_slack_history,path_translated_data,path_gemini_api_key,path_prompt_format,path_gemini_response
import google.generativeai as genai

# slackbotからのJSONファイルを読み込む
with open(f'{path_slack_history}', encoding='utf-8') as f:
    raw_data = json.load(f)

# オブジェクトごとに改行
translated_data = json.dumps(raw_data, ensure_ascii=False).replace('}, {', '},\n{')

# translated_dataをjsonファイルに保存
with open(f'{path_translated_data}', 'w', encoding='utf-8') as f:
    f.write(translated_data)

# 内容を表示
print('translated_data = ')
print(translated_data)


# geminiの初期設定
genai.configure(api_key=path_gemini_api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')

try:
    # geminiに投げるプロンプトのフォーマットを読み込む
    with open(f'{path_prompt_format}', 'r', encoding='utf-8') as f:
        prompt_format = f.read()
    
    with open(f'{path_translated_data}', encoding='utf-8') as f:
        prompt_messages = json.load(f)

    # Geminiにプロンプトを送信して応答を生成
    response = model.generate_content(
        f"{prompt_format}\n"+  
        f"{prompt_messages}"
        )

    # 応答のテキスト部分を表示
    print('\nresponse= ' +  f'{response.text}')

    # 応答をjsonに保存
    with open(f'{path_gemini_response}', 'w', encoding='utf-8') as f:
        f.write(response.text)

except FileNotFoundError:
    print("エラー: ファイルが見つかりません。")
except Exception as e:
    print(f"API呼び出し中にエラーが発生しました: {e}")


# jsonファイルの内容を空リストで上書きして削除
with open(f'{path_translated_data}', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False)

with open(f'{path_slack_history}', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False)

"""
with open(f'{path_gemini_response}', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False)
"""