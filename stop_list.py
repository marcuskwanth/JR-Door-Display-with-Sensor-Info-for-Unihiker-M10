# Station database
jp_y, kana_y, en_y = 50, 50, 50

stations = [
    {
        "kanji": "東 京", "kanji_font": 25, 
        "kana": "とうきょう", "kana_font": 12, "kana_y": jp_y+8, 
        "en": "Tōkyō", "en_font": 18, "en_y": jp_y+4, 
        "jy": "01", "acy": "TYO"
    },
    {
        "kanji": "神 田", "kanji_font": 25,
        "kana": "かんだ", "kana_font": 20, "kana_y": jp_y+4, 
        "en": "Kanda", "en_font": 18, "en_y": jp_y+6, 
        "jy": "02"
    },
    {
        "kanji": "秋葉原", "kanji_font": 20, "kanji_y": jp_y+4, 
        "kana": "あきはばら", "kana_font": 12, "kana_y": jp_y+10, 
        "en": "Akihabara", "en_font": 15, "en_y": jp_y+8, 
        "jy": "03", "acy": "AKB"
    },
    {
        "kanji": "御徒町", "kanji_font": 20, "kanji_y": jp_y+4, 
        "kana": "おかちまち", "kana_font": 12, "kana_y": jp_y+10, 
        "en": "Okachimachi", "en_font": 10, "en_y": jp_y+12, 
        "jy": "04"
    },
    {
        "kanji": "上 野", "kanji_font": 25, 
        "kana": "うえの", "kana_font": 20, "kana_y": jp_y+4, 
        "en": "Ueno", "en_font": 20, "en_y": jp_y+4, 
        "jy": "05", "acy": "UEN"
    },
    {
        "kanji": "鶯 谷", "kanji_font": 25, 
        "kana": "うぐいすだに", "kana_font": 10, "kana_y": jp_y+10, 
        "en": "Uguisudani", "en_font": 13, "en_y": jp_y+8, 
        "jy": "06"
    },
    {
        "kanji": "日暮里", "kanji_font": 20, "kanji_y": jp_y+4, 
        "kana": "にっぽり", "kana_font": 16, "kana_y": jp_y+6, 
        "en": "Nippori", "en_font": 18, "en_y": jp_y+4, 
        "jy": "07", "acy": "NPR"
    },
    {
        "kanji": "西日暮里", "kanji_font": 16, "kanji_y": jp_y+6, 
        "kana": "にしにっぽり", "kana_font": 12, "kana_y": jp_y+10, 
        "en": "Nishi-Nippori", "en_font": 11, "en_y": jp_y+8, 
        "jy": "08"
    },
    {
        "kanji": "田 端", "kanji_font": 25, 
        "kana": "たばた", "kana_font": 20, "kana_y": jp_y+4, 
        "en": "Tabata", "en_font": 18, "en_y": jp_y+4, 
        "jy": "09"
    },
    {
        "kanji": "駒 込", "kanji_font": 25, 
        "kana": "こまごめ", "kana_font": 18, "kana_y": jp_y+4, 
        "en": "Komagome", "en_font": 13, "en_y": jp_y+8, 
        "jy": "10"
    },
    {
        "kanji": "巣 鴨", "kanji_font": 25, 
        "kana": "すがも", "kana_font": 20,"kana_y": jp_y+4, 
        "en": "Sugamo", "en_font": 17, "en_y": jp_y+6, 
        "jy": "11"
    },
    {
        "kanji": "大 塚", "kanji_font": 25, 
        "kana": "おおつか", "kana_font": 17, "kana_y": jp_y+4, 
        "en": "Ōtsuka", "en_font": 18, "en_y": jp_y+4, 
        "jy": "12"
    },
    {
        "kanji": "池 袋", "kanji_font": 25, 
        "kana": "いけぶくろ", "kana_font": 14, "kana_y": jp_y+8, 
        "en": "Ikebukuro", "en_font": 15, "en_y": jp_y+8, 
        "jy": "13", "acy": "IKB"
    },
    {
        "kanji": "目 白", "kanji_font": 25, 
        "kana": "めじろ", "kana_font": 20,"kana_y": jp_y+4, 
        "en": "Mejiro", "en_font": 18, "en_y": jp_y+4, 
        "jy": "14"
    },
    {
        "kanji": "高田馬場", "kanji_font": 16, "kanji_y": jp_y+6, 
        "kana": "たかだのばば", "kana_font": 11, "kana_y": jp_y+10, 
        "en": "Takadanobaba", "en_font": 10, "en_y": jp_y+10, 
        "jy": "15"
    },
    {
        "kanji": "新大久保", "kanji_font": 16, "kanji_y": jp_y+6, 
        "kana": "しんおおくぼ", "kana_font": 10, "kana_y": jp_y+10, 
        "en": "Shin-Ōkubo", "en_font": 12, "en_y": jp_y+10, 
        "jy": "16"
    },
    {
        "kanji": "新 宿", "kanji_font": 25, 
        "kana": "しんじゅく", "kana_font": 12, "kana_y": jp_y+10, 
        "en": "Shinjuku", "en_font": 17, "en_y": jp_y+4, 
        "jy": "17", "acy": "SJK"
    },
    {
        "kanji": "代々木", "kanji_font": 22, "kanji_y": jp_y+4, 
        "kana": "よよぎ", "kana_font": 20,"kana_y": jp_y+4, 
        "en": "Yoyogi", "en_font": 18, "en_y": jp_y+4, 
        "jy": "18"
    },
    {
        "kanji": "原 宿", "kanji_font": 25, 
        "kana": "はらじゅく", "kana_font": 15, "kana_y": jp_y+6, 
        "en": "Harajuku", "en_font": 16, "en_y": jp_y+6, 
        "jy": "19"
    },
    {
        "kanji": "渋 谷", "kanji_font": 25, 
        "kana": "しぶや", "kana_font": 20, "kana_y": jp_y+4, 
        "en": "Shibuya", "en_font": 18, "en_y": jp_y+4, 
        "jy": "20", "acy": "SBY"
    },
    {
        "kanji": "恵比寿", "kanji_font": 22, "kanji_y": jp_y+4, 
        "kana": "えびす", "kana_font": 20,"kana_y": jp_y+4, 
        "en": "Ebisu", "en_font": 20, "en_y": jp_y+4, 
        "jy": "21", "acy": "EBS"
    },
    {
        "kanji": "目 黒", "kanji_font": 25, 
        "kana": "めぐろ", "kana_font": 20,"kana_y": jp_y+4, 
        "en": "Meguro", "en_font": 18, "en_y": jp_y+4, 
        "jy": "22"
    },
    {
        "kanji": "五反田", "kanji_font": 22, "kanji_y": jp_y+4, 
        "kana": "ごたんだ", "kana_font": 17, "kana_y": jp_y+6, 
        "en": "Gotanda", "en_font": 17, "en_y": jp_y+4, 
        "jy": "23"
    },
    {
        "kanji": "大 崎", "kanji_font": 25,
        "kana": "おおさき", "kana_font": 17, "kana_y": jp_y+6, 
        "en": "Ōsaki", "en_font": 20, "en_y": jp_y+4, 
        "jy": "24", "acy": "OSK"
    },
    { 
        "kanji": "品 川", "kanji_font": 25, 
        "kana": "しながわ", "kana_font": 14, "kana_y": jp_y+8, 
        "en": "Shinagawa", "en_font": 13, "en_y": jp_y+8, 
        "jy": "25", "acy": "SGW"
    },
    {
        "kanji": "高輪ゲトウェイ", "kanji_font": 10, "kanji_y": jp_y+12,
        "kana": "たかなわゲートウェイ", "kana_font": 7, "kana_y": jp_y+12, 
        "en": "TakanawaGateway", "en_font": 8, "en_y": jp_y+12,
        "jy": "26", "acy": "TGW"
    },
    {
        "kanji": "田 町", "kanji_font": 25, 
        "kana": "たまち", "kana_font": 20, "kana_y": jp_y+4, 
        "en": "Tamachi", "en_font": 15, "en_y": jp_y+8, 
        "jy": "27"
    },
    {
        "kanji": "浜松町", "kanji_font": 20, "kanji_y": jp_y+4, 
        "kana": "はままつちょう", "kana_font": 10, "kana_y": jp_y+12, 
        "en": "Hamamatsuchō", "en_font": 9, "en_y": jp_y+12, 
        "jy": "28", "acy": "HMC"
    },
    {
        "kanji": "新 橋", "kanji_font": 25, 
        "kana": "しんばし", "kana_font": 18, "kana_y": jp_y+4, 
        "en": "Shimbashi", "en_font": 14, "en_y": jp_y+8, 
        "jy": "29", "acy": "SMB"
    },
    {
        "kanji": "有楽町", "kanji_font": 20, "kanji_y": jp_y+4, 
        "kana": "ゆうらくちょう", "kana_font": 10, "kana_y": jp_y+12, 
        "en": "Yūrakuchō", "en_font": 14, "en_y": jp_y+8, 
        "jy": "30"
        },
]