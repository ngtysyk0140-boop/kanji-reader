import xml.etree.ElementTree as ET, re, json, os
SRC = os.path.join(os.path.dirname(__file__), 'src')
OUT = '/Users/nagatayoshiyuki/Desktop/kanji-reader/data'

# 学年配当（v1 の DB: Wikipedia 学年別漢字配当表 2020年版）
s = open(os.path.join(OUT, 'kanji_db.js'), encoding='utf-8').read()
V1 = json.loads(re.search(r'window.KANJI_DB = (\{.*\});', s).group(1))
JOYO = set(V1.keys())
print('joyo', len(JOYO))

# ---- 部首 214 ----
RAD = """1 一 いち
2 丨 ぼう・たてぼう
3 丶 てん
4 丿 の・はらいぼう
5 乙 おつ・おつにょう
6 亅 はねぼう
7 二 に
8 亠 なべぶた・けいさんかんむり
9 人 ひと・にんべん・ひとやね
10 儿 ひとあし・にんにょう
11 入 いる・いりがしら
12 八 はち・はちがしら
13 冂 けいがまえ・どうがまえ
14 冖 わかんむり
15 冫 にすい
16 几 つくえ・きにょう
17 凵 かんにょう・うけばこ
18 刀 かたな・りっとう
19 力 ちから
20 勹 つつみがまえ
21 匕 さじのひ・ひ
22 匚 はこがまえ
23 匸 かくしがまえ
24 十 じゅう
25 卜 ぼくのと・うらない
26 卩 ふしづくり・わりふ
27 厂 がんだれ
28 厶 む
29 又 また
30 口 くち・くちへん
31 囗 くにがまえ
32 土 つち・つちへん
33 士 さむらい
34 夂 ふゆがしら
35 夊 すいにょう
36 夕 ゆうべ・た
37 大 だい
38 女 おんな・おんなへん
39 子 こ・こへん
40 宀 うかんむり
41 寸 すん
42 小 しょう
43 尢 だいのまげあし
44 尸 しかばね・かばね
45 屮 てつ
46 山 やま・やまへん
47 巛 かわ
48 工 たくみ・たくみへん
49 己 おのれ
50 巾 はば・はばへん
51 干 かん・いちじゅう
52 幺 いとがしら
53 广 まだれ
54 廴 えんにょう
55 廾 にじゅうあし
56 弋 しきがまえ・よく
57 弓 ゆみ・ゆみへん
58 彐 けいがしら
59 彡 さんづくり
60 彳 ぎょうにんべん
61 心 こころ・りっしんべん・したごころ
62 戈 ほこ・ほこがまえ
63 戸 と・とだれ
64 手 て・てへん
65 支 しにょう・えだにょう
66 攴 ぼくづくり・のぶん
67 文 ぶん
68 斗 とます・と
69 斤 おの・おのづくり
70 方 ほう・かたへん
71 无 なし・すでのつくり
72 日 ひ・ひへん・にち
73 曰 ひらび・いわく
74 月 つき・つきへん
75 木 き・きへん
76 欠 あくび・かける
77 止 とめる・とめへん
78 歹 がつへん・かばねへん
79 殳 るまた・ほこづくり
80 毋 なかれ・はは
81 比 くらべる・ならびひ
82 毛 け
83 氏 うじ
84 气 きがまえ
85 水 みず・さんずい・したみず
86 火 ひ・ひへん・れっか・れんが
87 爪 つめ・つめかんむり・つめがしら
88 父 ちち
89 爻 こう・めめ
90 爿 しょうへん
91 片 かた・かたへん
92 牙 きば
93 牛 うし・うしへん
94 犬 いぬ・けものへん
95 玄 げん
96 玉 たま・たまへん・おうへん
97 瓜 うり
98 瓦 かわら
99 甘 あまい・かん
100 生 うまれる
101 用 もちいる
102 田 た・たへん
103 疋 ひき・ひきへん
104 疒 やまいだれ
105 癶 はつがしら
106 白 しろ
107 皮 けがわ・ひのかわ
108 皿 さら
109 目 め・めへん
110 矛 ほこ・ほこへん
111 矢 や・やへん
112 石 いし・いしへん
113 示 しめす・しめすへん
114 禸 ぐうのあし
115 禾 のぎ・のぎへん
116 穴 あな・あなかんむり
117 立 たつ・たつへん
118 竹 たけ・たけかんむり
119 米 こめ・こめへん
120 糸 いと・いとへん
121 缶 ほとぎ
122 网 あみがしら・よこめ・あみめ
123 羊 ひつじ
124 羽 はね
125 老 おい・おいかんむり
126 而 しこうして
127 耒 らいすき・すきへん
128 耳 みみ・みみへん
129 聿 ふでづくり
130 肉 にく・にくづき
131 臣 しん
132 自 みずから
133 至 いたる・いたるへん
134 臼 うす
135 舌 した
136 舛 まいあし
137 舟 ふね・ふねへん
138 艮 こん・ねづくり
139 色 いろ
140 艸 くさ・くさかんむり
141 虍 とらがしら・とらかんむり
142 虫 むし・むしへん
143 血 ち
144 行 ぎょう・ぎょうがまえ
145 衣 ころも・ころもへん
146 襾 にし・おおいかんむり
147 見 みる
148 角 つの・つのへん
149 言 げん・ごんべん
150 谷 たに
151 豆 まめ
152 豕 ぶた・いのこ
153 豸 むじなへん
154 貝 かい・かいへん
155 赤 あか
156 走 はしる・そうにょう
157 足 あし・あしへん
158 身 み・みへん
159 車 くるま・くるまへん
160 辛 からい
161 辰 しんのたつ
162 辶 しんにょう・しんにゅう
163 邑 むら・おおざと
164 酉 とり・とりへん・ひよみのとり
165 釆 のごめ・のごめへん
166 里 さと・さとへん
167 金 かね・かねへん
168 長 ながい
169 門 もん・もんがまえ
170 阜 おか・こざとへん
171 隶 れいづくり
172 隹 ふるとり
173 雨 あめ・あめかんむり
174 青 あお
175 非 あらず
176 面 めん
177 革 かわ・かくのかわ・つくりがわ
178 韋 なめしがわ
179 韭 にら
180 音 おと
181 頁 おおがい
182 風 かぜ
183 飛 とぶ
184 食 しょく・しょくへん
185 首 くび
186 香 かおり
187 馬 うま・うまへん
188 骨 ほね・ほねへん
189 高 たかい
190 髟 かみがしら
191 鬥 とうがまえ
192 鬯 ちょう
193 鬲 かなえ
194 鬼 おに・きにょう
195 魚 うお・うおへん
196 鳥 とり
197 鹵 しお
198 鹿 しか
199 麦 むぎ・ばくにょう
200 麻 あさ・あさかんむり
201 黄 き
202 黍 きび
203 黒 くろ
204 黹 ふつ
205 黽 べんあし
206 鼎 かなえ
207 鼓 つづみ
208 鼠 ねずみ
209 鼻 はな
210 斉 せい
211 歯 は
212 竜 りゅう
213 亀 かめ
214 龠 やく"""
RADICALS = {}
for line in RAD.split('\n'):
    n, ch, names = line.split(' ')
    RADICALS[int(n)] = [ch, names]
