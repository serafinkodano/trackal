"""Build research/product-opportunities.csv and research/competitor-audit.csv (wersja po recenzji fali 3).

Wejście (katalog roboczy = katalog z `raw/` = research/data/agent-outputs/ + wyniki skryptów):
  raw/longlist.json, raw/final_status.json, raw/calibration.json, raw/audit_*.json, raw/refute_*.json,
  raw/demand_*.json, raw/evidence_rows.json oraz pliki z polem `register` (fala 1).
"""
import csv, glob, json, os, re, sys
from urllib.parse import urlparse

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/trackal/research'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import build_cards as bc  # wspólne poprawki tekstu (bc.fix) i dwuosiowe etykiety popytu (bc.demand_label)
W = {'demand': .20, 'gap': .20, 'ai_distribution': .15, 'ad_potential': .15, 'feasibility': .10, 'reliability': .10, 'shared_engine': .10}
KPL = {'demand': 'popyt', 'gap': 'luka', 'ai_distribution': 'dystrybucja AI', 'ad_potential': 'reklama', 'feasibility': 'wykonalność',
       'reliability': 'wiarygodność', 'shared_engine': 'wspólny silnik'}
LV = {'low': 'niska', 'medium': 'średnia', 'high': 'wysoka'}
RANK = {'niska': 0, 'średnia': 1, 'wysoka': 2}
STATUS4 = ['pilot', 'zbadać', 'później', 'odrzucić']
TYPE = {'direct': 'bezpośredni', 'partial': 'częściowy', 'substitute': 'substytut',
        'probably_direct_unverified': 'sporny (do ręcznej weryfikacji; wiedza modelu)'}
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
    if re.search(r'nie konkurent(?! bezpośredni)|sygnał popytu|źródło (danych|reguł)|regulacj', (comp or '').lower() + ' ' + head):
        return 'nie-konkurent'
    if re.search(r'^(prawie|prawdopodobnie|możliwy)[^.]{0,30}(bezpośredni|direct)', head):
        return 'sporny (do ręcznej weryfikacji; wiedza modelu)'
    if re.search(r'^\W*(direct|bezpośredni)', head):
        return 'bezpośredni'
    if re.search(r'^\W*(partial|częściowy|częściowa)', head):
        return 'częściowy'
    if re.search(r'^\W*(substitute|substytut)', head):
        return 'substytut'
    if re.search(r'(częściow\w*|partial)\s+lub\s+(bezpośredni|direct)|(bezpośredni\w*|direct)\s+lub\s+(częściow|partial)', head):
        return 'sporny (częściowy lub bezpośredni)'
    hits = []
    for pat, v in [(r'bezpośredni|direct', 'bezpośredni'), (r'częściow|partial', 'częściowy'), (r'substytut|substitute', 'substytut')]:
        m = re.search(pat, head)
        if m:
            hits.append((m.start(), v))
    return min(hits)[1] if hits else 'niezweryfikowany'


def row_type(comp, concl):
    t = ((comp or '') + ' | ' + (concl or '')[:120]).lower()
    if re.search(r'sygnał popytu|\(sygnał', t):
        return 'sygnał_popytu'
    if re.search(r'nie konkurent(?! bezpośredni)|regulacja|źródło danych|źródło reguł|ustawa|\bsb \d', t):
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



