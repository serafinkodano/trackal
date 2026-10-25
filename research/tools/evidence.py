import json
FILES = [('AI','foundation_F-AI'),('ADS','foundation_F-ADS'),('POR','foundation_F-PORT'),('POR2','topup_T-PORT'),
         ('CAP','foundation_F-CAP'),('CAP2','topup_T-CAP'),('REG','foundation_F-REG'),('REG2','topup_T-REG1'),
         ('REG3','topup_T-REG2'),('DEM','topup_T-FAM')]
ET = {'direct':'bezpośrednie','indirect':'pośrednie','estimate':'estymacja','hypothesis':'hipoteza'}
CF = {'high':'wysoka','medium':'średnia','low':'niska'}
rows = []
def clean(s): return ' '.join(str(s).replace('|','/').split())
for pre, f in FILES:
    d = json.load(open(f'raw/{f}.json'))
    for n, x in enumerate(d['findings'], 1):
        src = '; '.join(s['url'] for s in x['sources']) or '—'
        rows.append((f'E-{pre}-{n:02d}', clean(x['claim_pl']), clean(x.get('numbers','')), ET[x['evidence_type']], CF[x['confidence']], src))
for pre, f in [('VER','verify_AI'),('VER','verify_ADS')]:
    d = json.load(open(f'raw/{f}.json'))
    for c in d['claims']:
        src = '; '.join(s['url'] + (' (pierwotne)' if s['primary'] else '') for s in c['sources'])
        v = {'confirmed':'potwierdzone','partially':'częściowo','refuted':'obalone','unverifiable':'nieweryfikowalne'}[c['verdict']]
        rows.append((f'E-VER-{c["id"]}', clean(c['corrected_claim_pl']), '', f'weryfikacja: {v}', '—', src))
json.dump(rows, open('raw/evidence_rows.json','w'), ensure_ascii=False)
print(len(rows))
