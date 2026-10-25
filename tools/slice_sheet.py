"""表情シート（4列×3行の1枚絵）を12枚に切り分けて assets/chara/<表情>.png にする。
使い方: python3 tools/slice_sheet.py シート.png   （macOS の sips を使う。Pillow 不要）
順番（左上→右へ、上の段から）: welcome happy cheer oops / sad hint explain think / write read sleep surprise
そのあと python3 tools/build_site.py → git commit → push で公開に反映。"""
import sys, os, subprocess
ORDER = ['welcome','happy','cheer','oops','sad','hint','explain','think','write','read','sleep','surprise']
src = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'assets', 'chara'); os.makedirs(out, exist_ok=True)
info = subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',src], capture_output=True, text=True).stdout
W = int([l for l in info.splitlines() if 'pixelWidth' in l][0].split()[-1])
H = int([l for l in info.splitlines() if 'pixelHeight' in l][0].split()[-1])
cw, ch = W//4, H//3
for i, name in enumerate(ORDER):
    r, c = divmod(i, 4); dst = os.path.join(out, name+'.png')
    subprocess.run(['cp', src, dst], check=True)
    # 下の段のキャラの頭が入り込まないよう、マスの下 12% を切り落とす
    subprocess.run(['sips','-c',str(int(ch*0.88)),str(cw),'--cropOffset',str(r*ch),str(c*cw),dst,'--out',dst], capture_output=True)
    subprocess.run(['sips','-Z','400',dst,'--out',dst], capture_output=True)
print('sliced 12 images ->', out)
