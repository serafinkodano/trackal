"""Generate finalist cards (markdown) from longlist + audit + wave2b refute/demand outputs."""
import json, os, sys
TOP10 = sys.argv[1].split(',')
ll = {x['final_id']: x for x in json.load(open('raw/longlist.json'))}
CAL = json.load(open('raw/calibration.json'))
FS = json.load(open('raw/final_status.json'))
W = [('demand', 'Dowody popytu', 20), ('gap', 'Luka zintegrowanego produktu', 20), ('ai_distribution', 'Potencjał dystrybucji AI', 15),
     ('ad_potential', 'Potencjał reklamowy', 15), ('feasibility', 'Wykonalność i koszt utrzymania', 10),
     ('reliability', 'Wiarygodność obliczeń i ryzyko', 10), ('shared_engine', 'Współdzielenie silników', 10)]
LV = {'low': 'niska', 'medium': 'średnia', 'high': 'wysoka'}
TYP = {'direct': 'bezpośredni', 'partial': 'częściowy', 'substitute': 'substytut', 'probably_direct_unverified': 'prawdopodobnie bezpośredni (niezweryfikowane)'}


def one(s, n=700):
    s = ' '.join(str(s).split())
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' …'


def load(p):
    return json.load(open(p)) if os.path.exists(p) else None


out = []
for rank, fid in enumerate(TOP10, 1):
    x = ll[fid]; a = load(f'raw/audit_{fid}.json'); r = load(f'raw/refute_{fid}.json'); d = load(f'raw/demand_{fid}.json')
    c = CAL[fid]
    out.append(f"### {rank}. {fid} — {FS.get(fid, {}).get('name') or x['name_en']}\n")
    out.append(f"**Rodzina:** {x['family_pl']} · **Ocena ważona:** agent {c['agent']:.2f} → po kalibracji **{c['cal']:.2f}** / 5 · **Status:** {c['status']}\n")
    if c.get('note'):
        out.append(f"> {c['note']}\n")
    out.append(f"- **Użytkownik i moment potrzeby:** {one(x['user_and_moment'], 400)}")
    out.append(f"- **Przykładowe pytanie:** *{one(x['sample_prompt_en'], 400)}*")
    out.append(f"- **Problem decyzyjny:** {one(x['decision_problem'], 900)}")
    out.append(f"- **Warianty:** {one(x['variants_compared'], 700)}")
    out.append(f"- **Kluczowe zależności:** {one(x['key_dependencies'], 800)}")
    out.append(f"- **Główne wyniki:** {one(x['main_outputs'], 600)}")
    out.append(f"- **Powód wejścia na zewnętrzną stronę:** {one(x['reason_external_site'], 500)}\n")
    out.append("**Konkurencja (audyt fali 2 + próba obalenia w fali 2b; strony nieotwierane, dowód: search-summary):**\n")
    out.append("| Narzędzie | Typ | Co pokrywa | Czego brak / co niezweryfikowane |\n|---|---|---|---|")
    if a:
        for comp in a['competitors'][:10]:
            out.append(f"| [{one(comp['name'], 60)}]({comp['url']}) | {TYP[comp['type']]} | {one(comp['covers_pl'], 220)} | {one(comp['misses_or_unverified_pl'], 220)} |")
    if r:
        for cand in r['candidates'][:6]:
            out.append(f"| [{one(cand['name'], 60)}]({cand['url']}) (fala 2b) | {TYP[cand['classification']]} | {one(cand['evidence_pl'], 220)} | do ręcznej weryfikacji: {one(cand['what_to_check_manually_pl'], 200)} |")
    out.append("")
    if a:
        out.append(f"**Luka (audyt):** {one(a['gap_statement_pl'], 1100)}\n")
    if r:
        out.append(f"**Próba obalenia (fala 2b):** {'ZNALEZIONO konkurenta bezpośredniego. ' if r['direct_competitor_found'] else ''}{one(r['conclusion_pl'], 900)} *Zakres:* {one(r['search_scope_pl'], 300)} *Pewność:* {LV[r['confidence']]}.\n")
    out.append("**Ocena kryteriów** (1–5; wyżej = lepiej / łatwiej / mniejsze ryzyko):\n")
    out.append("| Kryterium (waga) | Ocena | Uzasadnienie | Dowody | Luki | Pewność |\n|---|---|---|---|---|---|")
    if a:
        for k, label, w in W:
            s = a['scores'][k]
            adj = c.get('adj', {}).get(k)
            sc = f"{s['score']}" + (f" → **{adj}**" if adj is not None else '')
            out.append(f"| {label} ({w}%) | {sc} | {one(s['rationale_pl'], 300)} | {one(s['evidence_pl'], 260)} | {one(s['gaps_pl'], 200)} | {LV[s['confidence']]} |")
    out.append("")
    if d:
        out.append("**Popyt (fala 2b):**\n")
        for e in d['demand_evidence'][:6]:
            kind = {'direct': 'bezpośrednie', 'indirect': 'pośrednie', 'estimate': 'estymacja', 'hypothesis': 'hipoteza'}[e['kind']]
            out.append(f"- [{kind}] {one(e['claim_pl'], 300)} (mierzy: {one(e['measures_pl'], 120)}) — {e['url']}")
        if d['forum_question_examples']:
            out.append("- Przykłady pytań z forów (parafrazy): " + '; '.join(f"*{one(q['paraphrase_en'], 160)}* ({q['url']})" for q in d['forum_question_examples'][:4]))
        out.append(f"- Sezonowość / wyzwalacze: {one(d['seasonality_or_triggers_pl'], 400)}\n")
        out.append("**Prompty testowe (do przyszłego testu; wyników NIE symulowano):**\n")
        out.append("*Bez prośby o narzędzie:*")
        out += [f"{i}. {p}" for i, p in enumerate(d['prompts_no_tool_request'], 1)]
        out.append("\n*Z prośbą o kalkulator:*")
        out += [f"{i}. {p}" for i, p in enumerate(d['prompts_calculator_request'], 1)]
        out.append("\n*Z prośbą o porównanie scenariuszy:*")
        out += [f"{i}. {p}" for i, p in enumerate(d['prompts_scenario_comparison'], 1)]
        out.append("")
        out.append(f"**Ryzyko, że asystent rozwiąże sam:** {one(d['ai_self_solve_assessment_pl'], 700)}\n")
        out.append(f"**Zależności, które asystent prawdopodobnie pominie:** {one(d['missing_dependencies_ai_likely_ignores_pl'], 600)}\n")
        out.append(f"**MVP:** {one(d['mvp_scope_pl'], 800)}\n")
        out.append(f"**Świadomie odłożone:** {one(d['deferred_features_pl'], 500)}\n")
        out.append(f"**Dane i testy obliczeń:** {one(d['data_sources_and_tests_pl'], 700)}\n")
        out.append(f"**Kontrola ekspercka:** {one(d['expert_review_pl'], 500)}\n")
    out.append(f"**Ryzyko merytoryczne:** {LV[x['content_risk']]} · **Trudność implementacji:** {LV[x['impl_difficulty']]} · **Utrzymanie:** {LV[x['maintenance_burden']]} · **Otoczenie reklamowe:** {one(x['ad_environment'], 300)}\n")
    out.append('---\n')
open('raw/cards.md', 'w').write('\n'.join(out))
print('cards', len(TOP10), sum(len(l) for l in out))
