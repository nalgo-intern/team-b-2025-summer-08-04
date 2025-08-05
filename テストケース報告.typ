#import "@preview/showybox:2.0.4": showybox


#set page(
  paper: "a4",
  margin: (
    top: 25mm,
    bottom: 25mm,
    left: 30mm,
    right: 20mm
  ),
  number-align: center
)

#set text(
  //font: "Noto Sans Mono CJK JP",
  font: "Noto Sans JP",
  size: 11pt,
  tracking: 1pt,
  lang: "ja"
)

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1em
)

#set heading(numbering: "1.1")

#set page(numbering: "i")
#counter(page).update(1)

#show heading: it => {
  set text(size:16pt)
  it
}

= テストケース報告
== 最も単純なケース
#linebreak()
#figure(
  showybox()[ 
  [{"user": "U021JKQFJUC", "text": "じゃあ、7/20の15:00から1時間、会議を設定しますね。"},
  #linebreak()
  {"user": "U021JKQFJUD", "text": "わかりました！"}]
  ],
 caption: [応答],
) <case1_messages>
#linebreak()
#figure(
  showybox()[ 
  {"date": "2023-07-20", "start_time": "15:00", "end_time": "16:00","summary": "会議"}
  ],
 caption: [結果],
) <case1_result>

== 少し複雑なケース
#linebreak()
#figure(
  showybox()[ 
  {"user": "U021JKQFJUC", "text": "ミーティングの件、いつに設定しましょうか？"},
  #linebreak()
  {"user": "U021JKQFJUD", "text": "7/20はどうでしょうか？"},
  #linebreak()
  {"user": "U021JKQFJUC", "text": "その日で問題ないと思います！"},
  #linebreak()
  {"user": "U021JKQFJUD", "text": "承知しました。何時開始にしましょうか？"},
  #linebreak()
  {"user": "U021JKQFJUC", "text": "今日の15:00ごろからなら空いているので、それ以降ならいつでも問題ないです!"},
  #linebreak()
  {"user": "U021JKQFJUD", "text": "では、15:00から1時間、会議を設定しますね。"},
  #linebreak()
  {"user": "U021JKQFJUC", "text": "承知しました。"}
  #linebreak()
  ],
 caption: [応答],
) <case1_messages>
#linebreak()
#figure(
  showybox()[ 
  {"date": "2024-07-20", "start_time": "17:00", "end_time": "18:00","summary": "会議"}
  ],
 caption: [結果],
) <case1_result>