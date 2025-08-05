from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
# 環境変数または直接記載
SLACK_BOT_TOKEN = ""
SLACK_APP_TOKEN = ""
app = App(token=SLACK_BOT_TOKEN)
# メッセージ受信イベント（プライベートチャンネル対応）
@app.event("message")
def handle_message_events(body, say, logger):
    print("メッセージ読み取り関数実行開始")
    event = body.get("event", {})
    channel = event.get("channel")
    user = event.get("user")
    text = event.get("text")
    logs = {"user": user, "text": text}
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("インスタンス生成完了")
    handler.start()