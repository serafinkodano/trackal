"""Build research/product-opportunities.csv and research/competitor-audit.csv (wersja po recenzji fali 3).

Wejście (katalog roboczy = katalog z `raw/` = research/data/agent-outputs/ + wyniki skryptów):
  raw/longlist.json, raw/final_status.json, raw/calibration.json, raw/audit_*.json, raw/refute_*.json,
  raw/demand_*.json, raw/evidence_rows.json oraz pliki z polem `register` (fala 1).
"""
import csv, glob, json, os, re, sys
from urllib.parse import urlparse

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/trackal/research'
W = {'demand': .20, 'gap': .20, 'ai_distribution': .15, 'ad_potential': .15, 'feasibility': .10, 'reliability': .10, 'shared_engine': .10}
KPL = {'demand': 'popyt', 'gap': 'luka', 'ai_distribution': 'dystrybucja AI', 'ad_potential': 'reklama', 'feasibility': 'wykonalność',
       'reliability': 'wiarygodność', 'shared_engine': 'wspólny silnik'}
LV = {'low': 'niska', 'medium': 'średnia', 'high': 'wysoka'}
RANK = {'niska': 0, 'średnia': 1, 'wysoka': 2}
STATUS4 = ['pilot', 'zbadać', 'później', 'odrzucić']
TYPE = {'direct': 'bezpośredni', 'partial': 'częściowy', 'substitute': 'substytut',
        'probably_direct_unverified': 'prawdopodobnie bezpośredni (niezweryfikowany)'}
EVK = {'direct': 'bezpośredni', 'indirect': 'pośredni', 'estimate': 'estymacja', 'hypothesis': 'hipoteza'}

ll = json.load(open('raw/longlist.json'))
final = json.load(open('raw/final_status.json'))
cal = json.load(open('raw/calibration.json'))
audits = {json.load(open(f))['id']: json.load(open(f)) for f in glob.glob('raw/audit_*.json')}
refutes = {json.load(open(f))['id']: json.load(open(f)) for f in glob.glob('raw/refute_*.json')}
demands = {json.load(open(f))['id']: json.load(open(f)) for f in glob.glob('raw/demand_*.json')}
ev = json.load(open('raw/evidence_rows.json'))
FINALISTS = set(refutes)

# --- E-DEM / E-* lookup by URL (to cite register IDs next to demand signals) ---
url2ev = {}
for rid, claim, nums, typ, conf, src in ev:
    for u in src.split('; '):
        u = u.replace(' (pierwotne)', '').strip()
        if u.startswith('http'):
            url2ev.setdefault(u.rstrip('/'), rid)

# --- temp-id -> final id ---
temp2final = {}
for x in ll:
    for k in x['merged_from']:
        src, tid = k.split(':', 1)
        temp2final[(src, tid)] = x['final_id']
        temp2final.setdefault(('*', tid), x['final_id'])
SEED = {'A': ['RENO-02', 'RENO-01'], 'B': ['INS-02'], 'C': ['INS-04'], 'D': ['AUTO-01'], 'E': ['JOB-02'], 'F': ['ENER-03'],
        'G': ['CARE-01'], 'H': ['RENT-02', 'RENT-01'], 'I': ['BIZ-04']}


def map_related(src, rel):
    ids = []
    r = rel
    # ranges: G2-01 do G2-16, G3-01 – G3-16, G5-09 – G5-13, S4-R1..S4-R4
    for m in re.finditer(r'(G\d)-(\d\d)\s*(?:do|–|\.\.)\s*(?:G\d-)?(\d\d)', r):
        for n in range(int(m.group(2)), int(m.group(3)) + 1):
            ids.append(f'{m.group(1)}-{n:02d}')
    for m in re.finditer(r'(S\d)-R(\d)\.\.(?:S\d-)?R(\d)', r):
        for n in range(int(m.group(2)), int(m.group(3)) + 1):
            ids.append(f'{m.group(1)}-R{n}')
    ids += re.findall(r'T-S\d-R\d|(?<!T-)S\d-R\d|G\d-\d\d', r)
    out = []
    for t in ids:
        f = temp2final.get((src, t)) or temp2final.get(('*', t))
        if f:
            out.append(f)
    seeds = re.findall(r'Seed ([A-I])', r)
    if src in ('seed_S4', 'topup_T-S4'):
        seeds += re.findall(r'(?<![\w-])([GH])(?![\w-])', r)
    if 'S1-A' in r:
        seeds.append('A')
    if 'S2-F' in r:
        seeds.append('F')
    if src == 'topup_T-S5' and re.search(r'(?<![\w-])S5(?![\w-])', r):
        seeds.append('I')
    for s in seeds:
        out += SEED[s]
    return list(dict.fromkeys(out)), len(ids) + len(seeds)


