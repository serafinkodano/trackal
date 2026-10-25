"""Scenario model for an ad-funded US decision-simulator site.

Generates research/economics.csv. Every input is an ASSUMPTION unless the
`basis` column cites a source documented in research/evidence-and-assumptions.md.
Run: python3 research/tools/economics_model.py
"""
import csv
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "economics.csv"
SCEN = ["conservative", "base", "optimistic"]

# (key, label_pl, unit, {scenario: value}, basis)
INPUTS = [
    # --- revenue per session -------------------------------------------------
    ("page_rpm_us", "Page RPM wydawcy (AdSense, netto po udziale Google) dla ruchu z USA na stronach narzędzi finanse/dom",
     "USD / 1000 odsłon", {"conservative": 2.4, "base": 8.0, "optimistic": 18.0},
     "ZAŁOŻENIE; brak danych pierwotnych dla stron-narzędzi. Zakresy vendorskie bez metodologii (E-ADS-11; mediana ok. 2,4 USD z 75 stawek). Most CPM→RPM niżej jako test spójności. Rozstrzygnie pilotaż (K-06, krok 1b G0)"),
    ("non_us_rpm_factor", "RPM ruchu spoza USA jako ułamek RPM USA", "ułamek",
     {"conservative": 0.20, "base": 0.25, "optimistic": 0.35}, "ZAŁOŻENIE (E-ADS-16: tier-1 vs reszta świata)"),
    ("us_share", "Udział sesji z USA wśród sesji ludzi", "ułamek",
     {"conservative": 0.60, "base": 0.75, "optimistic": 0.85}, "ZAŁOŻENIE (serwis anglojęzyczny, treści USA)"),
    ("pages_per_session", "Odsłony na sesję (narzędzie + metodologia/wyniki)", "odsłony / sesję",
     {"conservative": 1.1, "base": 1.3, "optimistic": 1.6},
     "ZAŁOŻENIE: publicznych benchmarków dla stron-narzędzi nie znaleziono; analogia do landing pages 1-1,5 PV/sesję (E-ADS-26); AdSense nie odświeża reklam po przeliczeniu (E-VER-C7)"),
    ("adblock_rate", "Udział odsłon z zablokowanymi reklamami (adblock)", "ułamek",
     {"conservative": 0.25, "base": 0.20, "optimistic": 0.15}, "ZAŁOŻENIE (E-ADS-17: 19-33% zależnie od metody; ankieta vs pomiar)"),
    ("rdp_share", "Udział odsłon z USA w trybie reklam niespersonalizowanych (GPC/RDP, stanowe prawo prywatności)", "ułamek",
     {"conservative": 0.15, "base": 0.10, "optimistic": 0.05}, "ZAŁOŻENIE; skala nieznana (E-ADS-19)"),
    ("rdp_rpm_factor", "RPM reklam niespersonalizowanych względem personalizowanych", "ułamek",
     {"conservative": 0.6, "base": 0.7, "optimistic": 0.8}, "ZAŁOŻENIE (E-ADS-35: testy bezciasteczkowe -30% do -36% CPM)"),
    ("unfilled_rate", "Udział niewypełnionych wyświetleń", "ułamek",
     {"conservative": 0.05, "base": 0.03, "optimistic": 0.02}, "ZAŁOŻENIE"),
    ("human_share", "Udział sesji ludzi w sesjach zarejestrowanych (po filtrach GA4)", "ułamek",
     {"conservative": 0.85, "base": 0.92, "optimistic": 0.97}, "ZAŁOŻENIE; boty i agenci AI nie są monetyzowani (E-ADS-22, E-ADS-23)"),
    # --- traffic structure ---------------------------------------------------
    ("ai_share_of_sessions", "Udział ruchu z asystentów AI w sesjach ludzi", "ułamek",
     {"conservative": 0.003, "base": 0.01, "optimistic": 0.05},
     "ZAŁOŻENIE zgodne z benchmarkami 0,1-1% (E-AI-02, E-VER-C5); obserwacja właściciela (10-30%) tylko jako wrażliwość niżej"),
    ("ai_rpm_factor", "RPM sesji z AI względem średniej (mobile, aplikacje, zaangażowanie)", "mnożnik",
     {"conservative": 0.8, "base": 1.0, "optimistic": 1.15}, "HIPOTEZA; brak danych pierwotnych o RPM ruchu AI"),
    # --- costs (monthly, cash) -----------------------------------------------
    ("cost_domain", "Domena", "USD / mies.", {"conservative": 2, "base": 1.5, "optimistic": 1.5}, "ZAŁOŻENIE (~18-24 USD/rok)"),
    ("cost_vps_cdn", "VPS + CDN + kopie", "USD / mies.", {"conservative": 60, "base": 30, "optimistic": 30}, "ZAŁOŻENIE"),
    ("cost_ai_tools", "Claude Code / API LLM (część przypisana projektowi)", "USD / mies.",
     {"conservative": 200, "base": 120, "optimistic": 100}, "ZAŁOŻENIE (subskrypcja + API)"),
    ("cost_data", "Płatne dane / API", "USD / mies.", {"conservative": 50, "base": 0, "optimistic": 0},
     "ZAŁOŻENIE: start na danych publicznych (NREL, EIA, FRED itp.; licencje do sprawdzenia, E-REG3-11, E-REG3-12)"),
    ("cost_seo_ai_monitoring", "Narzędzia SEO / monitoring AI", "USD / mies.",
     {"conservative": 150, "base": 50, "optimistic": 0}, "ZAŁOŻENIE; start na GSC/Bing WMT"),
    ("expert_hourly", "Stawka eksperta (EA/CPA/CFP/fachowiec)", "USD / h",
     {"conservative": 250, "base": 175, "optimistic": 125}, "ZAŁOŻENIE (do potwierdzenia ofertą, K-07)"),
    ("expert_hours_new_tool", "Godziny eksperta na nowy symulator", "h / narzędzie",
     {"conservative": 18, "base": 14, "optimistic": 11},
     "SZACUNEK agentów fali 2b dla 5 produktów pilotażowych (łącznie ok. 55-90 h); Z-16"),
    ("expert_hours_upkeep_tool_year", "Godziny eksperta na utrzymanie narzędzia rocznie", "h / narzędzie / rok",
     {"conservative": 4, "base": 2, "optimistic": 1}, "ZAŁOŻENIE"),
    ("owner_maint_hours_fixed", "Czas właściciela na utrzymanie: część stała", "h / mies.",
     {"conservative": 12, "base": 8, "optimistic": 6}, "ZAŁOŻENIE"),
    ("owner_maint_hours_per_tool", "Czas właściciela na utrzymanie: na każde żywe narzędzie", "h / narzędzie / mies.",
     {"conservative": 1.0, "base": 0.8, "optimistic": 0.6}, "ZAŁOŻENIE"),
    ("owner_hourly_value", "Wycena godziny właściciela (koszt alternatywny)", "USD / h",
     {"conservative": 50, "base": 40, "optimistic": 30}, "ZAŁOŻENIE"),
    ("owner_hours_new_tool", "Czas właściciela na zbudowanie symulatora z Claude Code (po zbudowaniu silnika)", "h / narzędzie",
     {"conservative": 53, "base": 45, "optimistic": 37}, "SZACUNEK z tabeli pilotażu (architecture-and-validation.md §3: 30-70 h/produkt)"),
    ("owner_hours_engine", "Jednorazowa budowa silnika, CI, szablonów, analityki", "h",
     {"conservative": 220, "base": 155, "optimistic": 90}, "SZACUNEK (architecture-and-validation.md §3: 90-220 h)"),
    ("owner_build_hours_month", "Godziny właściciela dostępne na budowę (po utrzymaniu)", "h / mies.",
     {"conservative": 40, "base": 60, "optimistic": 80}, "ZAŁOŻENIE o dostępności (ok. 10/15/20 h tygodniowo); wyznacza harmonogram"),
    ("one_time_legal", "Polityka prywatności, regulamin, CMP, audyt dostępności (jednorazowo)", "USD",
     {"conservative": 1500, "base": 600, "optimistic": 200}, "ZAŁOŻENIE"),
    # --- portfolio & traffic trajectory ----------------------------------------
    ("max_tools", "Docelowa liczba symulatorów w horyzoncie 36 mies. (limit planu)", "szt.",
     {"conservative": 5, "base": 15, "optimistic": 30}, "PLAN ilustracyjny; w praktyce zależny od reguł §4.3"),
    ("share_tools_with_traffic", "Udział narzędzi osiągających istotny ruch", "ułamek",
     {"conservative": 0.2, "base": 0.35, "optimistic": 0.5}, "ZAŁOŻENIE (rozkład potęgowy, nie liniowy)"),
    ("sessions_top_tool_mature", "Sesje/mies. najlepszego narzędzia po 12 mies. od publikacji", "sesje / mies.",
     {"conservative": 3000, "base": 15000, "optimistic": 60000}, "ILUSTRACJA, nie prognoza; brak wolumenów (K-04)"),
    ("zipf_s", "Wykładnik rozkładu ruchu między narzędziami z ruchem (Zipf)", "bezwymiarowy",
     {"conservative": 1.2, "base": 1.0, "optimistic": 0.9}, "ZAŁOŻENIE"),
    ("ramp_months", "Czas dojścia narzędzia do ruchu dojrzałego (liniowo, potem płasko)", "mies.",
     {"conservative": 12, "base": 12, "optimistic": 9}, "ZAŁOŻENIE; bez sezonowości popytu (zob. uwaga przy sezonowości)"),
    # --- RPM bridge (consistency check only) -----------------------------------
    ("bridge_slots_per_page", "Most CPM→RPM: sloty reklamowe dopuszczalne politykami na stronie-symulatorze", "szt. / odsłonę",
     {"conservative": 2.0, "base": 2.5, "optimistic": 3.0}, "ZAŁOŻENIE (E-ADS-02, E-ADS-03: brak reklam przy elementach interaktywnych)"),
    ("bridge_viewable_filled", "Most CPM→RPM: udział slotów widocznych i wypełnionych", "ułamek",
     {"conservative": 0.6, "base": 0.7, "optimistic": 0.8}, "ZAŁOŻENIE"),
    ("bridge_net_ecpm_us", "Most CPM→RPM: eCPM netto dla wydawcy (USA, finanse/dom)", "USD / 1000 wyświetleń",
     {"conservative": 2.0, "base": 4.5, "optimistic": 7.5}, "ZAŁOŻENIE; Search CPC reklamodawców (3,44 USD) i CPC GDN (0,86 USD) to inna warstwa (E-ADS-15)"),
]

