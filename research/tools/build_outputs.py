"""Build research/product-opportunities.csv and research/competitor-audit.csv from agent outputs."""
import csv, glob, json, os, re, sys
sys.path.insert(0, 'tools')
OUT = '/home/user/trackal/research'
W = {'demand': .20, 'gap': .20, 'ai_distribution': .15, 'ad_potential': .15, 'feasibility': .10, 'reliability': .10, 'shared_engine': .10}
LV = {'low': 'niska', 'medium': 'średnia', 'high': 'wysoka'}

ll = json.load(open('raw/longlist.json'))
final = json.load(open('raw/final_status.json')) if os.path.exists('raw/final_status.json') else {}
audits = {}
for f in glob.glob('raw/audit_*.json'):
    d = json.load(open(f)); audits[d['id']] = d

# temp-id -> final id (for register rows of wave 1)
temp2final = {}
for x in ll:
    for k in x['merged_from']:
        src, tid = k.split(':', 1)
        temp2final[(src, tid)] = x['final_id']
        temp2final.setdefault(('*', tid), x['final_id'])


def comp_str(cs):
    return '; '.join(f"{c['name']} [{ {'direct': 'bezpośredni', 'partial': 'częściowy', 'substitute': 'substytut'}[c['type']]}] {c.get('url', '')}" for c in cs)


rows = []
for x in ll:
    fid = x['final_id']
    a = audits.get(fid)
    fs = final.get(fid, {})
    status = fs.get('status') or (a['recommendation'] if a else x['status'])
    reason = fs.get('reason') or (a['recommendation_reason_pl'] if a else x['status_reason'])
    comps = x['nearest_competition']
    gap = x['gap']; solved = x['already_solved']
    level = x['verification_level']
    weighted = ''
    direct = ''
    if a:
        comps_a = [{'name': c['name'], 'type': c['type'], 'url': c['url']} for c in a['competitors']]
        comps = comps_a
        gap = a['gap_statement_pl']
        solved = '; '.join(f"{c['name']}: {c['covers_pl']}" for c in a['competitors'][:8])
        level = 'audyt konkurencji (fala 2, search-summary, 7 zapytań)'
        weighted = f"{sum(W[k] * a['scores'][k]['score'] for k in W):.2f}"
        direct = 'tak' if a['direct_competitor_found'] else 'nie znaleziono w badanym zakresie'
    rows.append({
        'ID': fid,
        'nazwa_robocza_en': fs.get('name') or x['name_en'],
        'rodzina': x['family_pl'],
        'uzytkownik_i_moment_potrzeby': x['user_and_moment'],
        'przykladowe_pytanie_do_LLM_en': x['sample_prompt_en'],
        'pelny_problem_decyzyjny': x['decision_problem'],
        'laczone_obszary': x['combined_domains'],
        'warianty_porownania': x['variants_compared'],
        'kluczowe_zaleznosci_miedzy_modulami': x['key_dependencies'],
        'glowne_wyniki': x['main_outputs'],
        'powod_wejscia_na_zewnetrzna_strone': x['reason_external_site'],
        'zrodla_danych': x['data_sources'],
        'dane_uzytkownika': x['user_data'],
        'najblizsza_konkurencja': comp_str(comps),
        'co_juz_rozwiazano': solved,
        'istotny_brak_w_istniejacych_produktach': gap,
        'trudnosc_implementacji': LV[x['impl_difficulty']],
        'obciazenie_utrzymaniem': LV[x['maintenance_burden']],
        'ryzyko_merytoryczne': LV[x['content_risk']],
        'ryzyko_ze_asystent_AI_rozwiaze_sam': LV[x['ai_self_solve_risk']],
        'dowody_popytu': x['demand_evidence'],
        'otoczenie_reklamowe': x['ad_environment'],
        'poziom_pewnosci': LV[x['confidence']],
        'status': status,
        'uzasadnienie_statusu': reason,
        'poziom_weryfikacji': level,
        'ocena_wazona_0_5 (tylko top 25)': weighted,
        'bezposredni_konkurent (tylko top 25)': direct,
        'scalone_z_pomyslow_agentow': ', '.join(x['merged_from']),
        'uwagi_scalenia': x['merge_note'],
    })
with open(f'{OUT}/product-opportunities.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('product rows', len(rows))

# competitor register
reg = []
NOQ = re.compile(r'^\W*brak|niewykonan|nie wykonano|wiedz[ay] modelu|not performed|budżet wyszukiwań|limit wyszukiwań|wyczerpan', re.I)
for f in sorted(glob.glob('raw/*.json')):
    d = json.load(open(f))
    if not isinstance(d, dict) or 'register' not in d:
        continue
    src = os.path.basename(f)[:-5]
    for r in d['register']:
        if src.startswith('audit_'):
            fid = d['id']; stage = 'fala 2: audyt top 25'
        else:
            tid = r.get('related_idea', '')
            fid = temp2final.get((src, tid)) or temp2final.get(('*', tid)) or tid
            stage = 'fala 1: rodziny/seedy'
        basis = 'wiedza modelu, bez wyszukiwania (niezweryfikowane)' if NOQ.search(r['query']) or NOQ.search(r['url'][:60]) or not r['url'].startswith('http') else 'search-summary (strona nieotwierana)'
        reg.append({
            'data': r['date'], 'etap': stage, 'agent_zrodlowy': src, 'produkt_ID': fid,
            'kwerenda': r['query'], 'URL': r['url'], 'konkurent': r['competitor'],
            'sprawdzone_funkcje': r['features_checked'], 'ograniczenia_dostepu': r['access_limits'],
            'wniosek': r['conclusion'], 'pewnosc': LV.get(r['confidence'], r['confidence']), 'podstawa_dowodu': basis,
        })
for f in sorted(glob.glob('raw/refute_*.json')):
    d = json.load(open(f))
    for cnd in d['candidates']:
        reg.append({
            'data': '2026-10-25', 'etap': 'fala 2b: próba obalenia (finaliści)', 'agent_zrodlowy': os.path.basename(f)[:-5], 'produkt_ID': d['id'],
            'kwerenda': 'jedno z 8 zapytań agenta obalającego: ' + ' | '.join(d['queries_run'][:8]),
            'URL': cnd['url'], 'konkurent': cnd['name'], 'sprawdzone_funkcje': cnd['evidence_pl'],
            'ograniczenia_dostepu': 'strona nieotwierana (WebFetch zablokowany), dowód: search-summary; do ręcznej weryfikacji: ' + cnd['what_to_check_manually_pl'],
            'wniosek': {'direct': 'bezpośredni', 'probably_direct_unverified': 'prawdopodobnie bezpośredni (niezweryfikowane)', 'partial': 'częściowy', 'substitute': 'substytut'}[cnd['classification']],
            'pewnosc': LV.get(d['confidence'], d['confidence']), 'podstawa_dowodu': 'search-summary (strona nieotwierana)',
        })
seen, out = set(), []
for r in reg:
    k = (r['produkt_ID'], r['konkurent'].lower()[:40], r['URL'][:80], r['kwerenda'][:60])
    if k in seen:
        continue
    seen.add(k); out.append(r)
ORDER = {'fala 2: audyt top 25': 0, 'fala 2b: próba obalenia (finaliści)': 1}
out.sort(key=lambda r: (ORDER.get(r['etap'], 2), r['produkt_ID'], r['konkurent']))
with open(f'{OUT}/competitor-audit.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('register rows', len(out), 'model-knowledge rows', sum(1 for r in out if r['podstawa_dowodu'].startswith('wiedza')))