def norm_status(s):
    s = (s or '').strip()
    for st in STATUS4:
        if s.startswith(st):
            q = s[len(st):].strip(' ()')
            return st, q
    return s, ''


def url_key(u):
    u = (u or '').strip()
    if not u.startswith('http'):
        return ''
    p = urlparse(u)
    return (p.netloc.lower().removeprefix('www.') + p.path.rstrip('/')).lower()


GENERIC = {'www', 'com', 'org', 'net', 'gov', 'io', 'co', 'us', 'app', 'ai', 'tools', 'tool', 'calculator', 'calculators', 'blog',
           'en', 'help', 'support', 'news', 'm', 'edu', 'info', 'biz', 'uk', 'au', 'ca'}
FOREIGN = {'reddit', 'youtube', 'etsy', 'medium', 'facebook', 'linkedin', 'quora', 'x', 'twitter', 'yahoo', 'msn', 'aol', 'substack'}


def url_match(name, url):
    if not (url or '').startswith('http'):
        return 'brak URL'
    host = urlparse(url).netloc.lower().removeprefix('www.')
    labels = [l for l in re.split(r'[.\-]', host) if l and l not in GENERIC]
    nm = re.sub(r'[^a-z0-9]', '', (name or '').lower())
    if any(l in FOREIGN for l in labels) and not any(l in nm for l in labels if l in FOREIGN):
        return 'nie – URL innego serwisu (wzmianka)'
    if any(len(l) >= 3 and l in nm for l in labels):
        return 'tak'
    toks = [t for t in re.findall(r'[a-z0-9]{4,}', (name or '').lower()) if t not in ('calculator', 'calculators', 'tool', 'planner', 'with', 'from')]
    if any(t in host.replace('-', '') for t in toks):
        return 'tak'
    return 'nie – URL innego podmiotu (wzmianka/artykuł)'


def classify(concl, comp):
    c = (concl or '').strip().lower()
    head = c[:80]
    if re.search(r'nie konkurent|sygnał popytu|źródło (danych|reguł)|regulacj', (comp or '').lower() + ' ' + head):
        return 'nie-konkurent'
    if re.search(r'^(prawie|prawdopodobnie|możliwy)[^.]{0,30}(bezpośredni|direct)', head):
        return 'prawdopodobnie bezpośredni (niezweryfikowany)'
    if re.search(r'^\W*(direct|bezpośredni)', head):
        return 'bezpośredni'
    if re.search(r'^\W*(partial|częściowy|częściowa)', head):
        return 'częściowy'
    if re.search(r'^\W*(substitute|substytut)', head):
        return 'substytut'
    for pat, v in [(r'bezpośredni|direct', 'bezpośredni'), (r'częściow|partial', 'częściowy'), (r'substytut|substitute', 'substytut')]:
        if re.search(pat, head):
            return v
    return 'niezweryfikowany'


def row_type(comp, concl):
    t = ((comp or '') + ' | ' + (concl or '')[:120]).lower()
    if re.search(r'sygnał popytu|\(sygnał', t):
        return 'sygnał_popytu'
    if re.search(r'nie konkurent|regulacja|źródło danych|źródło reguł|ustawa|\bsb \d', t):
        return 'źródło_reguł_lub_danych'
    if re.search(r'^\W*\(?brak (konkurenta|narzędzia|wyników)|^\W*nie znaleziono|brak narzędzia w wynikach', (comp or '').lower()):
        return 'brak_wyniku'
    return 'konkurent'


RE_NOTE1 = re.compile(r'notatk[aiy] (z )?fali 1|tylko notatka|brak w search-summary', re.I)
RE_MODEL = re.compile(r'wiedz[ayę]\s+(modelu|treningow)|wiedza treningowa|znan[eya] z wiedzy|z pamięci modelu|model knowledge|training', re.I)
RE_NORES = re.compile(r'nie pojawił|brak w wynikach|nie zwróci|pust[ye] wynik|brak wyników|0 wyników|nie znaleziono w wynikach|nie było w wynikach', re.I)
RE_SS = re.compile(r'search-summary|wzmianka w (search-)?summary|ai-podsumowanie|podsumowanie wyszukiwarki|summary', re.I)
RE_NOQ = re.compile(r'^\W*brak|niewykonan|nie wykonano|not performed|budżet wyszukiwań|limit wyszukiwań|wyczerpan', re.I)


