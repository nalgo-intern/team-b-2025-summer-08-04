import datetime

today = datetime.date.today()
year = today.year
str_year = str(year)

print(f"Today's year: {str_year}")

#曜日を取得
w_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
d = datetime.date(year, today.month, today.day)
weekday = str(w_list[d.weekday()])
print(f"Today's weekday: {weekday}")