SEASONALITY = {  # ad RPM multiplier; normalised to mean 1.0 below. ASSUMPTION (E-ADS-20)
    "Jan": 0.75, "Feb": 0.85, "Mar": 0.95, "Apr": 0.95, "May": 1.0, "Jun": 0.97,
    "Jul": 0.92, "Aug": 0.95, "Sep": 1.0, "Oct": 1.05, "Nov": 1.2, "Dec": 1.35,
}
_m = sum(SEASONALITY.values()) / 12
SEASONALITY = {k: v / _m for k, v in SEASONALITY.items()}
MONTHS = list(SEASONALITY)

TARGETS = [1000, 3000, 10000]
PREMIUM_UPLIFT = {"conservative": 1.2, "base": 1.5, "optimistic": 2.0}  # HYPOTHESIS
OWNER_AI_SHARE = {"conservative": 0.10, "base": 0.20, "optimistic": 0.30}  # owner's observation, unverified


def p(key, s):
    for k, _, _, vals, _ in INPUTS:
        if k == key:
            return vals[s]
    raise KeyError(key)


def monetised_factor(s):
    return (1 - p("adblock_rate", s)) * (1 - p("unfilled_rate", s)) * (1 - p("rdp_share", s) * (1 - p("rdp_rpm_factor", s)))


