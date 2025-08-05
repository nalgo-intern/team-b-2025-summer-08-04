from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

#.envファイルから環境変数を読み込む
load_dotenv()

# BOTトークンとAPPトークンの取得
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

#json形式のメッセージを溜めるためのリスト
message_baffer = []

def chack_data(llm_data:dict):
    """LLMから受け取ったデータが条件を満たしているのか確認し
    満たしているときにslackに送るtxtを作成する関数"""
    
    date = llm_data["date"]
    start_time = llm_data["start_time"]
    end_time = llm_data["end_time"]
    summary = llm_data["summary"]
    send_txt = ""
    data_count = 0
    chack = True # LLMから送られてきたデータが正しいか判定する変数
    
    if date != None:
        data_count += 1
        send_txt += f"日時：{date}\n"
        
    if start_time != None:
        data_count += 1
        send_txt += f"開始時間：{start_time}\n"
    
    if end_time != None:
        send_txt += f"終了時間：{end_time}\n"
        
    if summary != None:
        data_count += 1
        send_txt += f"内容：{summary}\n"
    
    if data_count < 3:
        chack = False
        
    return chack, send_txt
        
        
    

# メッセージ受信イベント（プライベートチャンネル対応）
@app.event("message")
def handle_message_events(body, say, logger):
    event = body.get("event",{})

    #他BOTやシステムメッセージを無視
    if event.get("subtype"):
        return
    
    #ユーザーIDとメッセージ内容の取得
    user_id = event.get("user")
    text = event.get("text")
    
    #ユーザーIDとメッセージ内容の取得でランタイムエラーが起きた場合
    if not user_id or not text:
        return
    print(f"user:message  {user_id}:{text}")

    #ユーザーIDとメッセージ内容をjson形式に変換
    message_json = {
        "user": user_id,
        "text": text
    }

    #バッファに蓄積
    message_baffer.append(message_json)

    #バッファの長さを参照し、長さが10以上なら出力し、バッファリセット
    #このコードでは、say(text=f"メッセージ内容:{message_baffer}")　でslackのチャンネルにメッセージ内容を送信しているため、この部分をgeminiに送信するコードに変更してください。
    if len(message_baffer) >= 10:
        llm_data = llmからもらうdataの関数()
        chack, send_txt = chack_data(llm_data)
        if chack:
            say(text=send_txt)
        message_baffer.clear()
        
        
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("インスタンス生成完了")
    handler.start()