TEXT_SUBS = [
    ('(kontekst zadania: od 7.10.2026 i 19.08.2026)', '(daty z briefu właściciela potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]: AI Mode od 19.08.2026, Intelligent UI od 7–8.10.2026)'),
    ('kontekst zadania: ChatGPT Intelligent UI od 2026-10-07, Google AI Mode od 2026-08-19', 'brief właściciela, daty potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]: Intelligent UI od 7–8.10.2026, AI Mode od 19.08.2026'),
    ('kontekst zadania', 'brief właściciela; daty potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]'),
    ('prawie bezpośredni', 'możliwie bezpośredni (niezweryfikowane)'),
    ('SERP jest zdominowany przez domeny o wysokim autorytecie (YMYL)', 'w wynikach wyszukiwania (search-summary) dominują domeny o wysokim autorytecie (YMYL); pełnego SERP nie badano (K-05)'),
    ('SERP jest zatłoczony', 'wyniki wyszukiwania (search-summary) są zatłoczone'),
    ('solidny popyt', 'dobrą ocenę popytu (4/5, sygnały pośrednie)'),
    ('ekspert 11–17 h (nie jest tani)', 'ekspert 24–36 h wg agenta fali 2b (nie jest tani)'),
    (', a popyt wyraźny dzięki lock-in w 2026', ', a ocena popytu 4 opiera się na sygnałach pośrednich (popyt online niezmierzony); wpływ lock-in stóp w 2026 na wagę decyzji to hipoteza'),
    ('duży i powtarzalny popyt na decyzję', 'częsta decyzja (skala zdarzeń: originations HELOC/home equity; nie pomiar popytu online)'),
    ('realny popyt i wysoka reużywalność silnika', 'ocena popytu 4 na sygnałach pośrednich (popyt niezmierzony) i wysoka reużywalność silnika'),
    ('dobry popyt (4)', 'dobra ocena popytu (4, sygnały pośrednie)'),
    ('Pokazuje realny popyt', 'Sygnał pośredni (pojedynczy wątek z forum), nie pomiar popytu'),
    ('bezpośredni sygnał popytu na dylemat kolejności', 'pośredni sygnał (anegdota z forum) dylematu kolejności'),
    ('Żadnego narzędzia łączącego dach, PV i sprzedaż.', 'W streszczeniach nie widać narzędzia łączącego dach, PV i sprzedaż (niezweryfikowane).'),
    ('Częściowy/bliski bezpośredniemu dla rdzenia', 'Częściowy (możliwy bezpośredni — do ręcznej weryfikacji) dla rdzenia'),
    ('potencjalnie bliski bezpośredniemu', 'możliwy bezpośredni (do ręcznej weryfikacji)'),
    ('Częściowy, bliski bezpośredniemu', 'Częściowy (możliwy bezpośredni — do ręcznej weryfikacji)'),
    ('CarCalcPro już łączy rollover, LTV i moment wyjścia z underwater', 'według streszczeń wyszukiwarki CarCalcPro łączy już rollover, LTV i moment wyjścia z underwater (niezweryfikowane)'),
    (', rozważając monetyzację afiliacyjną lub lead-gen zamiast AdSense', '; w modelu bazowym (AdSense) produkt się nie broni (wąska publiczność B2B), a afiliacja lub lead-gen do 3PL to tylko ewentualny dodatek albo osobna decyzja poza modelem bazowym'),
    ('z monetyzacją afiliacyjną (finansowanie zapasów, 3PL, SaaS)', 'z ewentualną afiliacją jako dodatkiem (finansowanie zapasów, 3PL, SaaS; poza modelem bazowym)'),
    ('Budować tylko, jeśli ręczna weryfikacja nie znajdzie zegara §121 + 4 wariantów w jednym narzędziu.',
     'Budować tylko po własnym pomiarze popytu i SERP (jak G0, kroki 2–3) i jeśli ręczna weryfikacja (TrueHomeCosts, Bellhaven, TeamzLab i kandydaci z karty) nie znajdzie narzędzia pokrywającego ≥ 3 kluczowe zależności: zegar §121, recapture, wartość niskiej stopy, warianty najmu i sprzedaży.'),
    ('Budować tylko, jeśli ręczna weryfikacja potwierdzi, że nikt nie rozbija „kary za utratę niskiej stopy” i finansowania HELOC/cash-out w jednym modelu.',
     'Budować tylko po własnym pomiarze popytu i SERP (jak G0, kroki 2–3) i jeśli ręczna weryfikacja (BusinessCaseGuy, Dr. Brian Jones, TrueHomeCosts, FinHome, AgentCalc i pozostali kandydaci z karty) nie znajdzie narzędzia pokrywającego ≥ 3 kluczowe zależności z karty HOME-04: kara za utratę niskiej stopy, finansowanie remontu HELOC vs cash-out, ponowna wycena podatku od nieruchomości, basis/§121, przekroczenia budżetu, scenariusz spadku stóp i refinansu.'),
    ('Dane Edmunds: Q1 2026 30,9%/7 183 USD; Q3 2026 29,1%/7 107 USD.',
     'Dane Edmunds: Q2 2026 29,6%/6 884 USD (potwierdzone, E-REV-07); Q1 2026 30,9%/7 183 USD; Q3 2026 29,1%/7 107 USD (wg agenta, jedno niepotwierdzone źródło, E-DEM-14).'),
    ('(RothHelper, QuantCalc ACA Bridge Optimizer, a także CoastIQ, ThunderHarbor i acaoptimizer)',
     '(konkurenci bezpośredni: RothHelper, QuantCalc ACA Bridge Optimizer; częściowi, pewność niska: CoastIQ, ThunderHarbor, acaoptimizer)'),
    ('OverlineIQ, top1031, Resideline częściowo pokrywają', 'OverlineIQ (sporny), top1031 i Resideline (częściowi) pokrywają fragmenty'),
    ('Popyt jest realny i rosnący', 'Sygnały popytu są pośrednie (zdarzenia, podaż treści); wolumenów nie zmierzono'),
    ('Popyt istnieje i jest widoczny na forach', 'Pytania pojawiają się na forach (anegdotycznie); wolumenów nie zmierzono'),
    ('Profil jest mocny w popycie', 'Ocena popytu jest wysoka, ale opiera się na sygnałach pośrednich'),
    ('Popyt i potencjał reklamowy są mocne', 'Ocena popytu (sygnały pośrednie) i potencjału reklamowego jest wysoka'),
    ('Popyt i wartość reklamowa wyglądają mocno', 'Ocena popytu (sygnały pośrednie) i wartości reklamowej jest wysoka'),
    ('realny popyt pytaniowy', 'pytania widoczne online (sygnał pośredni, bez wolumenu)'),
    ('Silny popyt wymuszony zdarzeniem', 'Duża skala zdarzenia (sygnał pośredni, nie pomiar popytu online)'),
    ('Silny popyt tematyczny', 'Duża podaż treści na temat (sygnał pośredni)'),
    ('decyzja dotyczy bardzo dużej grupy kupujących rocznie', 'to skala zdarzeń, nie popyt online'),
]


