import json, glob
ideas = []
for f in sorted(glob.glob('raw/family_*.json')) + sorted(glob.glob('raw/seed_*.json')) + sorted(glob.glob('raw/topup_T-S*.json')):
    d = json.load(open(f))
    for i in d.get('ideas', []) + d.get('replacement_ideas', []):
        i['_src'] = f.split('/')[-1][:-5]
        ideas.append(i)
json.dump(ideas, open('raw/all_ideas.json', 'w'), ensure_ascii=False, indent=1)
print(len(ideas))
for i in ideas:
    if i['_src'].startswith('family'): continue
    print(i['temp_id'], '|', i['name_en'][:90], '|', i['status'])