def human_session_rpm(s, ai_share=None):
    """Net ad revenue per 1000 HUMAN sessions (USD)."""
    ai = p("ai_share_of_sessions", s) if ai_share is None else ai_share
    blended = p("page_rpm_us", s) * (p("us_share", s) + (1 - p("us_share", s)) * p("non_us_rpm_factor", s))
    mix = 1 - ai + ai * p("ai_rpm_factor", s)
    return p("pages_per_session", s) * blended * monetised_factor(s) * mix


def session_rpm(s):
    """Net ad revenue per 1000 RECORDED sessions (USD) - includes non-monetised bots."""
    return human_session_rpm(s) * p("human_share", s)


def fixed_cash(s, tools):
    base = sum(p(k, s) for k in ["cost_domain", "cost_vps_cdn", "cost_ai_tools", "cost_data", "cost_seo_ai_monitoring"])
    return base + tools * p("expert_hours_upkeep_tool_year", s) * p("expert_hourly", s) / 12


def owner_maint_hours(s, tools):
    return p("owner_maint_hours_fixed", s) + p("owner_maint_hours_per_tool", s) * tools


def build_cost_cash(s):
    return p("expert_hours_new_tool", s) * p("expert_hourly", s)


def build_cost_owner(s):
    return p("owner_hours_new_tool", s) * p("owner_hourly_value", s)