def apply_subs(rows_, cards_fix=False):
    for r in rows_:
        for k, v in r.items():
            if isinstance(v, str):
                for a_, b_ in TEXT_SUBS:
                    v = v.replace(a_, b_)
                if cards_fix and k not in ('ID', 'status', 'odrebny_pomysl'):
                    v = bc.fix(v)
                r[k] = v

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
                klas = 'sporny (do ręcznej weryfikacji; wiedza modelu)'
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
            'kwerenda': ' ; '.join(d['queries_run']) + ' (kandydat nieprzypisany do konkretnego zapytania; lista z data/agent-outputs/refute_' + fid + '.json)',
            'URL_zrodla': cnd['url'], 'url_zgodny_z_nazwa_konkurenta': um, 'konkurent': cnd['name'],
            'typ_wiersza': 'konkurent', 'klasyfikacja (automatyczna z wniosku)': klas,
            'sprawdzone_funkcje': cnd['evidence_pl'],
            'ograniczenia_dostepu': 'strona nieotwierana (WebFetch zablokowany), dowód: search-summary; do ręcznej weryfikacji: ' + cnd['what_to_check_manually_pl'],
            'wniosek': klas, 'uwaga_reguly_9': rule9, 'pewnosc': conf,
            'podstawa_dowodu': 'search-summary – opis w wyniku wyszukiwania',
            'status_weryfikacji': 'strona nieotwierana; ' + ('URL nie należy do konkurenta (wzmianka lub artykuł); strona narzędzia nieustalona' if um.startswith('nie') else 'do ręcznej weryfikacji przed decyzją o pilocie'),
            'konflikt_klasyfikacji': '', 'zastapiony_przez_nowsza_fale': '',
        })

# wave-1 rows whose conclusion classifies several ideas differently ("DIRECT dla G6-03; PARTIAL dla G6-02") -> one row per product
TID = re.compile(r'T-S\d-R\d|(?<!T-)S\d-R\d|G\d-\d\d')
split = []
for r in reg:
    finals = r['produkt_ID_final'].split(';')
    if not r['etap'].startswith('fala 1') or len(finals) < 2 or r['typ_wiersza'] != 'konkurent':
        split.append(r); continue
    per, current = {}, None
    for seg in re.split(r'[;.]', r['wniosek']):
        k = classify(seg, r['konkurent'])
        if k != 'niezweryfikowany':
            current = k            # klasyfikacja obowiązuje do następnego określenia w tym samym wniosku
        for t in TID.findall(seg):
            f = temp2final.get((r['agent_zrodlowy'], t)) or temp2final.get(('*', t))
            if f and current:
                per.setdefault(f, current)
    if not per:
        split.append(r); continue
    for f in finals:
        r2 = dict(r)
        r2['produkt_ID_final'] = f
        r2['klasyfikacja (automatyczna z wniosku)'] = per.get(f, 'niezweryfikowany (wniosek dotyczy innego zakresu)')
        split.append(r2)
