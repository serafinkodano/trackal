import json
rows = json.load(open('raw/evidence_rows.json'))
head = open('evidence_head.md').read()
def cut(s, n):
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' …'
lines = []
for rid, claim, nums, typ, conf, src in rows:
    srcs = ' ; '.join(src.split('; '))
    lines.append(f"| {rid} | {cut(claim, 650)} | {cut(nums, 250)} | {typ} | {conf} | {srcs} |")
open('/home/user/trackal/research/evidence-and-assumptions.md', 'w').write(head + '\n'.join(lines) + '\n')
print(len(lines))
