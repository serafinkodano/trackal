#!/usr/bin/env python3
"""Generuje research/evidence-and-assumptions.md (część opisowa + rejestr dowodów).

Wejście (ścieżki względem katalogu nadrzędnego wobec tools/):
- evidence_head.md                — część opisowa (sekcje 0–7, nagłówek tabeli rejestru);
- raw/evidence_rows.json          — wiersze rejestru: (id, treść, liczby, typ, pewność, źródła);
- raw/evidence_overrides.json     — poprawki po recenzji fali 3:
    set      — zastępuje wskazane pola wiersza,
    replace  — podmienia fragment tekstu (stary fragment musi wystąpić dokładnie raz),
    append   — dopisuje nowe wiersze na końcu rejestru (np. E-REV-01…09),
    reguly   — reguły dla wszystkich wierszy (pewność hipotez, wyjątki od skracania).

W evidence_head.md można używać znaczników liczonych z plików CSV w research/:
    {{rows:plik.csv}}                    — liczba wierszy danych,
    {{n:plik.csv:kolumna=wartość}}       — liczba wierszy z daną wartością w kolumnie,
    {{n:plik.csv:k1=w1&&k2=w2}}          — liczba wierszy spełniających wszystkie warunki naraz,
    {{nonempty:plik.csv:kolumna}}        — liczba wierszy z niepustą wartością,
    {{distinct:plik.csv:kolumna}}        — liczba różnych niepustych wartości,
    {{register_rows}}                    — liczba wierszy rejestru dowodów po poprawkach.

Uruchomienie:
    cd <scratchpad> && python3 tools/build_evidence.py
Skrypt kończy się kodem 1, jeśli tabela markdown jest zepsuta, znacznik jest nieznany,
poprawka nie pasuje do danych albo ID się powtarza.
"""
import csv
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = '/home/user/trackal/research'
OUT = os.path.join(RESEARCH, 'evidence-and-assumptions.md')
HEAD = os.path.join(BASE, 'evidence_head.md')
ROWS = os.path.join(BASE, 'raw', 'evidence_rows.json')
OVERRIDES = os.path.join(BASE, 'raw', 'evidence_overrides.json')

FIELDS = ['tresc', 'liczby', 'typ', 'pewnosc', 'zrodla']
CUT_CLAIM, CUT_NUMS = 650, 250
CONF_RANK = {'niska': 0, 'niska–średnia': 1, 'średnia': 2, 'wysoka': 3}
# Sformułowania, których raport nie używa (kanon fali 3); ostrzeżenie, nie błąd.
FORBIDDEN = ['brak konkurencji', 'prawie bezpośredni', '7 USD/1000', '7,0 USD', '143 tys. sesji',
             '9 / 13 / 18', 'nagradza', 'generatory słabną', 'domen enterprise', 'RPM = CPC',
             'popyt potwierdz', 'nie odczytałem', 'i to w źródle pierwotnym']
# Liczby i sformułowania sprzed przeliczenia modelu (kanon v1 → v2); sprawdzane tylko w części
# opisowej (evidence_head.md), bo rejestr dowodów cytuje źródła dosłownie; ostrzeżenie, nie błąd.
STALE = ['7,6 tys. USD', '3,7 tys. USD', '273 h', '273 / 200 / 127', '4 500 / 2 450', '2 450 USD',
         '18 / 14 / 11', '55–90', '55-90', '265 tys.', '22 tys. sesji', '880 / 350 / 180',
         '860 tys.', '1,84 mln', '24 / 12,9', '485 / 380', '−52 tys', '-52 tys', 'mies. 21',
         'mies. 34', '42 tys. / 2,7', 'limitem gotówki do ok. 8 tys', 'gotówki do ok. 8 tys',
         '95 odrębnych', 'odrębnych pomysłów 95', 'zbadać 28', 'później 37', 'kandydat do audytu: INS-06',
         'osobnej domeny', '(K3)', '≥ 5 tys. wyszukiwań', '4 prompty z prośbą', 'w źródle pierwotnym',
         'nie odczytałem', '4 / 2 / 1 h']