def basis_of(r):
    url = r.get('url', '') or ''
    q = r.get('query', '') or ''
    txt = ' '.join([url, r.get('access_limits', ''), r.get('features_checked', ''), r.get('conclusion', '')])
    if RE_NOTE1.search(txt) and not re.search(r'(?<!nie)(?<!nie )potwierdzon|notatka fali 1 zgodna|skorygowan|utrzyman', txt, re.I):
        return 'notatka fali 1 – niepotwierdzona w fali 2'
    if RE_MODEL.search(txt):
        if not RE_NOQ.search(q) and RE_NORES.search(txt):
            return 'wyszukiwanie wykonane – brak w wynikach; wiedza modelu'
        return 'wiedza modelu – bez wyszukiwania'
    if url.startswith('http') or RE_SS.search(txt):
        if RE_NOQ.search(q):
            return 'wiedza modelu – bez wyszukiwania'
        return 'search-summary – opis w wyniku wyszukiwania'
    if RE_NORES.search(txt) and not RE_NOQ.search(q):
        return 'wyszukiwanie wykonane – brak w wynikach; wiedza modelu'
    return 'wiedza modelu – bez wyszukiwania'


RE_ABSENT = re.compile(r'(^|[\s(;:,–-])(brak|nie porównuje|nie modeluje|nie ma |nie uwzględnia|nie łączy|nie liczy|nie obejmuje|bez |lacks|without|no )', re.I)
ACCESS_OK = re.compile(r'otw|summary|tytuł|wiedz|webfetch|wyszuk|test|hipotez|nieotwier|search', re.I)


def cap(conf, top):
    return conf if RANK.get(conf, 0) <= RANK[top] else top


# =========================== competitor register ===========================
reg = []
for f in sorted(glob.glob('raw/*.json')):
    d = json.load(open(f))
    if not isinstance(d, dict) or 'register' not in d:
        continue
    src = os.path.basename(f)[:-5]
    for r in d['register']:
        if src.startswith('audit_'):
            pid_agent = d['id']; finals = [d['id']]; stage = 'fala 2: audyt top 25'; nmapped = 1
        else:
            pid_agent = r.get('related_idea', '')
            finals, nmapped = map_related(src, pid_agent)
            stage = 'fala 1: rodziny/seedy/uzupełnienia'
        basis = basis_of(r)
        comp = r['competitor']
        um = url_match(comp, r['url'])
        typ = row_type(comp, r['conclusion'])
        klas = classify(r['conclusion'], comp) if typ == 'konkurent' else 'nie-konkurent'
        conf = LV.get(r['confidence'], r['confidence'])
        notes = []
        if basis.startswith('search-summary'):
            conf = cap(conf, 'średnia')
        else:
            conf = cap(conf, 'niska')
            if klas == 'bezpośredni':
                klas = 'prawdopodobnie bezpośredni (niezweryfikowany)'
        if um.startswith('nie'):
            conf = cap(conf, 'niska')
            notes.append('URL nie należy do konkurenta (wzmianka lub artykuł); strona narzędzia nieustalona')
        access = r['access_limits']
        if not ACCESS_OK.search(access or ''):
            access = 'strona nieotwierana (WebFetch zablokowany), dowód: ' + ('search-summary' if basis.startswith('search') else 'wiedza modelu') + \
                     '; ceny i dostęp wg summary/recenzji, niezweryfikowane. Wpis agenta: ' + (access or '—')
        rule9 = ''
        if typ == 'konkurent' and RE_ABSENT.search(r['conclusion'] + ' ' + r['features_checked']):
            rule9 = 'Brak funkcji wnioskowany ze streszczenia, tytułu lub wiedzy modelu (strony nie otwarto) – czytać jako „niezweryfikowane”, nie „brak”.'
        reg.append({
            'data': r['date'], 'etap': stage, 'agent_zrodlowy': src, 'produkt_ID_agenta': pid_agent,
            'produkt_ID_final': ';'.join(finals) if finals else 'nieprzypisany',
            'kwerenda': r['query'], 'URL_zrodla': r['url'], 'url_zgodny_z_nazwa_konkurenta': um, 'konkurent': comp,
            'typ_wiersza': typ, 'klasyfikacja (automatyczna z wniosku)': klas,
            'sprawdzone_funkcje': r['features_checked'], 'ograniczenia_dostepu': access, 'wniosek': r['conclusion'],
            'uwaga_reguly_9': rule9, 'pewnosc': conf, 'podstawa_dowodu': basis,
            'status_weryfikacji': 'strona nieotwierana; ' + ('; '.join(notes) if notes else 'do ręcznej weryfikacji przed decyzją o pilocie'),
            'konflikt_klasyfikacji': '', 'zastapiony_przez_nowsza_fale': '',
        })

