import json, subprocess
cal = json.load(open('raw/calibration.json'))
ll = {x['final_id']: x for x in json.load(open('raw/longlist.json'))}
fs = json.load(open('raw/final_status.json'))
K = ['demand','gap','ai_distribution','ad_potential','feasibility','reliability','shared_engine']
rows = []
for i, (fid, c) in enumerate(sorted(cal.items(), key=lambda kv: (-kv[1]['cal'], -kv[1]['agent'])), 1):
    a = json.load(open(f'raw/audit_{fid}.json'))
    cells = []
    for k in K:
        orig = a['scores'][k]['score']; new = c['scores'][k]
        cells.append(f"**{new}**" if new != orig else str(new))
    name = fs.get(fid, {}).get('name') or ll[fid]['name_en']
    name = name if len(name) < 70 else name[:67] + '…'
    direct = 'tak' if c['direct'] else 'nie znaleziono'
    rows.append(f"| {i} | {fid} | {name} | " + ' | '.join(cells) + f" | {c['agent']:.2f} | **{c['cal']:.2f}** | {direct} | {c['status']} |")
TOP10 = ['RENO-02','RENO-03','RENO-04','HOME-02','LIFE-01','HOME-04','INS-03','CARE-01','AUTO-01','FIN-01']
subprocess.run(['python3', 'tools/build_cards.py', ','.join(TOP10)], check=True)
doc = open('top10_head.md').read() + '\n'.join(rows) + '\n' + open('top10_rankings.md').read() + open('raw/cards.md').read()
open('/home/user/trackal/research/top-10-products.md', 'w').write(doc)
print('written', len(doc))