def simulate(s, months=36):
    """Capacity-limited launch schedule + Zipf/ramp traffic. Returns monthly records (illustration)."""
    cap = p("owner_build_hours_month", s)
    queue = [("engine", p("owner_hours_engine", s))] + [("tool", p("owner_hours_new_tool", s))] * int(p("max_tools", s))
    qi, remaining = 0, queue[0][1]
    launches, traffic_rank, nrank = [], [], 0
    rpm = session_rpm(s)
    share, top, z, ramp = p("share_tools_with_traffic", s), p("sessions_top_tool_mature", s), p("zipf_s", s), p("ramp_months", s)
    recs = []
    for m in range(1, months + 1):
        hours, used, launched_now = cap, 0.0, 0
        while qi < len(queue) and hours > 1e-9:
            use = min(hours, remaining)
            hours -= use
            used += use
            remaining -= use
            if remaining <= 1e-9:
                if queue[qi][0] == "tool":
                    launches.append(m)
                    k = len(launches)
                    if math.ceil(k * share - 1e-9) > math.ceil((k - 1) * share - 1e-9):   # traffic tools spread evenly; tool 1 (best-chosen pilot) gets traffic
                        nrank += 1
                        traffic_rank.append(nrank)
                    else:
                        traffic_rank.append(None)
                    launched_now += 1
                qi += 1
                remaining = queue[qi][1] if qi < len(queue) else 0
        live = len(launches)
        sessions = sum(top / (rk ** z) * min(1.0, (m - lm) / ramp)
                       for lm, rk in zip(launches, traffic_rank) if rk is not None and m > lm)
        revenue = sessions * rpm / 1000 * SEASONALITY[MONTHS[(m - 1) % 12]]
        cash_cost = fixed_cash(s, live) + launched_now * build_cost_cash(s) + (p("one_time_legal", s) if m == 1 else 0)
        owner_cost = (owner_maint_hours(s, live) + used) * p("owner_hourly_value", s)
        recs.append(dict(m=m, live=live, sessions=sessions, revenue=revenue, cash_cost=cash_cost, owner_cost=owner_cost))
    return recs


ADDON_RPM = {"conservative": 0.002 * 10 * 1000, "base": 0.005 * 25 * 1000, "optimistic": 0.01 * 50 * 1000}
ADDONS = [
    ["addon_separate", "DODATEK (poza modelem bazowym): udział sesji kończących się kwalifikowaną konwersją u partnera (lead/wniosek)", "ułamek",
     0.002, 0.005, 0.01, "założenie", "ZAŁOŻENIE bez źródła; poza bazą z powodu ograniczenia właściciela"],
    ["addon_separate", "DODATEK: wypłata dla wydawcy za konwersję (po marży sieci)", "USD",
     10, 25, 50, "założenie", "ZAŁOŻENIE; ceny płacone przez kupujących leady: solar 25-250, ubezp. auto 8-80, home 6-18, refi 40-200 USD (E-ADS-33); wydawca dostaje mniej"],
    ["addon_separate", "DODATEK: przychód z lead-gen/afiliacji na 1000 sesji (hipoteza)", "USD / 1000 sesji",
     ADDON_RPM["conservative"], ADDON_RPM["base"], ADDON_RPM["optimistic"], "hipoteza",
     "udział × wypłata × 1000; wynik własnych założeń. Niezależnie od tego NerdWallet i SmartAsset raportują przychody głównie z partnerów i leadów (E-POR2-06, E-POR2-07)"],
]