errors, warnings = [], []


def cut(s, n):
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' …'


def clean(s):
    """Komórka tabeli: bez nowych linii; znak | ucieczką, żeby nie psuł tabeli."""
    s = ' '.join(str(s).split())
    return s.replace('|', '\\|')


# ---------- wiersze i poprawki ----------
rows = [dict(zip(['id'] + FIELDS, r)) for r in json.load(open(ROWS, encoding='utf-8'))]
by_id = {r['id']: r for r in rows}
if len(by_id) != len(rows):
    errors.append('powtórzone ID w raw/evidence_rows.json')

ov = json.load(open(OVERRIDES, encoding='utf-8')) if os.path.exists(OVERRIDES) else {}
rules = ov.get('reguly', {})
touched = set()

for rid, fields in ov.get('set', {}).items():
    if rid not in by_id:
        errors.append(f'set: brak wiersza {rid}')
        continue
    for k, v in fields.items():
        if k not in FIELDS:
            errors.append(f'set: nieznane pole {k} w {rid}')
            continue
        by_id[rid][k] = v
    touched.add(rid)

for rid, reps in ov.get('replace', {}).items():
    if rid not in by_id:
        errors.append(f'replace: brak wiersza {rid}')
        continue
    for rep in reps:
        pole, old, new = rep['pole'], rep['stare'], rep['nowe']
        cnt = by_id[rid][pole].count(old)
        if cnt != 1:
            errors.append(f'replace: {rid}.{pole}: fragment występuje {cnt} razy: {old[:60]!r}')
            continue
        by_id[rid][pole] = by_id[rid][pole].replace(old, new)
    touched.add(rid)

appended = []
for a in ov.get('append', []):
    if a['id'] in by_id:
        errors.append(f'append: ID {a["id"]} już istnieje')
        continue
    r = {'id': a['id'], **{k: a.get(k, '') for k in FIELDS}}
    rows.append(r)
    by_id[r['id']] = r
    appended.append(r['id'])

# Reguła: wpis typu „hipoteza” (wiedza modelu lub wniosek bez źródła) ma pewność najwyżej „niska”.
cap = rules.get('hipoteza_max_pewnosc')
lowered = []
if cap:
    for r in rows:
        if r['typ'].strip().lower().startswith('hipoteza') and \
                CONF_RANK.get(r['pewnosc'], -1) > CONF_RANK[cap]:
            r['pewnosc'] = cap
            lowered.append(r['id'])

no_cut_prefixes = tuple(rules.get('bez_skracania_prefiksy', []))

lines = []
for r in rows:
    full = r['id'] in touched or r['id'].startswith(no_cut_prefixes)
    claim = r['tresc'] if full else cut(r['tresc'], CUT_CLAIM)
    nums = r['liczby'] if full else cut(r['liczby'], CUT_NUMS)
    srcs = ' ; '.join(s.strip() for s in r['zrodla'].split('; '))
    lines.append('| ' + ' | '.join(clean(x) for x in [r['id'], claim, nums, r['typ'], r['pewnosc'], srcs]) + ' |')

# ---------- część opisowa: znaczniki liczone z CSV ----------
_csv_cache = {}


def load_csv(name):
    if name not in _csv_cache:
        path = os.path.join(RESEARCH, name)
        with open(path, encoding='utf-8', newline='') as f:
            _csv_cache[name] = list(csv.DictReader(f))
    return _csv_cache[name]


def col(name, column):
    data = load_csv(name)
    if data and column not in data[0]:
        raise KeyError(f'brak kolumny {column!r} w {name}')
    return [d[column] for d in data]