assert len(RADICALS) == 214

# ---- KANJIDIC2 ----
K = {}
root = ET.parse(os.path.join(SRC, 'kanjidic2.xml')).getroot()
for c in root.iter('character'):
    lit = c.find('literal').text
    if lit not in JOYO: continue
    rad = None
    for rv in c.iter('rad_value'):
        if rv.get('rad_type') == 'classical': rad = int(rv.text)
    misc = c.find('misc')
    sc = int(misc.find('stroke_count').text)
    freq = misc.find('freq'); freq = int(freq.text) if freq is not None else None
    on, kun = [], []
    rm = c.find('reading_meaning')
    if rm is not None:
        for r in rm.iter('reading'):
            if r.get('r_type') == 'ja_on': on.append(r.text)
            elif r.get('r_type') == 'ja_kun': kun.append(r.text)
    K[lit] = {'g': V1[lit]['g'], 'on': on, 'kun': kun, 's': sc, 'rad': rad, 'f': freq}
missing = JOYO - set(K)
print('kanjidic missing', missing)
# 𠮟 等が無ければ v1 から補う
for k in missing:
    K[k] = {'g': V1[k]['g'], 'on': [], 'kun': [], 's': V1[k]['s'], 'rad': None, 'f': None}

# 常用漢字表の音訓（v1: Wikipedia）を正本にし、KANJIDIC2 は補助。表外読みを除くため v1 の読みを採用。
def split_v1(r):
    on, kun = [], []
    for part in r.split('、'):
        part = part.strip()
        if not part: continue
        special = part.startswith('（') and part.endswith('）')
        core = part.strip('（）')
        if re.fullmatch(r'[ァ-ヶー]+', core): on.append(core)
        else: kun.append(core)  # 'おお-きい' 形式（-以降が送り仮名）
    return on, kun
for k in K:
    on, kun = split_v1(V1[k]['r'])
    K[k]['on'] = on; K[k]['kun'] = kun

# ---- KanjiVG ----
S = {}
root = ET.parse(os.path.join(SRC, 'kanjivg.xml')).getroot()
NS = '{http://kanjivg.tagaini.net}'
for kj in root.iter('kanji'):
    kid = kj.get('id')  # kvg:kanji_05b66
    if '-' in kid: continue  # 変体は除く
    cp = int(kid.split('_')[1], 16)
    ch = chr(cp)
    if ch not in JOYO: continue
    paths = [p.get('d') for p in kj.iter('path')]
    S[ch] = paths
print('kanjivg', len(S), 'missing', [k for k in JOYO if k not in S][:20])
for k in S: K[k]['s'] = len(S[k])  # 常用漢字表の字体に合わせ KanjiVG の画数を採用
# 画数の整合性チェック
bad = [(k, K[k]['s'], len(S[k])) for k in S if K[k]['s'] != len(S[k])]
print('stroke mismatch', len(bad), bad[:10])

with open(os.path.join(OUT, 'kanji.js'), 'w', encoding='utf-8') as f:
    f.write('// 常用漢字 2136字。g:学年(1-6=小, 7=中学) on:音読み kun:訓読み(「-」以降は送り仮名) s:総画数 rad:部首番号(康熙214) f:使用頻度順位\n')
    f.write('// 出典: 文部科学省 学年別漢字配当表 / 文化庁 常用漢字表 (Wikipedia経由), KANJIDIC2 (EDRDG, CC BY-SA 4.0)\n')
    f.write('window.KANJI = ' + json.dumps(K, ensure_ascii=False, separators=(',', ':')) + ';\n')
    f.write('window.RADICALS = ' + json.dumps(RADICALS, ensure_ascii=False, separators=(',', ':')) + ';\n')
with open(os.path.join(OUT, 'strokes.js'), 'w', encoding='utf-8') as f:
    f.write('// 書き順データ: KanjiVG (Ulrich Apel, CC BY-SA 3.0) https://kanjivg.tagaini.net/ 109x109 座標\n')
    f.write('window.STROKES = ' + json.dumps(S, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('sizes', os.path.getsize(os.path.join(OUT, 'kanji.js')), os.path.getsize(os.path.join(OUT, 'strokes.js')))
