import json, sys
sys.path.insert(0, 'tools')
from longlist_map import MAP, FAM
ideas = {i['_src'] + ':' + i['temp_id']: i for i in json.load(open('raw/all_ideas.json'))}
used, out = set(), []
for fid, fam, pk, merged, st, note in MAP:
    for k in [pk] + merged:
        assert k in ideas, k
        assert k not in used, k
        used.add(k)
    base = dict(ideas[pk])
    comps = list(base['nearest_competition'])
    for k in merged:
        for c in ideas[k]['nearest_competition']:
            if c['name'] not in {x['name'] for x in comps}:
                comps.append(c)
    base['nearest_competition'] = comps
    base.update(final_id=fid, family_code=fam, family_pl=FAM[fam], merged_from=[pk] + merged, merge_note=note)
    if st: base['status'] = st; base['status_reason'] = note + ' ' + base['status_reason']
    out.append(base)
missing = [k for k in ideas if k not in used]
print('final', len(out), 'unused', missing)
json.dump(out, open('raw/longlist.json', 'w'), ensure_ascii=False, indent=1)
