from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

#.envファイルから環境変数を読み込む
load_dotenv()

# BOTトークンとAPPトークンの取得
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

#slackアプリインスタンスの作成
app = App(token=SLACK_BOT_TOKEN)

#json形式のメッセージを溜めるためのリスト
message_baffer = []

#起動時にBotのユーザーIDを取得
bot_user_id = app.client.auth_test()["user_id"]

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
        say(text=f"メッセージ内容:{message_baffer}")
        message_baffer.clear()

#リアクションされたときの処理(リアクションユーザー判断、メールアドレス取得)
@app.event("reaction_added")
def handle_reaction(event,say,logger):
    user_id = event.get("user")               # リアクションをしたユーザー
    reaction = event.get("reaction")          # 使用されたリアクション
    item_user = event.get("item_user")        # リアクション対象メッセージの送信者
    
    print("reaction:",reaction)
    print("type:",type(reaction))
    #Botが送ったメッセージに対するリアクションかを確認
    if item_user == bot_user_id:
        if reaction in ["o","+1"]: #特定のリアクションのみ対象にする
            try:
                #ユーザー情報の取得
                user_info = app.client.users_info(user=user_id)
                email = user_info["user"]["profile"].get("email","(取得不可)")
                say(text=f"リアクションユーザーのメール: {email}")
            except Exception as e:
                say(text=f"❌ メール取得失敗: {e}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("インスタンス生成完了")
    handler.start()