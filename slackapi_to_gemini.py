import json
from config import path_extracted_data,path_gemini_api_key,path_prompt_format,path_gemini_response
import google.generativeai as genai
import datetime

#年を取得
today = datetime.date.today()
year = str(today.year)

# slackbotからのJSONファイルを読み込む
with open(f'{path_extracted_data}', encoding='utf-8') as f:
    extracted_data = json.load(f)

# オブジェクトごとに改行
translated_data = json.dumps(extracted_data, ensure_ascii=False).replace('}, {', '},\n{')

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

    prompt = (f'{prompt_format}\n' +  
              f'また、年に関する情報がない場合、年は{year}に設定してください。\n\n' +
              f'{translated_data}' )
    
    # Geminiにプロンプトを送信して応答を生成
    response = model.generate_content(prompt)
    #プロンプトの内容を表示
    print('\n\nprompt= \n' +  f'{prompt}')

    # 応答のテキスト部分を表示
    print('\n\nresponse= \n' +  f'{response.text}')

    # 応答をjsonに保存
    with open(f'{path_gemini_response}', 'w', encoding='utf-8') as f:
        f.write(response.text)

except FileNotFoundError:
    print("エラー: ファイルが見つかりません。")
except Exception as e:
    print(f"API呼び出し中にエラーが発生しました: {e}")


# jsonファイルの内容を空リストで上書きして削除
with open(f'{path_extracted_data}', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False)


with open(f'{path_gemini_response}', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False)
    