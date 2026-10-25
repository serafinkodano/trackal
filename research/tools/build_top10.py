"""Składa research/top-10-products.md.

Kolejność: top10_head.md (z tabelą selekcji do audytu fali 2 wstawianą w miejsce znacznika) + tabela rankingu 25
(liczona tu z raw/calibration.json, statusy z product-opportunities.csv) + top10_rankings.md, w który w miejsce
znacznika §2a wstawiane są uzasadnienia per kryterium dla 15 propozycji spoza finału + karty finalistów
(tools/build_cards.py). Uruchamiać z katalogu scratchpad: python3 tools/build_top10.py
"""
import json, os, re, sys
from collections import Counter

sys.dont_write_bytecode = True  # nie zostawiać tools/__pycache__/build_cards*.pyc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import build_cards as bc  # noqa: E402

cal = json.load(open('raw/calibration.json'))
ll = {x['final_id']: x for x in json.load(open('raw/longlist.json'))}
fs = json.load(open('raw/final_status.json'))
PR = bc.products_csv()
K = ['demand', 'gap', 'ai_distribution', 'ad_potential', 'feasibility', 'reliability', 'shared_engine']

# Finaliści (etap D/E). Reguła wyboru i odstępstwa od rankingu: §1.4 w top10_head.md.
# Karty w §4 są układane w kolejności pozycji w rankingu §2 (recenzja spójności, decisions#11).
TOP10 = ['RENO-02', 'RENO-03', 'RENO-04', 'HOME-02', 'LIFE-01', 'HOME-04', 'INS-03', 'CARE-01', 'AUTO-01', 'FIN-01']
MERGED = {'RENO-01': 'RENO-02'}  # gałęzie, które nie liczą się jako odrębne propozycje (kanon K4)

# Reguła odrębności (kanon K4; architecture-and-validation.md §2): wyjaśnienie dopisywane w nawiasie kwadratowym do kolumny
# „Uwaga do statusu” tam, gdzie tekst z CSV („gałąź”, „moduł”, „ten sam silnik”) mógłby sugerować, że pomysł nie jest odrębny.
DISTINCT_NOTE = {
    'ENER-01': '[odrębna decyzja: forma własności PV — gotówka, kredyt, leasing, PPA; z RENO-02 dzieli tylko moduł PV]',
    'INS-01': '[odrębna decyzja: zgłosić szkodę czy zapłacić samemu (dom i auto); RENO-02 korzysta tylko z progu zgłoszenia szkody]',
    'AUTO-03': '[odrębna decyzja: naprawa vs wymiana po awarii; z AUTO-01 dzieli silnik]',
}

