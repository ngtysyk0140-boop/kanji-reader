"""表情シート（4列×3行の1枚絵）を12枚に切り分けて assets/chara/<表情>.png にする。
使い方: python3 tools/slice_sheet.py シート.png   （ffmpeg を使う。sips は左上マスで位置指定を無視する不具合があったため置き換え）
順番（左上→右へ、上の段から）: welcome happy cheer oops / sad hint explain think / write read sleep surprise
そのあと python3 tools/build_site.py → git commit → push で公開に反映。"""
import sys, os, subprocess
ORDER = ['welcome','happy','cheer','oops','sad','hint','explain','think','write','read','sleep','surprise']
src = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'assets', 'chara'); os.makedirs(out, exist_ok=True)
probe = subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0', src], capture_output=True, text=True).stdout.strip()
W, H = [int(x) for x in probe.split(',')[:2]]
cw, ch = W//4, H//3
for i, name in enumerate(ORDER):
    r, c = divmod(i, 4); dst = os.path.join(out, name+'.png')
    # 下の段のキャラの頭が入り込まないよう、マスの下 12% を切り落とし、高さ 400px に縮小
    h = int(ch*0.88)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-vf','crop=%d:%d:%d:%d,scale=-1:400' % (cw, h, c*cw, r*ch), dst], check=True)
print('sliced 12 images ->', out)