reg = split

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

CONTESTED = {'ENER-03': 'home energy planner', 'RENT-01': 'overlineiq'}
for r in out:
    if not r['etap'].startswith('fala 1') or r['typ_wiersza'] != 'konkurent':
        continue
    if not r['klasyfikacja (automatyczna z wniosku)'].startswith(('bezpośredni', 'prawdopodobnie bezpośredni', 'sporny')):
        continue
    notes_ = []
    for pid in r['produkt_ID_final'].split(';'):
        if pid in CONTESTED and CONTESTED[pid] in r['konkurent'].lower():
            notes_.append(f'nie – dla {pid} klasyfikacja sporna (fala 1: bezpośredni, fala 2: częściowy); rozstrzyga ręczna weryfikacja (K-03)')
        elif pid in CONTESTED:
            notes_.append(f'nie – brak oceny w nowszej fali; dla {pid} zakres do ręcznej weryfikacji (K-03)' + ('; bezpośredni dla rdzenia hold/sell seeda H (RENT-02)' if 'biggerpockets' in r['konkurent'].lower() else ''))
        elif pid in audits and not cal.get(pid, {}).get('direct'):
            notes_.append(f"tak – dla {pid} w audycie fali 2{' i próbie obalenia fali 2b' if pid in refutes else ''} nie potwierdzono konkurenta bezpośredniego; obowiązuje ocena nowszej fali")
    if notes_:
        r['zastapiony_przez_nowsza_fale'] = ' | '.join(notes_)
out.sort(key=lambda r: (-WAVE[r['etap']], r['produkt_ID_final'], r['konkurent']))
apply_subs(out)
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
    'AUTO-01': 'Wspólny silnik z AUTO-03, ale inna decyzja (AUTO-01: wyjście z ujemnego kapitału; AUTO-03: naprawa vs wymiana po wycenie naprawy) i inne warianty — oba liczone jako odrębne pomysły.',
    'AUTO-03': 'Wspólny silnik z AUTO-01, ale inna decyzja (naprawa vs wymiana) i inne warianty; budować jako drugi tryb tego samego silnika, po wyniku AUTO-01.',
    'CARE-04': 'Wspólny silnik z LIFE-01, ale inna decyzja (dom rodzica przed jego śmiercią: Medicaid, brak step-up, darowizna) — odrębny pomysł.',
    'LIFE-01': 'Wspólne moduły z CARE-04 (ten sam dom przed śmiercią rodzica) i LIFE-02 (wykup współwłaściciela); to odrębne decyzje z innymi regułami.',
    'LIFE-02': 'Wspólny moduł wykupu współwłaściciela z LIFE-01, ale inna decyzja (rozwód: QDRO, refinansowanie, §1041) — odrębny pomysł.',
    'INS-06': 'Podzbiór ENER-03 (pompa sump jako jedno z obciążeń zasilania awaryjnego). Gałąź ENER-03 — nie liczy się do odrębnych pomysłów.',
    'ENER-03': 'Obejmuje INS-06 (pompa sump) jako gałąź.',
    'BIZ-05': 'Obejmuje BIZ-06 (czekanie na SBA vs finansowanie pomostowe) jako wariant tego samego porównania ofert.',
    'BIZ-06': 'Wariant BIZ-05 (to samo porównanie ofert finansowania z opcją czekania na SBA) — nie liczy się do odrębnych pomysłów.',
    'RENO-07': 'Część „sprzedaż as-is” pokrywa HOME-03; reszta to wariant RENO-02.',
    'HOME-03': 'Pokrywa część RENO-07 (sprzedaż as-is).',
    'CARE-07': 'Moduł capex CARE-01 (warianty CARE-07 są podzbiorem wariantów CARE-01) — nie liczy się do odrębnych pomysłów.',
    'CARE-01': 'Wchłania CARE-07 jako moduł capex.',
    'INS-08': 'Wspólny szablon obliczeń „ubezpieczyć vs samoubezpieczyć” z INS-09, INS-10 i CARE-06; to różne decyzje i modele (auto, zwierzę, gwarancja domu, LTC), nie presety.',
    'INS-09': 'Wspólny szablon obliczeń „ubezpieczyć vs samoubezpieczyć” z INS-08, INS-10 i CARE-06; inna decyzja i model (ubezpieczenie zwierzęcia).',
    'INS-10': 'Wspólny szablon obliczeń „ubezpieczyć vs samoubezpieczyć” z INS-08, INS-09 i CARE-06; inna decyzja i model (gwarancja domu).',
    'CARE-06': 'Wspólny szablon obliczeń „ubezpieczyć vs samoubezpieczyć” z INS-08, INS-09 i INS-10; inna decyzja i znacznie bardziej złożony model (LTC).',
    'RET-01': 'Bliski duplikat RET-03 (wieloletnie konwersje Roth z progiem IRMAA/ACA). RET-03 odrzucony (konkurenci bezpośredni) — dotyczy to też gałęzi ACA w RET-01.',
    'RET-03': 'Bliski duplikat RET-01 (gałąź ACA).',
    'BIZ-15': 'Inny model popytu (newsvendor, jednorazowy zakup sezonowy) i inne warianty niż BIZ-04; wspólny silnik gotówki — odrębny pomysł.',
    'RENO-01': 'Scalony z RENO-02 po audycie: przełącznik PV (demontaż/ponowny montaż) jest w MVP RENO-02, pełna ekonomika PV odroczona. Nie liczy się do odrębnych pomysłów.',
}
OUTSIDE = {'HLTH-02': 'poza zakresem startowym domeny (zdrowie)', 'HLTH-01': 'poza zakresem startowym domeny (zdrowie)',
           'LIFE-04': 'poza zakresem startowym domeny (finansowanie studiów)', 'FIN-03': 'poza zakresem startowym domeny (kredyty studenckie)'}