# Dlaczego propozycja spoza finału nie weszła do finału (jedno zdanie; źródło: uwaga_statusu i uzasadnienie_statusu w CSV).
NOT_FINAL = {
    'RENO-01': 'Po audycie scalony z RENO-02 jako opcjonalna gałąź PV (przełącznik PV jest w MVP RENO-02), więc nie jest odrębną propozycją.',
    'INS-01': ('Luka 2/5: rdzeń rachunku „zgłosić szkodę czy zapłacić” pokrywają darmowe kalkulatory częściowe (Calcbee, AdvoraHQ, Toolzie). '
               'To odrębna decyzja (dom i auto); RENO-02 korzysta tylko z progu zgłoszenia szkody jako modułu.'),
    'RENT-01': 'Rodzina wynajmu jest ograniczona do wąskich momentów (właściciel podejmuje tę decyzję zwykle raz, wymaga CPA), a klasyfikacja najbliższych narzędzi (BiggerPockets Sell vs Keep, OverlineIQ) jest sporna.',
    'HOME-03': 'Remis 3,30 z AUTO-01 i AUTO-02; FairOffer i kalkulatory lead-gen pokrywają rdzeń „fix vs as-is vs cash”, a kolejność w rodzinie HOME ustalono po HOME-04 i HOME-02.',
    'AUTO-02': 'Remis 3,30 z AUTO-01; korzysta z tego samego silnika, więc ma sens dopiero po wyniku AUTO-01 (produkt nr 10).',
    'FIN-02': 'Wykonalność i wiarygodność 2/5 (warunki HEI i HECM są niestandaryzowane i wymagają ręcznej aktualizacji).',
    'ENER-03': 'Luka obniżona w kalibracji do 2/5, bo Home Energy Planner ma klasyfikację sporną (fala 1: bezpośredni, fala 2: częściowy), a popyt jest epizodyczny.',
    'AUTO-03': 'Luka 2/5. To odrębna decyzja (naprawa vs wymiana auta po awarii), ale korzysta z silnika AUTO-01, więc ma sens dopiero po wyniku AUTO-01.',
    'HLTH-02': 'Zdrowie jest poza granicą domeny (`architecture-and-validation.md` §1.2); ewentualny tani test na healthscorer.com, nie na nowej domenie.',
    'HOME-01': 'Luka 2/5: sum.money i kalkulatory bridge/HELOC pokrywają większość sekwencji „kup przed sprzedażą”.',
    'JOB-02': 'Poza granicą domeny (`architecture-and-validation.md` §1.2); Calcuja Golden Handcuff Calculator pokrywa kluczowy fragment (koszt odejścia).',
    'BIZ-04': ('Publiczność B2B słabo pasuje do AdSense, a znaczną część problemu pokrywają płatne narzędzia (Cogsy, 8fig, Float). E-commerce jest poza domeną; '
               'ewentualny test w istniejącym serwisie e-commerce właściciela, osobna domena dopiero po spełnieniu warunków 3 i 4 (`architecture-and-validation.md` §1.2).'),
    'ENER-01': ('Luka 2/5 i AI 2/5 przy czasowym oknie 48E. To odrębna decyzja (forma własności PV: gotówka, kredyt, leasing, PPA), '
                'ale może korzystać z modułu PV z RENO-02, dlatego status „później”.'),
    'RET-03': 'Znaleziono konkurentów bezpośrednich (RothHelper, QuantCalc ACA Bridge Optimizer; search-summary, pewność średnia).',
    'BIZ-01': ('Publiczność B2B, gęste treści dostawców 3PL i coroczne zmiany opłat Amazon. E-commerce jest poza domeną; ewentualny test w istniejącym '
               'serwisie e-commerce właściciela, osobna domena dopiero po spełnieniu warunków 3 i 4 (`architecture-and-validation.md` §1.2).'),
}

