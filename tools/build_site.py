"""GitHub Pages 用の docs/ を index.html と data/ から組み立てる。
index.html は Artifact 用に DOCTYPE/html/head/body を持たない形なので、ここで完全な HTML に包み、
ホーム画面アプリ用の manifest / アイコン / 全画面設定を付ける。"""
import os, shutil, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
head = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<link rel="manifest" href="manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="漢検">
<meta name="theme-color" content="#fbf7ef">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)} [hidden]{display:none!important}</style>
</head>
<body>
"""
html = head + src + "\n</body>\n</html>\n"
os.makedirs(DOCS, exist_ok=True)
open(os.path.join(DOCS, 'index.html'), 'w', encoding='utf-8').write(html)
if os.path.isdir(os.path.join(DOCS, 'data')): shutil.rmtree(os.path.join(DOCS, 'data'))
shutil.copytree(os.path.join(ROOT, 'data'), os.path.join(DOCS, 'data'), ignore=shutil.ignore_patterns('kanji_db.js'))
json.dump({
  "name": "よんで かいて 漢検", "short_name": "漢検", "start_url": "./", "scope": "./", "display": "standalone",
  "background_color": "#fbf7ef", "theme_color": "#fbf7ef", "lang": "ja",
  "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]
}, open(os.path.join(DOCS, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ASSETS = os.path.join(ROOT, 'assets')
if os.path.isdir(ASSETS):
    for fn in os.listdir(ASSETS):
        if not fn.startswith('.') and fn != 'README.txt': shutil.copy(os.path.join(ASSETS, fn), os.path.join(DOCS, fn))
open(os.path.join(DOCS, '.nojekyll'), 'w').close()
print('built docs/', len(html))
