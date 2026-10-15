import xml.etree.ElementTree as ET, re, json, os, sys
from collections import defaultdict, Counter
SRC = os.path.join(os.path.dirname(__file__), 'src')
OUT = '/Users/nagatayoshiyuki/Desktop/kanji-reader/data'

s = open(os.path.join(OUT, 'kanji.js'), encoding='utf-8').read()
K = json.loads(re.search(r'window.KANJI = (\{.*?\});\n', s).group(1))
JOYO = set(K)
HAN = re.compile(r'[㐀-鿿\U00020000-\U0002ffff]')
KANA = re.compile(r'[ぁ-ゖァ-ヺーー]')

BLOCK_SUB = ['殺','淫','姦','娼','猥','痴','裸','麻薬','売春','性的','性交','恋','キス','不倫','離婚','煙草','たばこ','タバコ','ビール','ワイン','酔','爆弾','テロ','強盗','誘拐','死体','死ん','死に','自殺','暴力','銃','拳','妊娠','セックス','浮気','愛人','遺体','血まみれ','処刑','虐','拷問','奴隷','売女','くそ','バカ','馬鹿','ばか','阿呆','うんこ','おしっこ','便所','貧乏','乞食','浮浪','殴','刺殺','毒','呪','幽霊','地獄','悪魔','麻','喫煙','飲酒','酒','デブ','ブス','変態','気持ち悪','嫌い','憎','殴','泥棒','刑務所','監獄','警察に','逮捕','犯人','犯罪','暗殺','墓','葬','嫌','白人','黒人','人種','障害者','乞']
def blocked(t): return any(b in t for b in BLOCK_SUB)

def grade_of(text):
    g = 0
    for ch in text:
        if HAN.match(ch):
            if ch == '々': continue
            if ch not in JOYO: return 99
            g = max(g, K[ch]['g'])
    return g