# Selekcja 100 → 25: pomysły ze statusem „zbadać” (CSV), które nie trafiły do audytu fali 2, z powodem pominięcia.
# Powody to rekonstrukcja z uzasadnień fali 1 (kolumny uzasadnienie_statusu, uwagi_scalenia_i_bliskie_duplikaty).
SKIPPED = {
    'FIN-05': 'W rodzinie FIN pierwszeństwo dostały FIN-01 i FIN-02 z lepiej opisanymi dowodami; FIN-05 korzysta z tego samego silnika finansowania, a jego konkurencji w fali 1 nie zbadano.',
    'INS-06': ('Nie jest odrębnym pomysłem: to gałąź ENER-03 (pompa sump to jedno z obciążeń zasilania awaryjnego), a nie osobny produkt; '
               'w fali 1 nie zebrano też dowodów popytu. Dlatego nie jest kandydatem do kolejnego audytu.'),
    'AUTO-04': ('W rodzinie AUTO wybrano trzy pomysły z wyraźniejszym momentem decyzji (AUTO-01–03); popyt na AUTO-04 opisano tylko hipotezą. '
                'Odrębny pomysł z domeny B — następny kandydat do audytu (25. pozycja rankingu).'),
    'JOB-03': 'Popytu na powroty do biur w 2026 i konkurencji nie zweryfikowano (limit wyszukiwań), trudność implementacji jest wysoka, a rodzina JOB jest poza granicą domeny (`architecture-and-validation.md` §1.2).',
    'JOB-07': 'Ubezpieczenie zdrowotne jest poza granicą domeny, a ryzyko błędu i koszt utrzymania (składki ACA według ZIP, niepewne dopłaty 2026–2027) są wysokie.',
    'JOB-08': 'Wysoka trudność i ryzyko (stanowe reguły zasiłku dla bezrobotnych), rodzina poza granicą domeny; z rodziny JOB audytowano JOB-02.',
    'JOB-11': 'Gęsta konkurencja częściowa kalkulatorów S-corp, koszt przeglądu CPA i bliskość samodzielnego planowania podatku dochodowego, wyłączonego z zakresu (`architecture-and-validation.md` §1.2).',
    'RET-04': 'Wymaga przeglądu aktuarialnego (wysokie ryzyko merytoryczne), a popytu i konkurencji nie zweryfikowano; z rodziny RET audytowano RET-03.',
    'RET-05': 'Wysoki koszt danych lokalnych (podatki od nieruchomości, ubezpieczenia) i wysoka trudność implementacji; z rodziny RET audytowano RET-03.',
    'RET-06': 'Asystenci znają regułę 10 lat, planery mogą ją już modelować, a produkt jest w praktyce planowaniem podatku dochodowego, wyłączonym z zakresu (`architecture-and-validation.md` §1.2).',
    'CARE-03': 'Koszty ADU są silnie lokalne, a w fali 1 znaleziono tylko moduły częściowe; z rodziny CARE audytowano szerszy CARE-01.',
    'CARE-04': ('Ten sam silnik co LIFE-01, ale inna decyzja (dom rodzica przed jego śmiercią: Medicaid, brak step-up, darowizna), więc odrębny pomysł; '
                'wysokie ryzyko prawne (Medicaid). Z tego silnika audytowano LIFE-01.'),
    'BIZ-02': 'Wysoka zmienność przepisów celnych (koszt utrzymania) i publiczność B2B słabo pasująca do AdSense.',
    'BIZ-05': ('Obejmuje BIZ-06 jako wariant (BIZ-06 nie liczy się osobno); treść finansowa YMYL z pokusą lead-genu pożyczkowego. '
               'Z rodziny BIZ audytowano BIZ-01 i BIZ-04.'),
    'BIZ-10': 'Popyt nieznany (brak danych w fali 1) i ryzyko, że użytkownik woli arkusz; publiczność B2B.',
    'BIZ-12': 'Konkurencji i popytu nie zweryfikowano w fali 1; publiczność B2B słabo pasuje do AdSense.',
    'BIZ-13': 'Mała populacja i brak weryfikacji w fali 1; publiczność B2B.',
    'BIZ-14': 'Popytu i konkurencji nie zweryfikowano w fali 1; wąska publiczność B2B.',
    'BIZ-16': 'Zależność od jednej platformy, której opłaty zmieniają się co najmniej raz w roku, i ryzyko, że Seller Central podaje tę rekomendację natywnie.',
    'HLTH-01': 'Rdzeń jest zatłoczony przez kalkulatory HDHP/PPO 2025–2026, a zdrowie jest poza granicą domeny; z rodziny HLTH audytowano HLTH-02.',
    'LIFE-02': ('Wysokie ryzyko treści i koszt eksperta (CDFA). Z LIFE-01 dzieli moduł wykupu współwłaściciela, ale decyzja jest inna '
                '(rozwód: QDRO, refinansowanie, §1041), więc to odrębny pomysł; audytowano LIFE-01.'),
    'LIFE-04': 'Rdzeń porównania ofert uczelni jest zatłoczony narzędziami rządowymi i komercyjnymi, popyt jest silnie sezonowy, a finansowanie studiów jest poza granicą domeny.',
}

dec = bc.dec


def name_of(fid, n=None):
    nm = fs.get(fid, {}).get('name') or ll[fid]['name_en']
    if n and len(nm) >= n:
        nm = nm[:n - 3].rstrip() + '…'
    return nm.replace('|', '/')