NOT_DISTINCT = {'RENO-01': 'nie (gałąź RENO-02)', 'INS-06': 'nie (gałąź ENER-03)', 'CARE-07': 'nie (moduł CARE-01)', 'BIZ-06': 'nie (wariant BIZ-05)'}
DOMAIN_NOTE = {
    'RET': 'poza zakresem startowym domeny (emerytura)', 'CARE': 'poza zakresem startowym domeny (opieka i starzenie)',
    'JOB': 'poza zakresem startowym domeny (praca, relokacja, benefity)',
    'BIZ': 'poza domeną; ewentualny test w istniejącym serwisie e-commerce właściciela, osobna domena dopiero po spełnieniu warunków 3 i 4 (architecture-and-validation.md §1.2)',
}
TEXT_FIX = [
    ('BIZ-13', 'uzasadnienie_statusu', 'Dobry kandydat na drugi symulator w pilocie wspólnego silnika.',
     'Poza domeną wariantu B (mała firma/e-commerce); ewentualny test w istniejącym serwisie e-commerce właściciela (architecture-and-validation.md §1.2).'),
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
AUTO_NEW = '(Edmunds: Q2 2026 29,6% wymian z ujemnym kapitałem, średnio 6 884 USD — potwierdzone [E-REV-07]; Q3 2026 29,1% i 7 107 USD wg agenta, niepotwierdzone [E-DEM-14]; Q1 2026 30,9% i 7 183 USD)'


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
            ex.append(f"[siła źródła wg audytora: {EVK.get(s['evidence_type'], s['evidence_type'])}] {s['signal_pl'][:220].rstrip()}" + (f' [{rid}]' if rid else ''))
        parts.append(f"Audyt fali 2: {len(sig)} sygnałów (siła źródła wg audytora — " + ', '.join(f'{k}: {v}' for k, v in cnt.items()) + '). Przykłady: ' + ' | '.join(ex))
    d = demands.get(fid)
    if d:
        de = d['demand_evidence']
        ex = []
        for i, x in enumerate(de[:4]):
            rid = url2ev.get((x.get('url') or '').rstrip('/'))
            ex.append(f"{bc.demand_label(fid, i, x)} {x['claim_pl'][:200].rstrip()}" + (f' [{rid}]' if rid else ''))
        parts.append(f"Fala 2b (popyt): {len(de)} dowodów; pokazano 4 pierwsze z etykietami w dwóch osiach jak w top-10-products.md (pełna lista: data/agent-outputs/demand_{fid}.json). Przykłady: " + ' | '.join(ex))
    if parts:
        parts.append('Legenda: „siła źródła” ocenia źródło (pierwotne/wtórne), nie popyt; dwuosiowe etykiety (siła · co mierzy) jak w top-10-products.md §1.2. Wolumenów wyszukiwań ani promptów nie zmierzono (brak dostępu do danych SEO): bezpośrednich dowodów popytu online w tej sesji jest 0.')
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
    if fid == 'INS-06':
        status, qual = 'później', 'gałąź ENER-03 (nie odrębny); zamiennik seeda F; wraca razem z ENER-03'
    note = fs.get('note', '')
    if note in ('osobna domena, jeśli w ogóle', 'poza domeną', 'poza zakresem startowym domeny'):
        note = ''
    if fid == 'ENER-01':
        note = 'odrębna decyzja (forma własności PV); korzysta z modułu PV RENO-02'
    if fid == 'INS-01':
        note = 'odrębna decyzja (czy zgłaszać szkodę); próg „zgłosić szkodę” wchodzi też jako moduł RENO-02'
    if fid == 'AUTO-03':
        note = 'ten sam silnik co AUTO-01; odrębna decyzja (naprawa vs wymiana)'
    if fid == 'RENT-02':
        note = 'wariant capex seeda H (rdzeń hold/sell seeda H odrzucony)'
    if fid == 'ENER-03':
        note = 'ogólna wersja seeda F; konkurent sporny (Home Energy Planner: fala 1 bezpośredni, fala 2 częściowy)'
    uw = '; '.join(v for v in dict.fromkeys([qual, note, OUTSIDE.get(fid, '') or DOMAIN_NOTE.get(x['family_code'], '')]) if v)
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
            direct = 'sporny: OverlineIQ — w fali 1 (seed H) bezpośredni, w audycie fali 2 częściowy; do ręcznej weryfikacji. BiggerPockets Sell vs Keep jest bezpośredni dla rdzenia hold/sell seeda H; dla zakresu RENT-01 (1031, step-up, sprzedaż ratalna) niezweryfikowany'
        elif fid == 'RET-03':
            direct = f'tak: RothHelper, QuantCalc ACA Bridge Optimizer ({scope}; pewność średnia)'
        elif c and c['direct']:
            direct = f'tak ({scope}; pewność średnia)'
        else:
            direct = f'Nie znaleziono bezpośredniego konkurenta w badanym zakresie ({scope}; pewność niska–średnia)'
    row = {
        'ID': fid,
        'nazwa_robocza_en': fs.get('name') or x['name_en'],
        'odrebny_pomysl': NOT_DISTINCT.get(fid, 'tak'),
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
    if fid in ('RENO-05', 'CARE-05', 'CARE-08', 'JOB-04'):
        row['uwagi_scalenia_i_bliskie_duplikaty'] = (row['uwagi_scalenia_i_bliskie_duplikaty'] + ' Odrębna decyzja (inne warianty lub wynik); „moduł” w uzasadnieniu to rekomendowana forma budowy, nie scalenie.').strip()
    TAGS = {'ENER-03': (r'(Home Energy Planner[^;\[]*)\[częściowy\]', r'\1[sporny: fala 1 bezpośredni, fala 2 częściowy; do ręcznej weryfikacji]'),
            'RENT-01': (r'(OverlineIQ[^;\[]*)\[częściowy\]', r'\1[sporny: fala 1 bezpośredni, fala 2 częściowy]'),
            'RENT-02': (r'(BiggerPockets[^;\[]*Sell vs\. Keep[^;\[]*)\[częściowy\]', r'\1[częściowy dla wariantu capex RENT-02; bezpośredni dla rdzenia hold/sell seeda H]')}
    if fid in TAGS:
        row['najblizsza_konkurencja'] = re.sub(TAGS[fid][0], TAGS[fid][1], row['najblizsza_konkurencja'])
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

TEMP_ID = re.compile(r'(?<![\w-])(T-S\d-R\d|S\d-R\d|G\d-\d\d)(?![\w-])')
for row in rows:
    for k in list(row):
        if k in ('ID', 'scalone_z_pomyslow_agentow') or not isinstance(row[k], str):
            continue
        row[k] = TEMP_ID.sub(lambda m: temp2final.get(('*', m.group(1)), m.group(1)), row[k])
apply_subs(rows, cards_fix=True)
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