# ---------- JMdict ----------
PRI = {'ichi1':4,'news1':3,'spec1':3,'gai1':1,'ichi2':2,'news2':1,'spec2':2,'gai2':0}
def pri_score(tags):
    sc = 0
    for t in tags:
        if t in PRI: sc = max(sc, PRI[t])
        m = re.match(r'nf(\d\d)', t)
        if m: sc = max(sc, 4 - int(m.group(1))//12)
    return sc
def pos_code(poslist):
    p = ' '.join(poslist)
    if 'Ichidan verb' in p or 'Godan verb' in p or 'suru verb' in p or 'Kuru verb' in p or 'irregular' in p and 'verb' in p: return 'v'
    if 'adjective (keiyoushi)' in p: return 'adj-i'
    if 'adjectival nouns' in p: return 'adj-na'
    if 'adverb' in p: return 'adv'
    if 'noun' in p: return 'n'
    return 'o'

WORDS = {}  # keb -> dict
ctx = ET.iterparse(os.path.join(SRC, 'JMdict_e'), events=('end',))
n = 0
for ev, el in ctx:
    if el.tag != 'entry': continue
    n += 1
    kels = el.findall('k_ele'); rels = el.findall('r_ele'); senses = el.findall('sense')
    if not kels: el.clear(); continue
    poslist = [p.text for p in senses[0].findall('pos')] if senses else []
    uk = all(any(m.text and 'usually written using kana' in m.text for m in sn.findall('misc')) for sn in senses) if senses else False
    for ke in kels:
        keb = ke.find('keb').text
        if ke.find('ke_inf') is not None: continue
        pri = [p.text for p in ke.findall('ke_pri')]
        if not pri: continue
        if not HAN.search(keb): continue
        if any(ch for ch in keb if not (HAN.match(ch) or KANA.match(ch) or ch in '々')): continue
        g = grade_of(keb)
        if g == 99 or g == 0: continue
        # reading
        reb = None
        for re_ in rels:
            if re_.find('re_nokanji') is not None: continue
            restr = [r.text for r in re_.findall('re_restr')]
            if restr and keb not in restr: continue
            reb = re_.find('reb').text; break
        if not reb: continue
        if blocked(keb): continue
        sc = pri_score(pri)
        if keb in WORDS and WORDS[keb]['p'] >= sc: continue
        WORDS[keb] = {'w': keb, 'r': reb, 'g': g, 'p': sc, 'pos': pos_code(poslist), 'uk': uk}
    el.clear()
print('entries', n, 'words', len(WORDS))

# ---------- Tatoeba ----------
TOK = re.compile(r'\[([^\]|]+)\|([^\]]*)\]')
def parse_trans(t):
    toks = []; last = 0; plain = ''
    for m in TOK.finditer(t):
        if m.start() > last:
            seg = t[last:m.start()]; toks.append(('s', seg)); plain += seg
        kan = m.group(1); rd = ''.join(m.group(2).split('|'))
        if not rd: toks.append(('s', kan)); plain += kan
        else: toks.append(('r', kan, rd)); plain += kan
        last = m.end()
    if last < len(t): seg = t[last:]; toks.append(('s', seg)); plain += seg
    return toks, plain

SENTS = defaultdict(list)  # word -> list of (score, markup, reading)
wordset = set(WORDS)
MAXKANA = 6
cnt = 0
with open(os.path.join(SRC, 'jpn_transcriptions.tsv'), encoding='utf-8') as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 5 or parts[2] != 'Hrkt': continue
        user, text = parts[3], parts[4]
        if '[' not in text: continue
        toks, plain = parse_trans(text)
        L = len(plain)
        if L < 6 or L > 42: continue
        if blocked(plain): continue
        if grade_of(plain) == 99: continue
        if re.search(r'[A-Za-z]', plain): continue
        base = (2 if user else 0) + (1 if L <= 24 else 0) - (1 if ('トム' in plain or 'メアリー' in plain) else 0)
        markup = ''.join(t[1] if t[0]=='s' else '{%s|%s}' % (t[1], t[2]) for t in toks)
        # candidate words at each ruby token
        for i, t in enumerate(toks):
            if t[0] != 'r': continue
            kan, rd = t[1], t[2]
            # join following consecutive ruby tokens (up to 3)
            j = i; ck, cr = kan, rd
            chains = [(ck, cr, j)]
            while j + 1 < len(toks) and toks[j+1][0] == 'r' and len(chains) < 3:
                j += 1; ck += toks[j][1]; cr += toks[j][2]; chains.append((ck, cr, j))
            for ck, cr, j in chains:
                tail = ''
                if j + 1 < len(toks) and toks[j+1][0] == 's': tail = toks[j+1][1]
                for k in range(0, min(MAXKANA, len(tail)) + 1):
                    cand = ck + tail[:k]
                    if k and not re.fullmatch(r'[ぁ-ゖ]+', tail[:k]): break
                    if cand in wordset:
                        reading = cr + tail[:k]
                        if reading != WORDS[cand]['r']: continue
                        # より長い語（例: 例え→例えば）が成立するならそちらを優先し、この候補は捨てる
                        if any((cand + tail[k:k+m]) in wordset for m in (1,2,3) if len(tail) >= k+m): continue
                        # 送り仮名が語の途中で切れないよう、次の文字がひらがな続きなら弱く減点
                        nxt = tail[k:k+1]
                        sc = base - (1 if re.match(r'[ぁ-ゖ]', nxt) and k == 0 and WORDS[cand]['pos'] in ('v','adj-i') else 0)
                        # 目印: 対象語を ⟪ ⟫ で囲む
                        tm = ''.join(('{%s|%s}' % (toks[x][1], toks[x][2])) for x in range(i, j+1))
                        before = ''.join(t2[1] if t2[0]=='s' else '{%s|%s}' % (t2[1], t2[2]) for t2 in toks[:i])
                        after_tail = tail[k:]
                        after = after_tail + ''.join(t2[1] if t2[0]=='s' else '{%s|%s}' % (t2[1], t2[2]) for t2 in toks[j+2:]) if tail else ''.join(t2[1] if t2[0]=='s' else '{%s|%s}' % (t2[1], t2[2]) for t2 in toks[j+1:])
                        mk = before + '⟪' + tm + tail[:k] + '⟫' + after
                        SENTS[cand].append((sc, mk, reading, grade_of(plain)))
        cnt += 1
print('sentences used', cnt, 'words with sentences', len(SENTS))

# ---------- 選別 ----------
# 各語: 例文は 最大3件。スコア順、文の学年が語の学年に近いものを優先
for w, lst in SENTS.items():
    g = WORDS[w]['g']
    lst.sort(key=lambda x: (-(x[0] - max(0, x[3]-g)*0.5), len(x[1])))
    seen = set(); keep = []
    for sc, mk, rd, sg in lst:
        if mk in seen: continue
        seen.add(mk); keep.append([mk, rd, sg])
        if len(keep) >= (2 if g <= 6 else 1): break
        if g <= 6 and len(mk) > 70: continue
    SENTS[w] = keep

# 語の採用: 優先度>=1 の語を基本に、各漢字について「最高学年がその漢字」の語を最低でも確保
by_kanji = defaultdict(list)
for w, d in WORDS.items():
    for ch in set(w):
        if ch in JOYO: by_kanji[ch].append(w)
chosen = set()
for ch in JOYO:
    g = K[ch]['g']
    cands = [w for w in by_kanji[ch] if WORDS[w]['g'] == g]
    cands.sort(key=lambda w: (-WORDS[w]['p'], -(1 if w in SENTS else 0), len(w)))
    chosen.update(cands[:8 if g <= 6 else 4])
    others = [w for w in by_kanji[ch] if w not in chosen and WORDS[w]['g'] <= 6]
    others.sort(key=lambda w: (-WORDS[w]['p'], -(1 if w in SENTS else 0), len(w)))
    chosen.update(others[:2])
chosen.update(w for w, d in WORDS.items() if d['p'] >= 3 and len(w) <= 3 and d['g'] <= 6 and w in SENTS)
print('chosen words', len(chosen))
cov = Counter()
for ch in JOYO:
    g = K[ch]['g']
    if any(WORDS[w]['g'] == g for w in by_kanji[ch] if w in chosen): cov[g] += 1
total = Counter(K[ch]['g'] for ch in JOYO)
print('kanji coverage by grade (kanji having a word where it is the top-grade char):', {g: f'{cov[g]}/{total[g]}' for g in sorted(total)})
nosent = [w for w in chosen if w not in SENTS]
print('chosen without sentence', len(nosent), nosent[:30])

out_words = []
for w in sorted(chosen, key=lambda w: (WORDS[w]['g'], -WORDS[w]['p'], w)):
    d = WORDS[w]
    o = {'w': w, 'r': d['r'], 'g': d['g'], 'p': d['p'], 'pos': d['pos']}
    if d['uk']: o['uk'] = 1
    out_words.append(o)
out_sents = {w: SENTS[w] for w in chosen if w in SENTS and (WORDS[w]['g'] <= 6 or WORDS[w]['p'] >= 2)}
with open(os.path.join(OUT, 'words.js'), 'w', encoding='utf-8') as f:
    f.write('// 熟語・単語: JMdict (EDRDG, CC BY-SA 4.0) の頻出語（優先度タグ付き）から、常用漢字のみで書ける語を抽出。g:最高学年 p:頻出度(0-4) pos:品詞 uk:ふつう仮名書き\n')
    f.write('window.WORDS = ' + json.dumps(out_words, ensure_ascii=False, separators=(',', ':')) + ';\n')
with open(os.path.join(OUT, 'sentences.js'), 'w', encoding='utf-8') as f:
    f.write('// 例文: Tatoeba (CC BY 2.0 FR) 日本語文とふりがな転写。{漢字|よみ} 記法、⟪⟫ が対象語。[markup, 文中の読み, 文の最高学年]\n')
    f.write('window.SENTS = ' + json.dumps(out_sents, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('sizes', os.path.getsize(os.path.join(OUT, 'words.js')), os.path.getsize(os.path.join(OUT, 'sentences.js')))
print(Counter(d['g'] for d in out_words))