def competitor_cell(row):
    v = row['bezposredni_konkurent (top 25)']
    if v.startswith('Nie znaleziono'):
        m = re.search(r'pewność ([^)]*)\)', v)
        return f"nie znaleziono w badanym zakresie (pewność {m.group(1) if m else 'niska–średnia'})"
    if v.startswith('sporny'):
        who = v.split(':', 1)[1].split('—')[0].strip() if ':' in v else ''
        return f"sporny ({who}; do ręcznej weryfikacji)"
    if v.startswith('tak'):
        return 'tak: RothHelper, QuantCalc ACA Bridge Optimizer (pewność średnia)'
    return v


# ---------- §2: tabela rankingu ----------
order = sorted(cal.items(), key=lambda kv: (-round(kv[1]['cal'], 2), -round(kv[1]['agent'], 2)))
rows, pos, position = [], 0, {}
for fid, c in order:
    a = json.load(open(f'raw/audit_{fid}.json'))
    row = PR[fid]
    cells = []
    for k in K:
        orig = a['scores'][k]['score']; new = c['scores'][k]
        cells.append(f"**{new}**" if new != orig else str(new))
    if fid in MERGED:
        num = '—'
        prod = f"{name_of(fid)} — **scalony → {MERGED[fid]}, nie liczy się**"
    else:
        pos += 1; num = str(pos)
        prod = name_of(fid)  # pełna nazwa robocza jak w CSV (bez ucinania)
    position[fid] = num
    note = row['uwaga_statusu'].replace('|', '/')
    if fid in DISTINCT_NOTE and 'odrębn' not in note:
        note += f" {DISTINCT_NOTE[fid]}"
    rows.append(f"| {num} | {fid} | {prod} | " + ' | '.join(cells) +
                f" | {dec(c['agent'])} | **{dec(c['cal'])}** | {row['poziom_pewnosci (oceny/statusu)']} | {competitor_cell(row)} | "
                f"{row['status']} | {note} |")
assert pos == 24, pos

# ---------- §1.3: tabela selekcji do audytu fali 2 (z długiej listy → 25) ----------
skipped = [r for r in PR.values() if r['status'] == 'zbadać' and not r['ocena_agenta_0_5 (top 25)'].strip()]
missing = [r['ID'] for r in skipped if r['ID'] not in SKIPPED]
assert not missing, f'brak powodu pominięcia dla: {missing}'
sel = ['| ID | Pomysł | Rodzina | Weryfikacja przed audytem (CSV) | Powód pominięcia w selekcji do audytu (rekonstrukcja) |', '|---|---|---|---|---|']
for r in skipped:
    ver = 'koncepcyjny' if r['poziom_weryfikacji'].startswith('koncepcyjny') else 'wstępnie sprawdzony (search-summary)'
    nm = r['nazwa_robocza_en'].replace('|', '/')  # pełna nazwa (bez ucinania)
    idn = r['ID'] + ('' if r['odrebny_pomysl'].startswith('tak') else ' (nie jest odrębny)')
    sel.append(f"| {idn} | {nm} | {r['rodzina']} | {ver} | {SKIPPED[r['ID']]} |")
n_nd = sum(1 for r in skipped if not r['odrebny_pomysl'].startswith('tak'))
distinct = [r for r in PR.values() if r['odrebny_pomysl'].startswith('tak')]
st = Counter(r['status'] for r in distinct)
assert (len(PR), len(distinct), st['pilot'], st['zbadać'], st['później'], st['odrzucić']) == (96, 92, 5, 27, 35, 25), (len(PR), len(distinct), st)
assert n_nd == 1
sel_md = '\n'.join(sel) + (f"\n\nWierszy ze statusem „zbadać” poza audytem fali 2: {len(skipped)} (status końcowy z `product-opportunities.csv`), "
                           f"w tym {n_nd} nieodrębny (INS-06, gałąź ENER-03), czyli {len(skipped) - n_nd} odrębnych pomysłów. "
                           f"Statusy wszystkich {len(distinct)} odrębnych pomysłów: pilot {st['pilot']}, zbadać {st['zbadać']}, później {st['później']}, odrzucić {st['odrzucić']}.\n")

