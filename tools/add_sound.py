"""Suno などで作った音を整えてアプリに入れる。
使い方: python3 tools/add_sound.py <元ファイル> <名前> <アプリdir>   例: ... "foo.m4a" bgm_play ../kana-writer
BGM(bgm_*) は -20 LUFS、効果音(sfx_*) は -16 LUFS にそろえ、先頭末尾の無音を詰めて MP3 にする。"""
import sys, os, subprocess
src, name, app = sys.argv[1], sys.argv[2], sys.argv[3]
out = os.path.join(app, 'assets', 'sound', name + '.mp3'); os.makedirs(os.path.dirname(out), exist_ok=True)
is_bgm = name.startswith('bgm_')
trim = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse"
norm = "loudnorm=I=%s:TP=-1.5:LRA=11" % (-20 if is_bgm else -16)
CAP = {'sfx_tap':0.4,'sfx_stroke_ok':0.6,'sfx_stroke_ng':0.6,'sfx_correct':1.5,'sfx_wrong':1.5,'sfx_badge':2.5,'sfx_cheer':3.5,'sfx_end':4.0,'sfx_goal':6.0}
cap = CAP.get(name)
cut = ("atrim=0:%s,afade=t=out:st=%s:d=0.12," % (cap, cap-0.12)) if cap else ""
af = (norm if is_bgm else trim + "," + cut + norm)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-af', af, '-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '4', out], check=True)
dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', out], capture_output=True, text=True).stdout.strip()
print('->', out, float(dur), 'sec', os.path.getsize(out), 'bytes')