def main():
    rows = []
    add = rows.append
    add(["section", "metric", "unit", *SCEN, "type", "basis_or_formula"])
    for k, label, unit, vals, basis in INPUTS:
        typ = "plan" if basis.startswith("PLAN") else ("szacunek" if basis.startswith("SZACUNEK") else ("ilustracja" if basis.startswith("ILUSTRACJA") else "założenie"))
        add(["input", f"{k}: {label}", unit, *[vals[s] for s in SCEN], typ, basis])
    for mth, v in SEASONALITY.items():
        add(["input", f"seasonality_{mth}: mnożnik RPM reklam w miesiącu", "mnożnik", round(v, 3), round(v, 3), round(v, 3), "założenie",
             "ZAŁOŻENIE; średnia roczna = 1,0; styczeń ok. 55% grudnia (raporty: spadek 35-75% po szczycie Q4, E-ADS-20). Sezonowości POPYTU (awarie HVAC, sezon burz, wiosenna sprzedaż domów) nie modelowano"])

    mf = {s: monetised_factor(s) for s in SCEN}
    hrpm = {s: human_session_rpm(s) for s in SCEN}
    rpm = {s: session_rpm(s) for s in SCEN}
    add(["output", "Udział odsłon monetyzowanych (adblock, brak wypełnienia, RDP)", "ułamek", *[round(mf[s], 3) for s in SCEN], "wynik",
         "(1-adblock)×(1-unfilled)×(1-rdp_share×(1-rdp_rpm_factor))"])
    add(["output", "Przychód reklamowy na 1000 sesji LUDZI (średnia roczna)", "USD / 1000 sesji ludzi", *[round(hrpm[s], 2) for s in SCEN], "wynik",
         "pages_per_session × page_rpm_us × (us_share + (1-us_share)×non_us_rpm_factor) × monetyzacja × mix_AI"])
    add(["output", "Przychód reklamowy na 1000 sesji ZAREJESTROWANYCH (z botami; średnia roczna)", "USD / 1000 sesji", *[round(rpm[s], 2) for s in SCEN], "wynik",
         "× human_share; jednostka używana w progach ruchu poniżej"])
    add(["output", "Przychód na 1000 sesji w styczniu (najsłabszy miesiąc)", "USD / 1000 sesji", *[round(rpm[s] * SEASONALITY['Jan'], 2) for s in SCEN], "wynik", "× mnożnik sezonowy"])
    add(["output", "Przychód na 1000 sesji w grudniu (najsilniejszy miesiąc)", "USD / 1000 sesji", *[round(rpm[s] * SEASONALITY['Dec'], 2) for s in SCEN], "wynik",
         "× mnożnik sezonowy; odczyty z XI-XII dzielić przez 1,2-1,36 przed porównaniem z rokiem"])

    bridge = {s: p("bridge_slots_per_page", s) * p("bridge_viewable_filled", s) * p("bridge_net_ecpm_us", s) for s in SCEN}
    add(["rpm_bridge", "Most CPM→RPM: page RPM z założeń o slotach i eCPM (test spójności z page_rpm_us)", "USD / 1000 odsłon",
         *[round(bridge[s], 2) for s in SCEN], "wynik", "sloty × widoczne/wypełnione × eCPM netto; wszystkie składniki to założenia"])
    add(["rpm_bridge", "Warstwa reklamodawcy (NIE przychód wydawcy): CPC Search / CPC Display, Finance & Insurance", "USD / klik",
         "3.44 / 0.86", "3.44 / 0.86", "3.44 / 0.86", "dane vendorskie",
         "Promodo (E-ADS-15); relacja ~4:1 orientacyjna; nie przeliczać na RPM strony"])
    add(["rpm_bridge", "Kontekst odgórny: Omni Calculator - przychód / 1000 wizyt (szacunek na szacunkach)", "USD / 1000 wizyt",
         15, 20, 30, "estymacja",
         "ok. 4,2-5 mln USD/rok (Growjo, nieaudytowane) / (14-23 mln wizyt/mies. × 12) (E-POR-02, E-POR2-05, E-VER-C4); globalny, szeroki katalog, wiele odsłon/sesję - nie benchmark dla nowej domeny; różnicy 2-4× wobec bazy nie rozstrzygnięto"])

    for t in TARGETS:
        req = {s: t / rpm[s] * 1000 for s in SCEN}
        add(["required_traffic", f"Sesje/mies. potrzebne dla {t} USD przychodu reklamowego (średnio w roku)", "sesje zarejestrowane / mies.",
             *[int(round(req[s], -3)) for s in SCEN], "wynik", f"{t} / (przychód na 1000 sesji) × 1000"])
        add(["required_traffic", f"Sesje/mies. potrzebne dla {t} USD w styczniu", "sesje / mies.",
             *[int(round(req[s] / SEASONALITY['Jan'], -3)) for s in SCEN], "wynik", "uwzględnia sezonowy dołek RPM"])
        add(["required_traffic", f"Sesje/dzień dla {t} USD/mies.", "sesje / dzień", *[int(round(req[s] / 30.4, -1)) for s in SCEN], "wynik", "/ 30,4"])
        for n in (10, 25, 100):
            add(["required_traffic", f"Średnio sesji/mies. NA NARZĘDZIE dla {t} USD przy {n} narzędziach z ruchem", "sesje / narzędzie / mies.",
                 *[int(round(req[s] / n, -1)) for s in SCEN], "wynik", "ilustruje, że katalog nie zastępuje ruchu na narzędzie"])
        human = {s: req[s] * p("human_share", s) for s in SCEN}
        ai = {s: human[s] * p("ai_share_of_sessions", s) for s in SCEN}
        add(["required_traffic", f"W tym sesje ludzi z wyszukiwarek i innych źródeł (nie-AI) dla {t} USD", "sesje / mies.",
             *[int(round(human[s] - ai[s], -2)) for s in SCEN], "wynik", "sesje ludzi × (1 - ai_share); w praktyce głównie Google organic"])
        add(["required_traffic", f"W tym sesje ludzi z asystentów AI dla {t} USD", "sesje AI / mies.",
             *[int(round(ai[s], -1)) for s in SCEN], "wynik",
             "sesje ludzi × ai_share; porównanie: Omni Calculator ok. 4-6 tys. wizyt/mies. z ChatGPT+Claude+Gemini (E-AI-14, E-VER-C4)"])
        add(["required_traffic", f"W tym sesje botów (niemonetyzowane) dla {t} USD", "sesje / mies.",
             *[int(round(req[s] - human[s], -2)) for s in SCEN], "wynik", "sesje zarejestrowane × (1 - human_share)"])

    for t in TARGETS:
        add(["sensitivity", f"WRAŻLIWOŚĆ (poza bazą): sesje/mies. dla {t} USD po przejściu do sieci premium (Journey/Mediavine) z odświeżaniem in-view", "sesje / mies.",
             *[int(round(t / (rpm[s] * PREMIUM_UPLIFT[s]) * 1000, -3)) for s in SCEN], "hipoteza",
             f"mnożnik przychodu na sesję {PREMIUM_UPLIFT}; brak danych dla stron-narzędzi (E-ADS-12, E-ADS-27)"])
    for t in TARGETS:
        add(["sensitivity", f"WRAŻLIWOŚĆ (hipoteza właściciela): sesje AI/mies. przy udziale AI 10%/20%/30% dla {t} USD", "sesje AI / mies.",
             *[int(round(t / rpm[s] * 1000 * p("human_share", s) * OWNER_AI_SHARE[s], -2)) for s in SCEN], "hipoteza",
             "obserwacja właściciela z healthscorer.com, niezweryfikowana (K-01); 10-300× powyżej benchmarku"])
    add(["sensitivity", "WRAŻLIWOŚĆ: przychód na 1000 sesji przy page RPM = 2,4 USD (mediana vendorska) we wszystkich scenariuszach", "USD / 1000 sesji",
         *[round(rpm[s] * 2.4 / p("page_rpm_us", s), 2) for s in SCEN], "wrażliwość", "E-ADS-11"])

    for tools in (5, 15, 25, 50):
        fc = {s: fixed_cash(s, tools) for s in SCEN}
        add(["costs", f"Stałe koszty gotówkowe/mies. przy {tools} narzędziach (z utrzymaniem eksperckim)", "USD / mies.",
             *[round(fc[s]) for s in SCEN], "wynik", "domena+VPS+AI+dane+monitoring + roczne godziny eksperta/12"])
        add(["costs", f"Czas właściciela na utrzymanie przy {tools} narzędziach", "h / mies.",
             *[round(owner_maint_hours(s, tools), 1) for s in SCEN], "wynik", "część stała + h/narzędzie × narzędzia"])
        add(["breakeven", f"Próg rentowności gotówkowej przy {tools} narzędziach", "sesje / mies.",
             *[int(round(fc[s] / rpm[s] * 1000, -2)) for s in SCEN], "wynik", "koszty stałe / przychód na sesję"])
        full = {s: fc[s] + owner_maint_hours(s, tools) * p("owner_hourly_value", s) for s in SCEN}
        add(["breakeven", f"Próg rentowności z wyceną czasu właściciela przy {tools} narzędziach", "sesje / mies.",
             *[int(round(full[s] / rpm[s] * 1000, -2)) for s in SCEN], "wynik", "(koszty stałe + utrzymanie × stawka) / przychód na sesję"])
    launch_cash = {s: p("one_time_legal", s) + 5 * build_cost_cash(s) for s in SCEN}
    launch_hours = {s: p("owner_hours_engine", s) + 5 * p("owner_hours_new_tool", s) for s in SCEN}
    for tools in (5, 15):
        amort = {s: fixed_cash(s, tools) + launch_cash[s] / 24 for s in SCEN}
        add(["breakeven", f"Próg rentowności gotówkowej przy {tools} narzędziach z amortyzacją gotówki uruchomienia w 24 mies.", "sesje / mies.",
             *[int(round(amort[s] / rpm[s] * 1000, -2)) for s in SCEN], "wynik", "(koszty stałe + gotówka uruchomienia/24) / przychód na sesję"])
    add(["unit_economics", "Koszt budowy jednego nowego narzędzia: gotówka (ekspert)", "USD", *[round(build_cost_cash(s)) for s in SCEN], "wynik", "expert_hours_new_tool × expert_hourly"])
    add(["unit_economics", "Koszt budowy jednego nowego narzędzia: czas właściciela (wycena)", "USD", *[round(build_cost_owner(s)) for s in SCEN], "wynik", "owner_hours_new_tool × owner_hourly_value"])
    upkeep = {s: p('expert_hours_upkeep_tool_year', s) * p('expert_hourly', s) / 12 for s in SCEN}
    add(["unit_economics", "Sesje/mies. na narzędzie potrzebne do zwrotu GOTÓWKI budowy w 24 mies. (+utrzymanie eksperckie)", "sesje / narzędzie / mies.",
         *[int(round((build_cost_cash(s) / 24 + upkeep[s]) / rpm[s] * 1000, -2)) for s in SCEN], "wynik",
         "na tym progu opiera się reguła dodawania narzędzi (architecture-and-validation.md §4.3); porównaj z rozkładem: w bazie najlepsze narzędzie ok. 15 tys. sesji/mies. po 12 mies., mediana narzędzi z ruchem znacznie niżej"])
    add(["unit_economics", "Sesje/mies. na narzędzie potrzebne do zwrotu PEŁNEGO kosztu budowy (gotówka + czas) w 24 mies.", "sesje / narzędzie / mies.",
         *[int(round(((build_cost_cash(s) + build_cost_owner(s)) / 24 + upkeep[s]) / rpm[s] * 1000, -2)) for s in SCEN], "wynik",
         "próg pomocniczy z wyceną czasu właściciela (nie jest regułą dodawania narzędzi)"])

    for t in TARGETS:
        op = {s: t - fixed_cash(s, 25) for s in SCEN}
        op_full = {s: op[s] - owner_maint_hours(s, 25) * p("owner_hourly_value", s) for s in SCEN}
        add(["operating_profit", f"Zysk operacyjny gotówkowy przy {t} USD przychodu i 25 narzędziach", "USD / mies.", *[round(op[s]) for s in SCEN], "wynik", "przychód - koszty stałe (25 narzędzi)"])
        add(["operating_profit", f"Marża operacyjna gotówkowa przy {t} USD i 25 narzędziach", "%", *[round(100 * op[s] / t) for s in SCEN], "wynik", "zysk gotówkowy / przychód"])
        add(["operating_profit", f"Zysk po wycenie czasu właściciela przy {t} USD i 25 narzędziach", "USD / mies.", *[round(op_full[s]) for s in SCEN], "wynik", "j.w. - utrzymanie × stawka właściciela"])

    add(["launch", "Gotówkowy koszt uruchomienia 5 symulatorów (prawo/CMP + eksperci)", "USD", *[int(round(launch_cash[s], -1)) for s in SCEN], "wynik",
         "jednorazowe; przy finansowaniu etapowym wydatek na produkty 2-5 następuje dopiero po ich bramkach"])
    add(["launch", "Gotówkowy koszt testu opcji: silnik minimalny + 1 symulator (RENO-02), z 3 mies. kosztów stałych", "USD",
         *[int(round(p('one_time_legal', s) + build_cost_cash(s) + 3 * fixed_cash(s, 1), -1)) for s in SCEN], "wynik", "prawo/CMP + ekspert RENO-02 + 3 mies. kosztów stałych"])
    add(["launch", "Czas właściciela na test opcji: silnik + 1 symulator (RENO-02)", "h",
         *[round(p('owner_hours_engine', s) + p('owner_hours_new_tool', s)) for s in SCEN], "wynik", "owner_hours_engine + owner_hours_new_tool"])
    add(["launch", "Czas właściciela na uruchomienie silnika + 5 symulatorów", "h", *[round(launch_hours[s]) for s in SCEN], "wynik", "silnik + 5 × narzędzie"])
    add(["launch", "Wycena czasu uruchomienia", "USD", *[int(round(launch_hours[s] * p('owner_hourly_value', s), -1)) for s in SCEN], "wynik", "h × stawka właściciela"])

    sims = {s: simulate(s) for s in SCEN}
    for mth in (6, 12, 24, 36):
        r = {s: sims[s][mth - 1] for s in SCEN}
        add(["trajectory", f"ILUSTRACJA: żywe narzędzia w mies. {mth}", "szt.", *[r[s]['live'] for s in SCEN], "ilustracja", "harmonogram ograniczony dostępnością właściciela (owner_build_hours_month)"])
        add(["trajectory", f"ILUSTRACJA: sesje/mies. w mies. {mth}", "sesje / mies.", *[int(round(r[s]['sessions'], -2)) for s in SCEN], "ilustracja", "Zipf × rampa; NIE prognoza"])
        add(["trajectory", f"ILUSTRACJA: przychód reklamowy w mies. {mth}", "USD / mies.", *[round(r[s]['revenue']) for s in SCEN], "ilustracja", "sesje × przychód na sesję × sezonowość (mies. 1 = styczeń)"])
        add(["trajectory", f"ILUSTRACJA: wynik gotówkowy w mies. {mth} (z kosztem ekspertów nowych narzędzi)", "USD / mies.", *[round(r[s]['revenue'] - r[s]['cash_cost']) for s in SCEN], "ilustracja",
             "przychód - koszty stałe - gotówka na ekspertów narzędzi uruchomionych w tym miesiącu"])
    for mth in (12, 24, 36):
        cum = {s: sum(x['revenue'] - x['cash_cost'] for x in sims[s][:mth]) for s in SCEN}
        cumf = {s: sum(x['revenue'] - x['cash_cost'] - x['owner_cost'] for x in sims[s][:mth]) for s in SCEN}
        add(["trajectory", f"ILUSTRACJA: skumulowany wynik gotówkowy po {mth} mies.", "USD", *[int(round(cum[s], -2)) for s in SCEN], "ilustracja", "suma miesięcy"])
        add(["trajectory", f"ILUSTRACJA: skumulowany wynik z wyceną czasu właściciela po {mth} mies.", "USD", *[int(round(cumf[s], -2)) for s in SCEN], "ilustracja", "suma miesięcy; czas budowy i utrzymania × stawka"])
    for mode in ("cash", "full"):
        vals = []
        for s in SCEN:
            run, low, pay = 0.0, 0.0, None
            for x in sims[s]:
                run += x['revenue'] - x['cash_cost'] - (x['owner_cost'] if mode == "full" else 0)
                low = min(low, run)
                if pay is None and run >= 0 and x['m'] > 1:
                    pay = x['m']
            vals.append((int(round(low, -2)), pay or 0))
        lbl = 'gotówka' if mode == 'cash' else 'gotówka + czas właściciela'
        add(["trajectory", f"ILUSTRACJA: maksymalne skumulowane zaangażowanie ({lbl})", "USD", *[v[0] for v in vals], "ilustracja", "najniższy punkt skumulowanego wyniku w 36 mies."])
        add(["trajectory", f"ILUSTRACJA: miesiąc zwrotu ({lbl}); 0 = brak zwrotu w 36 mies.", "mies.", *[v[1] for v in vals], "ilustracja", "pierwszy miesiąc, w którym skumulowany wynik ≥ 0"])

    for r in ADDONS:
        add(r)
    lead_be = {s: fixed_cash(s, 5) / ((rpm[s] + ADDON_RPM[s]) / 1000) for s in SCEN}
    add(["addon_separate", "DODATEK: próg rentowności gotówkowej przy 5 narzędziach, gdyby dodać lead-gen", "sesje / mies.",
         *[int(round(lead_be[s], -2)) for s in SCEN], "hipoteza",
         "poza modelem bazowym z powodu ograniczenia właściciela; liczbowo zmienia ekonomikę, ale wymaga zgód (TCPA) i rodzi konflikt z neutralnością"])

    with OUT.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"wrote {OUT} ({len(rows)-1} rows)")
    for s in SCEN:
        print(s, "USD/1000 recorded:", round(rpm[s], 2), "human:", round(hrpm[s], 2), {t: int(t / rpm[s] * 1000) for t in TARGETS},
              "| m12 live", sims[s][11]['live'], "rev", round(sims[s][11]['revenue']), "| cum36 cash", round(sum(x['revenue'] - x['cash_cost'] for x in sims[s])))


if __name__ == "__main__":
    main()
