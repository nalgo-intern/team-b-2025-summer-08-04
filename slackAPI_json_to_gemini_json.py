import json

# extract.jsonの内容を読み込む
with open('extract.json', encoding='utf-8') as f:
    data = json.load(f)

print(data)  # 内容を表示

"""
# extract.jsonの内容を空リストで上書きして削除
with open('extract.json', 'w', encoding='utf-8') as f:
    json.dump([], f, ensure_ascii=False, indent=2)
"""