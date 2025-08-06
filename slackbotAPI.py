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
    data_chack = [0, 0, 0] # どのデータがあるかを確認するためのlist(dateがある場合:data_chack[0]=1, start_timeがある場合:data_chack[1]=1, summaryがある場合:data_chack[2]=1)
    chack = True # LLMから送られてきたデータが正しいか判定する変数
    
    if date != "None":
        data_chack[0] = 1
        send_txt += f"日程：{date}\n"
    if start_time != "None":
        data_chack[1] = 1
        send_txt += f"開始時間：{start_time}\n"
    if end_time != "None":
        send_txt += f"終了時間：{end_time}\n"
    if summary != "None":
        data_chack[2] = 1
        send_txt += f"予定内容：{summary}\n"
        send_txt += f"これでよろしければスタンプを押してください"
        
    if sum(data_chack) == 2:
        if not data_chack[0]:
            send_txt = f"「日程」の情報を追加してください"
        elif not data_chack[1]:
            send_txt = f"「開始時間」の情報を追加してください"
        else:
            send_txt = f"「予定内容」の情報を追加してください"

    if sum(data_chack) < 2:
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
    if len(message_baffer) >= 4:
        # llm_data = llmからもらうdataの関数()
        # llm_data = {"date": "2024-07-20", "start_time": "15:00", "end_time": "None","summary": "会議"}
        llm_data = {"date": "None", "start_time": "15:00", "end_time": "None","summary": "会議"}
        # llm_data = {"date": "2024-07-20", "start_time": "None", "end_time": "None","summary": "会議"}
        # llm_data = {"date": "2024-07-20", "start_time": "15:00", "end_time": "None","summary": "None"}
        # llm_data = {"date": "None", "start_time": "None", "end_time": "None","summary": "None"}
        chack, send_txt = chack_data(llm_data)
        if chack:
            say(text=send_txt)
        message_baffer.clear()
        
        
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("インスタンス生成完了")
    handler.start()