for fid, d in sorted(refutes.items()):
    for cnd in d['candidates']:
        um = url_match(cnd['name'], cnd['url'])
        own = um == 'tak' and len(cnd['evidence_pl']) > 150 and not re.search(r'tylko tytuł|wyłącznie tytuł', cnd['evidence_pl'], re.I)
        conf = 'średnia' if own else 'niska'
        klas = TYPE[cnd['classification']]
        rule9 = ''
        if RE_ABSENT.search(cnd['evidence_pl']):
            rule9 = 'Brak funkcji wnioskowany ze streszczenia (strony nie otwarto) – czytać jako „niezweryfikowane”, nie „brak”.'
        reg.append({
            'data': '2026-10-25', 'etap': 'fala 2b: próba obalenia (finaliści)', 'agent_zrodlowy': f'refute_{fid}', 'produkt_ID_agenta': fid,
            'produkt_ID_final': fid,
            'kwerenda': 'nieprzypisane – jedno z 8 zapytań agenta obalającego (pełna lista: data/agent-outputs/refute_' + fid + '.json, pole queries_run)',
            'URL_zrodla': cnd['url'], 'url_zgodny_z_nazwa_konkurenta': um, 'konkurent': cnd['name'],
            'typ_wiersza': 'konkurent', 'klasyfikacja (automatyczna z wniosku)': klas,
            'sprawdzone_funkcje': cnd['evidence_pl'],
            'ograniczenia_dostepu': 'strona nieotwierana (WebFetch zablokowany), dowód: search-summary; do ręcznej weryfikacji: ' + cnd['what_to_check_manually_pl'],
            'wniosek': klas, 'uwaga_reguly_9': rule9, 'pewnosc': conf,
            'podstawa_dowodu': 'search-summary – opis w wyniku wyszukiwania',
            'status_weryfikacji': 'strona nieotwierana; ' + ('URL nie należy do konkurenta (wzmianka lub artykuł); strona narzędzia nieustalona' if um.startswith('nie') else 'do ręcznej weryfikacji przed decyzją o pilocie'),
            'konflikt_klasyfikacji': '', 'zastapiony_przez_nowsza_fale': '',
        })

# dedup exact duplicates
seen, out = set(), []
for r in reg:
    k = (r['produkt_ID_final'], r['konkurent'].lower()[:40], r['URL_zrodla'][:80], r['kwerenda'][:60], r['etap'])
    if k in seen:
        continue
    seen.add(k); out.append(r)

# conflicts: same URL (or same competitor name when no URL) with different competitor classifications
WAVE = {'fala 2b: próba obalenia (finaliści)': 3, 'fala 2: audyt top 25': 2, 'fala 1: rodziny/seedy/uzupełnienia': 1}
groups = {}
for i, r in enumerate(out):
    if r['typ_wiersza'] != 'konkurent' or r['url_zgodny_z_nazwa_konkurenta'].startswith('nie'):
        continue
    k = url_key(r['URL_zrodla']) or re.sub(r'[^a-z0-9]', '', r['konkurent'].lower())[:30]
    groups.setdefault(k, []).append(i)
nconf = 0
for k, idx in groups.items():
    kl = {out[i]['klasyfikacja (automatyczna z wniosku)'] for i in idx}
    kl_main = {x.split(' (')[0] for x in kl}
    if len(kl_main) > 1:
        nconf += 1
        desc = '; '.join(sorted({f"{out[i]['klasyfikacja (automatyczna z wniosku)']} ({out[i]['etap'].split(':')[0]}, {out[i]['produkt_ID_final']})" for i in idx}))
        for i in idx:
            out[i]['konflikt_klasyfikacji'] = 'tak – ten sam URL/konkurent sklasyfikowany różnie: ' + desc
# superseded: same final product + same URL, older wave
nsup = 0
by_pu = {}
for i, r in enumerate(out):
    k = url_key(r['URL_zrodla'])
    if not k:
        continue
    for p in r['produkt_ID_final'].split(';'):
        by_pu.setdefault((p, k), []).append(i)
for (p, k), idx in by_pu.items():
    if len(idx) < 2:
        continue
    top = max(WAVE[out[i]['etap']] for i in idx)
    newest = [i for i in idx if WAVE[out[i]['etap']] == top]
    for i in idx:
        if WAVE[out[i]['etap']] < top and not out[i]['zastapiony_przez_nowsza_fale']:
            out[i]['zastapiony_przez_nowsza_fale'] = f"tak – dla {p} obowiązuje ocena z etapu „{out[newest[0]]['etap']}”"
            nsup += 1

