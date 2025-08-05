import google.generativeai as genai
from config import path_gemini_api_key
import json

# initialize
genai.configure(api_key=path_gemini_api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')

try:
    # promptのformatを読み込む
    with open('prompt_format.txt', 'r', encoding='utf-8') as f:
        prompt_format = f.read()
    
    with open('extract.json', encoding='utf-8') as f:
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