def token(m):
    body = m.group(1)
    try:
        if body == 'register_rows':
            return str(len(rows))
        kind, rest = body.split(':', 1)
        if kind == 'rows':
            return str(len(load_csv(rest)))
        name, spec = rest.split(':', 1)
        if kind == 'n':
            conds = [c.split('=', 1) for c in spec.split('&&')]
            if any(len(c) != 2 for c in conds):
                raise ValueError('warunek bez „=”')
            for column, _ in conds:
                col(name, column)  # sprawdza, czy kolumna istnieje
            n = sum(1 for d in load_csv(name) if all(d[c] == v for c, v in conds))
            if n == 0:
                warnings.append(f'znacznik {body!r} daje 0')
            return f'{n:,}'.replace(',', ' ')
        if kind == 'nonempty':
            return str(sum(1 for v in col(name, spec) if v.strip()))
        if kind == 'distinct':
            return str(len({v for v in col(name, spec) if v.strip()}))
    except (KeyError, ValueError, FileNotFoundError) as e:
        errors.append(f'znacznik {body!r}: {e}')
        return m.group(0)
    errors.append(f'nieznany znacznik {body!r}')
    return m.group(0)


head = open(HEAD, encoding='utf-8').read()
head = re.sub(r'\{\{([^{}]+)\}\}', token, head)
if '{{' in head:
    errors.append('w części opisowej zostały nierozwinięte znaczniki {{…}}')

text = head + '\n'.join(lines) + '\n'

# ---------- kontrole ----------
# 1. Tabele markdown: każdy wiersz bloku ma tyle samo kolumn co nagłówek.
def ncols(line):
    return len(re.findall(r'(?<!\\)\|', line)) - 1


block = []
for i, line in enumerate(text.split('\n') + [''], 1):
    if line.startswith('|'):
        block.append((i, line))
        continue
    if block:
        want = ncols(block[0][1])
        if len(block) < 2 or not re.match(r'^\|(\s*:?-{3,}:?\s*\|)+\s*$', block[1][1]):
            errors.append(f'tabela od linii {block[0][0]}: brak wiersza separatora')
        for ln, l in block:
            if ncols(l) != want:
                errors.append(f'linia {ln}: {ncols(l)} kolumn zamiast {want}')
        block = []

# 2. Wpisy E-REV w tabeli części opisowej = wpisy dopisane do rejestru.
head_rev = sorted(set(re.findall(r'^\| (E-REV-\d\d) \|', head, flags=re.M)))
if head_rev != sorted(a for a in appended if a.startswith('E-REV-')):
    errors.append(f'E-REV w części opisowej {head_rev} ≠ dopisane {appended}')

# 3. Odwołania E-… w części opisowej i w tekstach poprawek muszą istnieć w rejestrze
#    (w surowych wierszach rejestru tylko ostrzeżenie).
REF = r'\bE-[A-Z]+[0-9]?-(?:C)?\d+\b'
ids = {r['id'] for r in rows}
ov_text = json.dumps({k: ov.get(k) for k in ('set', 'replace', 'append')}, ensure_ascii=False)
for where, src in (('części opisowej', head), ('poprawkach', ov_text)):
    for ref in sorted(set(re.findall(REF, src))):
        if ref not in ids:
            errors.append(f'odwołanie {ref} w {where} nie istnieje w rejestrze')
for r in rows:
    for ref in set(re.findall(REF, r['tresc'] + ' ' + r['liczby'])):
        if ref not in ids:
            warnings.append(f'wiersz {r["id"]}: odwołanie {ref} nie istnieje w rejestrze')

# 4. Sformułowania sprzeczne z kanonem (ostrzeżenie).
low = text.lower()
for p in FORBIDDEN:
    if p.lower() in low:
        warnings.append(f'sformułowanie do sprawdzenia: {p!r}')
head_low = head.lower()
for p in STALE:
    if p.lower() in head_low:
        warnings.append(f'nieaktualna liczba lub sformułowanie w części opisowej: {p!r}')

if errors:
    print('BŁĘDY:', *errors, sep='\n  ')
    sys.exit(1)

open(OUT, 'w', encoding='utf-8').write(text)
print(f'wiersze rejestru: {len(lines)} (z czego dopisane: {len(appended)}: {", ".join(appended)})')
print(f'poprawione wiersze: {len(touched)}: {", ".join(sorted(touched))}')
print(f'hipotezy obniżone do „{cap}”: {len(lowered)}: {", ".join(lowered)}')
for w in warnings:
    print('UWAGA:', w)