out.sort(key=lambda r: (-WAVE[r['etap']], r['produkt_ID_final'], r['konkurent']))
with open(f'{OUT}/competitor-audit.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
unm = [r for r in out if r['produkt_ID_final'] == 'nieprzypisany']
from collections import Counter
STATS = {
    'register_rows': len(out),
    'unmapped_rows': len(unm),
    'unmapped_examples': sorted({r['produkt_ID_agenta'] for r in unm})[:20],
    'basis': Counter(r['podstawa_dowodu'] for r in out),
    'types': Counter(r['typ_wiersza'] for r in out),
    'klas': Counter(r['klasyfikacja (automatyczna z wniosku)'] for r in out),
    'url_mismatch': sum(1 for r in out if r['url_zgodny_z_nazwa_konkurenta'].startswith('nie')),
    'conflict_groups': nconf, 'superseded': nsup,
    'rule9': sum(1 for r in out if r['uwaga_reguly_9']),
}

# verification upgrade from register: idea named specifically (<=3 ids) in a search-summary row
searched = Counter()
for r in out:
    if r['etap'].startswith('fala 1') and r['podstawa_dowodu'].startswith('search-summary'):
        ids = r['produkt_ID_final'].split(';')
        if 0 < len(ids) <= 3:
            for p in ids:
                searched[p] += 1

# =========================== product opportunities ===========================
NEAR = {
    'AUTO-01': 'Bliski duplikat AUTO-03 (ten sam silnik keep vs trade/replace; AUTO-01 = wyzwalacz ujemny kapitał, AUTO-03 = wyzwalacz wycena naprawy). Traktować jako dwa wejścia do jednego symulatora.',
    'AUTO-03': 'Bliski duplikat AUTO-01: ten sam silnik, inny wyzwalacz (wycena naprawy). Wejście/preset AUTO-01, nie osobny produkt.',
    'CARE-04': 'Bliski duplikat LIFE-01 (dom rodzica: sprzedać/wynająć/zatrzymać — przed i po śmierci). Wariant czasowy LIFE-01.',
    'LIFE-01': 'Bliskie duplikaty: CARE-04 (ten sam dom przed śmiercią rodzica) i LIFE-02 (wykup współwłaściciela = moduł LIFE-01).',
    'LIFE-02': 'Bliski duplikat LIFE-01: wykup współwłaściciela to moduł LIFE-01.',
    'INS-06': 'Podzbiór ENER-03 (pompa sump jako jedno z obciążeń zasilania awaryjnego). Gałąź ENER-03, nie osobny produkt.',
    'ENER-03': 'Obejmuje INS-06 (pompa sump) jako gałąź.',
    'BIZ-05': 'Bliski duplikat BIZ-06 (porównanie ofert MCA/RBF/LOC/karta). Jeden silnik porównania kosztu finansowania firmy.',
    'BIZ-06': 'Bliski duplikat BIZ-05: ten sam silnik porównania ofert finansowania.',
    'RENO-07': 'Część „sprzedaż as-is” pokrywa HOME-03; reszta to wariant RENO-02.',
    'HOME-03': 'Pokrywa część RENO-07 (sprzedaż as-is).',
    'CARE-07': 'Lepiej jako moduł capex w CARE-01 niż osobny produkt (bliski duplikat).',
    'CARE-01': 'Wchłania CARE-07 jako moduł capex.',
    'INS-08': 'Jeden szablon „ubezpieczyć vs samoubezpieczyć” z INS-09, INS-10 i CARE-06 — presety jednego silnika.',
    'INS-09': 'Jeden szablon „ubezpieczyć vs samoubezpieczyć” z INS-08, INS-10 i CARE-06 — preset.',
    'INS-10': 'Jeden szablon „ubezpieczyć vs samoubezpieczyć” z INS-08, INS-09 i CARE-06 — preset.',
    'CARE-06': 'Jeden szablon „ubezpieczyć vs samoubezpieczyć” z INS-08, INS-09 i INS-10 — preset.',
    'RET-01': 'Bliski duplikat RET-03 (wieloletnie konwersje Roth z progiem IRMAA/ACA). RET-03 odrzucony (konkurenci bezpośredni) — dotyczy to też gałęzi ACA w RET-01.',
    'RET-03': 'Bliski duplikat RET-01 (gałąź ACA).',
    'BIZ-15': 'Inny model popytu (newsvendor, jednorazowy zakup sezonowy), ten sam silnik gotówki co BIZ-04 — tryb BIZ-04, nie osobny silnik.',
    'RENO-01': 'Scalony z RENO-02 po audycie: przełącznik PV (demontaż/ponowny montaż) jest w MVP RENO-02, pełna ekonomika PV odroczona. Nie liczy się do odrębnych pomysłów.',
}
OUTSIDE = {'JOB-02': 'poza zakresem startowym domeny', 'HLTH-02': 'poza zakresem startowym domeny (zdrowie)', 'HLTH-01': 'poza zakresem startowym domeny (zdrowie)',
           'LIFE-04': 'poza zakresem startowym domeny (finansowanie studiów)', 'FIN-03': 'poza zakresem startowym domeny (kredyty studenckie)',
           'BIZ-07': 'osobna domena, jeśli w ogóle'}
TEXT_FIX = [
    ('CARE-03', 'uzasadnienie_statusu', 'Wymaga weryfikacji (brak wyszukiwań).',
     'Wymaga dalszej weryfikacji: w fali 1 (T-S4) wyszukiwanie znalazło tylko moduły częściowe, np. HomeAdditionCostCalculator (koszt ADU, czynsz, okres zwrotu; search-summary), bez modułu opieki.'),
    ('CARE-03', 'co_juz_rozwiazano', 'Według wiedzy modelu (niezweryfikowane) istnieją osobne kalkulatory ADU i senior living oraz artykuły o życiu wielopokoleniowym. Integracja jest nieznana.',
     'Search-summary (T-S4): HomeAdditionCostCalculator liczy koszt ADU z czynszem i okresem zwrotu; ParentCareCalc i SeniorCareCalc porównują koszty opieki; są artykuły ADU vs assisted living. Integracja niezweryfikowana.'),
    ('RET-06', 'co_juz_rozwiazano', 'Nieznane (wyszukiwania per-idea zablokowane). Fragment, czyli minimalne RMD, jest prawdopodobnie dobrze pokryty.',
     'Search-summary (G7): takehometax.com Inherited IRA Calculator porównuje trzy strategie wypłat (równe, odroczenie do roku 10, bracket-filling); onetopstop.insure porównuje równe, back-load i front-load. Uwzględnienie IRMAA, ACA i FAFSA niezweryfikowane.'),
    ('FIN-03', 'uzasadnienie_statusu', 'Oficjalny StudentAid.gov Loan Simulator jako konkurent bezpośredni + wysoka zmienność reguł 2026-2028.',
     'Główne argumenty: wysoka zmienność reguł 2026–2028 i StudentLoanCalcs (strona o przejściu SAVE → RAP/IBR/Tiered Standard; search-summary). StudentAid.gov Loan Simulator — prawdopodobnie konkurent częściowy lub bezpośredni (wiedza modelu, niezweryfikowane).'),
    ('BIZ-15', 'uzasadnienie_statusu', 'Ciekawy jako tryb silnika R1 (ten sam model gotówki)', 'Ciekawy jako tryb silnika BIZ-04 (inny model popytu – newsvendor – ten sam model gotówki)'),
]
AUTO_RE = re.compile(r'\(30\.9% trade-in z negative equity, średnio \$7,183\)')
AUTO_NEW = '(Edmunds: 29,1% wymian z ujemnym kapitałem w Q3 2026, średnio 7 107 USD; Q1 2026: 30,9% i 7 183 USD [E-DEM-14])'


def comp_str(cs):
    return '; '.join(f"{c['name']} [{TYPE.get(c['type'], c['type'])}] {c.get('url', '')}".strip() for c in cs)


def demand_text(fid, fallback):
    parts = []
    a = audits.get(fid)
    if a:
        sig = a['demand_signals']
        cnt = Counter(EVK.get(s['evidence_type'], s['evidence_type']) for s in sig)
        ex = []
        for s in sig[:3]:
            rid = url2ev.get((s.get('url') or '').rstrip('/'))
            ex.append(f"[{EVK.get(s['evidence_type'], s['evidence_type'])}] {s['signal_pl'][:220].rstrip()}" + (f' [{rid}]' if rid else ''))
        parts.append(f"Audyt fali 2: {len(sig)} sygnałów (" + ', '.join(f'{k}: {v}' for k, v in cnt.items()) + '). Przykłady: ' + ' | '.join(ex))
    d = demands.get(fid)
    if d:
        de = d['demand_evidence']
        cnt = Counter(EVK.get(x['kind'], x['kind']) for x in de)
        ex = []
        for x in [y for y in de if y['kind'] == 'direct'][:2] + [y for y in de if y['kind'] != 'direct'][:2]:
            rid = url2ev.get((x.get('url') or '').rstrip('/'))
            ex.append(f"[{EVK.get(x['kind'], x['kind'])}] {x['claim_pl'][:200].rstrip()}" + (f' [{rid}]' if rid else ''))
        parts.append(f"Fala 2b (popyt): {len(de)} dowodów (" + ', '.join(f'{k}: {v}' for k, v in cnt.items()) + '). Przykłady: ' + ' | '.join(ex))
    if parts:
        parts.append('Wolumenów wyszukiwań ani promptów nie zmierzono (brak dostępu do danych SEO); „bezpośredni” = pytanie istnieje w tej formie, nie jego skala.')
        return ' '.join(parts)
    return fallback


rows = []
for x in ll:
    fid = x['final_id']
    a = audits.get(fid)
    fs = final.get(fid, {})
    c = cal.get(fid)
    raw_status = fs.get('status') or (a['recommendation'] if a else x['status'])
    status, qual = norm_status(raw_status)
    if fid == 'RENO-01':
        status, qual = 'później', 'przełącznik PV jest w MVP RENO-02; pełna ekonomika PV później'
    note = fs.get('note', '')
    uw = '; '.join(v for v in dict.fromkeys([qual, note, OUTSIDE.get(fid, '')]) if v)
    reason = fs.get('reason') or (a['recommendation_reason_pl'] if a else x['status_reason'])
    comps = x['nearest_competition']
    gap = x['gap']; solved = x['already_solved']
    level = x['verification_level']
    if a:
        comps = [{'name': cc['name'], 'type': cc['type'], 'url': cc['url']} for cc in a['competitors']]
        gap = a['gap_statement_pl']
        solved = '; '.join(f"{cc['name']}: {cc['covers_pl']}" for cc in a['competitors'][:8])
        level = 'audyt fali 2 (7 zapytań); search-summary, strony nieotwierane'
    comp_s = comp_str(comps)
    if fid in refutes:
        rf = refutes[fid]
        comp_s += '; ' + '; '.join(f"[fala 2b] {cc['name']} [{TYPE[cc['classification']]}] {cc['url']}" for cc in rf['candidates'])
        solved += ' || [fala 2b] ' + '; '.join(f"{cc['name']}: {cc['evidence_pl'][:200].rstrip()}…" for cc in rf['candidates'][:6])
        gap += ' || Fala 2b (próba obalenia): ' + rf['conclusion_pl'][:700].rstrip() + ('…' if len(rf['conclusion_pl']) > 700 else '')
        level = 'audyt fali 2 (7 zapytań) + próba obalenia fali 2b (8 zapytań) + badanie popytu fali 2b; search-summary, strony nieotwierane'
    elif not a and searched.get(fid):
        level = f'wstępnie sprawdzony w wyszukiwarce (fala 1; {searched[fid]} wiersz(e) search-summary w rejestrze)'
    elif not a and level == 'koncepcyjny':
        level = 'koncepcyjny (bez wyszukiwań przypisanych do tego pomysłu)'
    conf = LV[x['confidence']]
    if level.startswith('koncepcyjny'):
        conf = 'niska'
        if status == 'odrzucić':
            uw = '; '.join(v for v in [uw, 'odrzucenie koncepcyjne (bez wyszukiwań) – do ponownej oceny przy rozbudowie'] if v)
    if fs.get('conf'):
        conf = fs['conf']
    if status == 'pilot':
        conf = 'niska–średnia'
    direct = ''
    if a:
        scope = 'audyt fali 2: 7 zapytań' + (' + fala 2b: 8 zapytań' if fid in refutes else '') + '; search-summary'
        if fid == 'ENER-03':
            direct = 'sporny: Home Energy Planner — w fali 1 bezpośredni, w fali 2 częściowy; do ręcznej weryfikacji'
        elif fid == 'RENT-01':
            direct = 'sporny: OverlineIQ / BiggerPockets Sell vs Keep — w fali 1 (seed H) bezpośredni dla rdzenia hold vs sell, w fali 2 częściowy; do ręcznej weryfikacji'
        elif c and c['direct']:
            direct = f'tak ({scope}; pewność średnia)'
        else:
            direct = f'Nie znaleziono bezpośredniego konkurenta w badanym zakresie ({scope}; pewność niska–średnia)'
    row = {
        'ID': fid,
        'nazwa_robocza_en': fs.get('name') or x['name_en'],
        'odrebny_pomysl': 'nie (scalony z RENO-02)' if fid == 'RENO-01' else 'tak',
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
        'najblizsza_konkurencja': comp_s,
        'co_juz_rozwiazano': solved,
        'istotny_brak_w_istniejacych_produktach': gap,
        'trudnosc_implementacji': LV[x['impl_difficulty']],
        'obciazenie_utrzymaniem': LV[x['maintenance_burden']],
        'ryzyko_merytoryczne': LV[x['content_risk']],
        'ryzyko_ze_asystent_AI_rozwiaze_sam': LV[x['ai_self_solve_risk']],
        'dowody_popytu': demand_text(fid, x['demand_evidence']),
        'otoczenie_reklamowe': x['ad_environment'],
        'poziom_pewnosci (oceny/statusu)': conf,
        'status': status,
        'uwaga_statusu': uw,
        'uzasadnienie_statusu': reason,
        'rekomendacja_audytora (top 25)': a['recommendation'] if a else '',
        'poziom_weryfikacji': level,
        'ocena_agenta_0_5 (top 25)': f"{c['agent']:.2f}" if c else '',
        'ocena_po_kalibracji_0_5 (top 25)': f"{c['cal']:.2f}" if c else '',
        'zmienione_kryteria_w_kalibracji': ', '.join(f"{KPL[k]} {a['scores'][k]['score']}→{v}" for k, v in c['adj'].items()) if c and c['adj'] else ('brak zmian' if c else ''),
        'bezposredni_konkurent (top 25)': direct,
        'scalone_z_pomyslow_agentow': ', '.join(x['merged_from']),
        'uwagi_scalenia_i_bliskie_duplikaty': ' '.join(v for v in [x['merge_note'], NEAR.get(fid, '')] if v),
    }
    if fid == 'BIZ-15':
        row['uwagi_scalenia_i_bliskie_duplikaty'] = NEAR['BIZ-15']
    if fid == 'FIN-03':
        row['najblizsza_konkurencja'] = re.sub(r'Federal Student Aid[^;]*', 'StudentAid.gov Loan Simulator [prawdopodobnie częściowy lub bezpośredni – wiedza modelu, niezweryfikowane]', row['najblizsza_konkurencja'])
        row['uwagi_scalenia_i_bliskie_duplikaty'] = ''
    for k in ('uzasadnienie_statusu', 'dowody_popytu'):
        row[k] = AUTO_RE.sub(AUTO_NEW, row[k])
    for i, k, old, new in TEXT_FIX:
        if i == fid:
            if old in row[k]:
                row[k] = row[k].replace(old, new)
            elif new not in row[k]:
                print('TEXT_FIX not applied', fid, k)
    rows.append(row)

VOCAB = {'ID', 'odrebny_pomysl', 'trudnosc_implementacji', 'obciazenie_utrzymaniem', 'ryzyko_merytoryczne', 'ryzyko_ze_asystent_AI_rozwiaze_sam',
         'poziom_pewnosci (oceny/statusu)', 'status', 'uwaga_statusu', 'rekomendacja_audytora (top 25)', 'ocena_agenta_0_5 (top 25)',
         'ocena_po_kalibracji_0_5 (top 25)', 'zmienione_kryteria_w_kalibracji', 'bezposredni_konkurent (top 25)', 'scalone_z_pomyslow_agentow',
         'uwagi_scalenia_i_bliskie_duplikaty', 'rodzina', 'nazwa_robocza_en'}
EVIDENCE_FIELDS = ['najblizsza_konkurencja', 'co_juz_rozwiazano', 'istotny_brak_w_istniejacych_produktach', 'powod_wejscia_na_zewnetrzna_strone',
                   'dowody_popytu', 'otoczenie_reklamowe']
nfill = 0
for row in rows:
    for k in EVIDENCE_FIELDS:
        v = row[k]
        if len((v or '').strip()) < 25:
            row[k] = f"{(v or '').strip().rstrip('.')} — ocena koncepcyjna agenta; nie badano w tej sesji (brak danych)."
            nfill += 1

with open(f'{OUT}/product-opportunities.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
STATS.update({
    'product_rows': len(rows), 'distinct': sum(1 for r in rows if r['odrebny_pomysl'] == 'tak'),
    'status': Counter(r['status'] for r in rows), 'status_distinct': Counter(r['status'] for r in rows if r['odrebny_pomysl'] == 'tak'),
    'verification': Counter(r['poziom_weryfikacji'].split(' (')[0].split(';')[0] for r in rows),
    'placeholders_filled': nfill,
})
for k, v in STATS.items():
    print(k, dict(v) if isinstance(v, Counter) else v)
json.dump({k: (dict(v) if isinstance(v, Counter) else v) for k, v in STATS.items()}, open('raw/csv_stats.json', 'w'), ensure_ascii=False, indent=1)
