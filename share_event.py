import datetime
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ファイル名の定義
CONFIG_FILE = 'config.json'         # サービスアカウントの認証情報などの設定ファイル
MAP_FILE = 'calendar_map.json'      # ユーザーのメールアドレスとカレンダーIDの紐づけを保存するファイル
SAMPLE_FILE = 'sample.json'         # 予定情報（日時や内容など）を記録したJSONファイル

# 設定ファイルを読み込む関数
def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# カレンダーIDマップを読み込む関数（存在しない場合は空の辞書を返す）
def load_calendar_map():
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# カレンダーIDマップを保存する関数
def save_calendar_map(data):
    with open(MAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Google Calendar APIのサービスを初期化する関数
def init_calendar_service(credentials_path):
    SCOPES = ['https://www.googleapis.com/auth/calendar']  # 必要な権限（スコープ）
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)  # サービスオブジェクトを返す

# ユーザー用のカレンダーを取得 or 新規作成し、IDを返す関数
def get_or_create_calendar(service, user_email, calendar_map):
    # すでに存在する場合はそのIDを返す
    if user_email in calendar_map:
        return calendar_map[user_email]

    # 新しいカレンダーを作成
    calendar_body = {
        'summary': f'{user_email} の予定',
        'timeZone': 'Asia/Tokyo',
        'description': '自動作成された個人カレンダー'
    }
    calendar = service.calendars().insert(body=calendar_body).execute()
    calendar_id = calendar['id']
    print(f"✅ カレンダー作成: {user_email} (ID: {calendar_id})")

    # そのユーザーに共有（編集権限付き）でアクセスを許可
    acl_rule = {
        'scope': {
            'type': 'user',
            'value': user_email
        },
        'role': 'writer'
    }
    service.acl().insert(calendarId=calendar_id, body=acl_rule).execute()
    print(f"✅ 共有設定追加: {user_email}")

    # 作成したカレンダーIDを保存
    calendar_map[user_email] = calendar_id
    save_calendar_map(calendar_map)

    return calendar_id

# メイン関数：特定ユーザーのカレンダーに予定を追加
def share_event_to_user(user_email):
    config = load_config()  # 設定読み込み
    credentials_path = config['credentials_path']
    service = init_calendar_service(credentials_path)  # 認証とサービス初期化
    calendar_map = load_calendar_map()  # カレンダーマップを読み込み

    # 予定情報の読み込み（sample.json）
    with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    date_str = json_data["date"]  # 例: "2025-08-06"
    start_time_str = json_data["start_time"]  # 例: "14:30"
    end_time_str = json_data["end_time"]  # "None" または "15:30"
    summary = json_data["summary"]  # イベントのタイトル

    # カレンダーIDを取得または作成
    calendar_id = get_or_create_calendar(service, user_email, calendar_map)

    # 開始と終了の日時を構築（終了時間が None の場合は1時間後とする）
    start_dt = datetime.datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
    end_dt = (
        start_dt + datetime.timedelta(hours=1)
        if end_time_str == "None"
        else datetime.datetime.strptime(f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M")
    )

    # イベントデータを作成
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Asia/Tokyo',
        # },
        # 'reminders': {
        #     'useDefault': False,
        #     'overrides': [
        #         {'method': 'popup', 'minutes': 1},
        #         {'method': 'email', "minutes": 1}
        #     ]
        }
    }

    # イベントをユーザーのカレンダーに登録
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"✅ イベント登録完了: {user_email} → {created_event.get('htmlLink')}")
