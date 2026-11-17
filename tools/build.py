"""組出「行銷科技與數據分析｜AI倫理、資安與法規」網頁簡報。

來源：
  SRC = 金屬扣件智慧製造與AI生產優化實務班_網頁簡報.html（123 頁）
  MK  = mktech-ai-course 的 index.html（只取第 1 頁封面）
結果：封面（取自 MK）＋ SRC 第 24–56 頁，共 34 頁，寫到 ../index.html。

用法：python -I -X utf8 build.py <SRC> <MK>
"""
import re
import sys
from pathlib import Path

src_path, mk_path = Path(sys.argv[1]), Path(sys.argv[2])
out_path = Path(__file__).resolve().parent.parent / 'index.html'

src = src_path.read_text(encoding='utf-8')
mk = mk_path.read_text(encoding='utf-8')

SEC = re.compile(r'<section\b.*?</section>', re.S)
src_secs = SEC.findall(src)
mk_secs = SEC.findall(mk)
assert len(src_secs) == 123, len(src_secs)

FIRST, LAST = 24, 56  # 原簡報頁碼（1 起算，含頭尾）
body = src_secs[FIRST - 1:LAST]
assert len(body) == LAST - FIRST + 1

# 封面：MK 的 p2/r2、p3/r3 樣式和 SRC 的同名 class 不同，改用新 class 名稱
cover = mk_secs[0]
assert 'data-t="行銷科技與數據分析"' in cover
cover = (cover.replace('class="p2"', 'class="pc2"').replace('class="r2"', 'class="rc2"')
              .replace('class="p3"', 'class="pc3"').replace('class="r3"', 'class="rc3"'))
COVER_CSS = ('.pc2{--lh:32;--z:18.7;--m:0.27}'
             '.pc3{--lh:32;--z:18.7;--m:0.27;--sb:5.3}'
             '.rc2{--z:18.7;--m:0.27;color:#F5F2EC}'
             '.rc3{--z:18.7;--m:0.27;color:#F0A35E}\n')

start = src.find('<section')
end = src.rfind('</section>') + len('</section>')
head, tail = src[:start], src[end:]

# 分頁標題
head, n = re.subn(r'<title>[^<]*</title>',
                  '<title>行銷科技與數據分析｜AI倫理、資安與法規</title>', head, count=1)
assert n == 1
# 封面 class 樣式
i = head.rfind('</style>')
head = head[:i] + COVER_CSS + head[i:]

# localStorage 前綴：同一個 github.io 網域下避免和其他簡報互相覆蓋
tail_n = tail.count("'fastener-ai:'")
tail = tail.replace("'fastener-ai:'", "'mktech-ethics:'")
head = head.replace("'fastener-ai:'", "'mktech-ethics:'")

# 換頁時 JS 設定的分頁標題後綴
assert tail.count("'｜金屬扣件智慧製造與AI生產優化實務班'") == 1
tail = tail.replace("'｜金屬扣件智慧製造與AI生產優化實務班'", "'｜行銷科技與數據分析'")

html = head + cover + '\n' + '\n'.join(body) + tail
assert html.count('<section') == 34
out_path.write_text(html, encoding='utf-8')
print('pages', html.count('<section'), 'bytes', len(html.encode('utf-8')), 'ls-prefix replaced in tail', tail_n)
for k, s in enumerate([cover] + body, 1):
    t = re.search(r'data-t="([^"]*)"', s).group(1)
    print(k, t)