# ---------- §2a: uzasadnienia per kryterium dla 15 propozycji spoza finału ----------
s2a = ['## 2a. Uzasadnienia per kryterium dla 15 propozycji spoza top 10', '',
       'Źródło: audyty fali 2 (`audit_<ID>`; 7 zapytań WebSearch na produkt, wyłącznie streszczenia wyszukiwarki, strony nieotwierane) i kalibracja. '
       'Teksty uzasadnień, dowodów i luk to pełne zapisy audytu (bez skrótów), z poprawkami słownictwa z fali 3: podaż treści i liczba zdarzeń to nie popyt, '
       'twierdzenia o zachowaniu asystentów to hipotezy, a funkcji na nieotwartych stronach nie nazywamy „brakiem”. '
       'Pełny zapis konkurentów: `competitor-audit.csv`, kolumna `produkt_ID_final`. '
       'Pewność kryteriów „popyt”, „potencjał reklamowy” i „dystrybucja AI” jest ograniczona do „niska” (powód w kolumnie „Luki” i w §1.2); '
       'w nawiasie pewność nadana przez audytora. **Bezpośrednie dowody popytu online (wolumeny wyszukiwań lub promptów): 0 dla każdej z tych propozycji.**', '']
kind_pl = {'direct': 'bezpośrednie', 'indirect': 'pośrednie', 'estimate': 'estymacja', 'hypothesis': 'hipoteza'}
for fid, c in order:
    if fid in TOP10:
        continue
    a = json.load(open(f'raw/audit_{fid}.json')); row = PR[fid]
    cnt = Counter(s['evidence_type'] for s in a['demand_signals'])
    cnt_txt = ', '.join(f"{kind_pl[k]}: {cnt[k]}" for k in ('direct', 'indirect', 'estimate', 'hypothesis') if cnt[k])
    label = f"poz. {position[fid]}" if position[fid] != '—' else f"bez numeru; scalony → {MERGED.get(fid)}, nie liczy się"
    s2a.append(f"### {fid} ({label}) — {name_of(fid)}")
    s2a.append('')
    s2a.append(f"**Ocena:** agent {dec(c['agent'])} → po kalibracji **{dec(c['cal'])}** · **Status (CSV):** {bc.status_text(row)} · "
               f"**Pewność oceny/statusu:** {row['poziom_pewnosci (oceny/statusu)']} · **Rekomendacja audytora:** {a['recommendation']}")
    s2a.append('')
    s2a.append(f"- **Konkurent bezpośredni:** {bc.competitor_line(row)}.")
    s2a.append(f"- **Dlaczego nie w finale:** {NOT_FINAL[fid]}")
    s2a.append(f"- **Sygnały popytu w audycie:** {len(a['demand_signals'])} ({cnt_txt}; etykiety według siły źródła). "
               f"Żaden nie jest wolumenem wyszukiwań ani promptów" +
               ("; „bezpośrednie” oznacza tu np. wątek forum z pytaniem albo dane pierwotne o zdarzeniach, a nie pomiar popytu." if cnt['direct'] else '.'))
    if c.get('note'):
        note = re.sub(r'^Kalibracja:\s*', '', c['note'])
        s2a.append(f"- **{'Scalenie' if fid in MERGED else 'Kalibracja'}:** {note}")
    s2a.append('')
    s2a.append('| Kryterium (waga) | Ocena | Uzasadnienie | Dowód (wg audytu) | Luki | Pewność |\n|---|---|---|---|---|---|')
    s2a += bc.criteria_rows(a, c)
    s2a.append('')
s2a_md = '\n'.join(s2a) + '\n'

# ---------- składanie ----------
cards = bc.main(sorted(TOP10, key=lambda f: int(position[f])), position)
head = open('top10_head.md').read()
assert '<!-- selekcja-tabela -->' in head
head = head.replace('<!-- selekcja-tabela -->', sel_md.rstrip('\n'))
rk = open('top10_rankings.md').read()
assert '<!-- §2a -->' in rk
rk = rk.replace('<!-- §2a -->', s2a_md.rstrip('\n'))
doc = head + '\n'.join(rows) + '\n' + rk + cards
open('/home/user/trackal/research/top-10-products.md', 'w').write(doc)
print('written', len(doc))
