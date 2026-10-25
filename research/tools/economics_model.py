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
     "USD / 1000 odsłon", {"conservative": 4.0, "base": 9.0, "optimistic": 18.0},
     "ZAŁOŻENIE skalibrowane do zakresów 3-5 / 8-12 / 15-25 USD (E-ADS-11, E-ADS-12, E-ADS-28; vendorskie i self-reported); nie pochodzi z danych healthscorer.com"),
    ("non_us_rpm_factor", "RPM ruchu spoza USA jako ułamek RPM USA", "ułamek",
     {"conservative": 0.20, "base": 0.25, "optimistic": 0.35}, "ZAŁOŻENIE (E-ADS-16: tier-1 vs reszta świata)"),
    ("us_share", "Udział sesji z USA wśród sesji ludzi", "ułamek",
     {"conservative": 0.60, "base": 0.75, "optimistic": 0.85}, "ZAŁOŻENIE (serwis anglojęzyczny, treści USA)"),
    ("pages_per_session", "Odsłony na sesję (narzędzie + metodologia/wyniki)", "odsłony / sesję",
     {"conservative": 1.1, "base": 1.3, "optimistic": 1.6}, "ZAŁOŻENIE oparte na E-ADS-26 (landing pages 1-1,5 PV/sesję; AdSense bez odświeżania): interaktywne przeliczenia nie generują odsłon"),
    ("adblock_loss", "Udział odsłon bez monetyzacji (adblock, brak zgody, brak wypełnienia)", "ułamek",
     {"conservative": 0.28, "base": 0.20, "optimistic": 0.15}, "ZAŁOŻENIE oparte na E-ADS-17, E-ADS-19 (adblock w USA 19-33% zależnie od metody) + GPC/RDP"),
    ("human_share", "Udział sesji ludzi w sesjach zarejestrowanych (po filtrach GA4)", "ułamek",
     {"conservative": 0.85, "base": 0.92, "optimistic": 0.97}, "ZAŁOŻENIE; boty/agenci AI nie są monetyzowani"),
    # --- traffic structure ---------------------------------------------------
    ("ai_share_of_sessions", "Udział ruchu z asystentów AI w sesjach ludzi", "ułamek",
     {"conservative": 0.02, "base": 0.10, "optimistic": 0.30}, "HIPOTEZA; benchmarki rynkowe 0,1-1% ruchu witryn (E-AI-02, E-VER-C5), właściciel obserwuje więcej na healthscorer.com (niezweryfikowane)"),
    ("ai_rpm_factor", "RPM sesji z AI względem średniej (mobile, aplikacje, zaangażowanie)", "mnożnik",
     {"conservative": 0.8, "base": 1.0, "optimistic": 1.15}, "HIPOTEZA; brak danych pierwotnych o RPM ruchu AI"),
    # --- costs (monthly, cash) -----------------------------------------------
    ("cost_domain", "Domena", "USD / mies.", {"conservative": 2, "base": 1.5, "optimistic": 1.5}, "ZAŁOŻENIE (~18-24 USD/rok)"),
    ("cost_vps_cdn", "VPS + CDN + kopie", "USD / mies.", {"conservative": 60, "base": 30, "optimistic": 30}, "ZAŁOŻENIE"),
    ("cost_ai_tools", "Claude Code / API LLM (część przypisana projektowi)", "USD / mies.",
     {"conservative": 200, "base": 120, "optimistic": 100}, "ZAŁOŻENIE (subskrypcja + API)"),
    ("cost_data", "Płatne dane / API", "USD / mies.", {"conservative": 50, "base": 0, "optimistic": 0},
     "ZAŁOŻENIE: start na danych publicznych (NREL, EIA, FRED itp.)"),
    ("cost_seo_ai_monitoring", "Narzędzia SEO / monitoring AI", "USD / mies.",
     {"conservative": 150, "base": 50, "optimistic": 0}, "ZAŁOŻENIE; start na GSC/Bing WMT"),
    ("expert_hourly", "Stawka eksperta (EA/CPA/CFP/fachowiec)", "USD / h",
     {"conservative": 250, "base": 175, "optimistic": 125}, "ZAŁOŻENIE (do potwierdzenia ofertą)"),
    ("expert_hours_new_tool", "Godziny eksperta na nowy symulator (średnio, mix poziomów ryzyka)", "h / narzędzie",
     {"conservative": 8, "base": 5, "optimistic": 3}, "ZAŁOŻENIE"),
    ("expert_hours_upkeep_tool_year", "Godziny eksperta na utrzymanie narzędzia rocznie", "h / narzędzie / rok",
     {"conservative": 4, "base": 2, "optimistic": 1}, "ZAŁOŻENIE"),
    ("owner_hours_month", "Czas właściciela na utrzymanie (bez budowy nowych narzędzi)", "h / mies.",
     {"conservative": 30, "base": 20, "optimistic": 12}, "ZAŁOŻENIE"),
    ("owner_hourly_value", "Wycena godziny właściciela (koszt alternatywny)", "USD / h",
     {"conservative": 50, "base": 40, "optimistic": 30}, "ZAŁOŻENIE"),
    ("owner_hours_new_tool", "Czas właściciela na zbudowanie symulatora z Claude Code (po zbudowaniu silnika)", "h / narzędzie",
     {"conservative": 60, "base": 35, "optimistic": 20}, "ZAŁOŻENIE"),
    ("owner_hours_engine", "Jednorazowa budowa silnika, CI, szablonów, analityki", "h",
     {"conservative": 220, "base": 140, "optimistic": 90}, "ZAŁOŻENIE"),
    ("one_time_legal", "Polityka prywatności, regulamin, audyt dostępności (jednorazowo)", "USD",
     {"conservative": 1500, "base": 600, "optimistic": 200}, "ZAŁOŻENIE"),
    # --- portfolio -----------------------------------------------------------
    ("tools_live_m12", "Liczba symulatorów po 12 mies.", "szt.", {"conservative": 10, "base": 15, "optimistic": 25}, "PLAN"),
    ("share_tools_with_traffic", "Udział narzędzi osiągających istotny ruch", "ułamek",
     {"conservative": 0.2, "base": 0.35, "optimistic": 0.5}, "ZAŁOŻENIE (rozkład potęgowy, nie liniowy)"),
    ("sessions_top_tool_m12", "Sesje/mies. najlepszego narzędzia w mies. 12", "sesje / mies.",
     {"conservative": 3000, "base": 15000, "optimistic": 60000}, "ILUSTRACJA, nie prognoza"),
    ("zipf_s", "Wykładnik rozkładu ruchu między narzędziami z ruchem (Zipf)", "-",
     {"conservative": 1.2, "base": 1.0, "optimistic": 0.9}, "ZAŁOŻENIE"),
]

SEASONALITY = {  # multiplier on RPM; normalised to mean 1.0 below. ASSUMPTION (E-ADS-20)
    "Jan": 0.75, "Feb": 0.85, "Mar": 0.95, "Apr": 0.95, "May": 1.0, "Jun": 0.97,
    "Jul": 0.92, "Aug": 0.95, "Sep": 1.0, "Oct": 1.05, "Nov": 1.2, "Dec": 1.35,
}
_m = sum(SEASONALITY.values()) / 12
SEASONALITY = {k: v / _m for k, v in SEASONALITY.items()}

TARGETS = [1000, 3000, 10000]
PREMIUM_UPLIFT = {"conservative": 1.2, "base": 1.5, "optimistic": 2.0}  # HYPOTHESIS


def p(key, s):
    for k, _, _, vals, _ in INPUTS:
        if k == key:
            return vals[s]
    raise KeyError(key)


def session_rpm(s):
    """Net ad revenue per 1000 RECORDED sessions (USD)."""
    blended_page_rpm = p("page_rpm_us", s) * (p("us_share", s) + (1 - p("us_share", s)) * p("non_us_rpm_factor", s))
    per_human_session = p("pages_per_session", s) * blended_page_rpm * (1 - p("adblock_loss", s))
    mix = 1 - p("ai_share_of_sessions", s) + p("ai_share_of_sessions", s) * p("ai_rpm_factor", s)
    return per_human_session * mix * p("human_share", s)


def monthly_fixed_cash(s, tools):
    base = sum(p(k, s) for k in ["cost_domain", "cost_vps_cdn", "cost_ai_tools", "cost_data", "cost_seo_ai_monitoring"])
    expert_upkeep = tools * p("expert_hours_upkeep_tool_year", s) * p("expert_hourly", s) / 12
    return base + expert_upkeep


def owner_cost(s):
    return p("owner_hours_month", s) * p("owner_hourly_value", s)


def zipf_sessions(s):
    n_tools = p("tools_live_m12", s)
    n_traffic = max(1, round(n_tools * p("share_tools_with_traffic", s)))
    top = p("sessions_top_tool_m12", s)
    z = p("zipf_s", s)
    return [top / (r ** z) for r in range(1, n_traffic + 1)], n_tools - n_traffic


def main():
    rows = []
    add = rows.append
    add(["section", "metric", "unit", *SCEN, "type", "basis_or_formula"])
    for k, label, unit, vals, basis in INPUTS:
        add(["input", f"{k}: {label}", unit, *[vals[s] for s in SCEN], "założenie" if "ZAŁOŻENIE" in basis or "HIPOTEZA" in basis or "ILUSTRACJA" in basis else "plan", basis])
    for mth, v in SEASONALITY.items():
        add(["input", f"seasonality_{mth}: mnożnik RPM w miesiącu", "mnożnik", round(v, 3), round(v, 3), round(v, 3), "założenie",
             "ZAŁOŻENIE; średnia roczna = 1.0; styczeń ok. 55% grudnia (raporty: spadek 35-75% po szczycie Q4, E-ADS-20)"])

    rpm = {s: session_rpm(s) for s in SCEN}
    add(["output", "Przychód reklamowy na 1000 zarejestrowanych sesji (średnia roczna)", "USD / 1000 sesji",
         *[round(rpm[s], 2) for s in SCEN], "wynik",
         "pages_per_session × page_rpm_us × (us_share + (1-us_share)×non_us_rpm_factor) × (1-adblock_loss) × mix_AI × human_share"])
    add(["output", "Przychód na 1000 sesji w styczniu (najsłabszy miesiąc)", "USD / 1000 sesji",
         *[round(rpm[s] * SEASONALITY['Jan'], 2) for s in SCEN], "wynik", "× mnożnik sezonowy"])
    add(["output", "Przychód na 1000 sesji w grudniu (najsilniejszy miesiąc)", "USD / 1000 sesji",
         *[round(rpm[s] * SEASONALITY['Dec'], 2) for s in SCEN], "wynik", "× mnożnik sezonowy"])

    for t in TARGETS:
        req = {s: t / rpm[s] * 1000 for s in SCEN}
        add(["required_traffic", f"Sesje/mies. potrzebne dla {t} USD przychodu reklamowego (średnio w roku)", "sesje / mies.",
             *[int(round(req[s], -3)) for s in SCEN], "wynik", f"{t} / (przychód na 1000 sesji) × 1000"])
        add(["required_traffic", f"Sesje/mies. potrzebne dla {t} USD w styczniu", "sesje / mies.",
             *[int(round(req[s] / SEASONALITY['Jan'], -3)) for s in SCEN], "wynik", "uwzględnia sezonowy dołek"])
        add(["required_traffic", f"Sesje/dzień dla {t} USD/mies.", "sesje / dzień",
             *[int(round(req[s] / 30.4, -1)) for s in SCEN], "wynik", "/ 30.4"])
        for n in (10, 25, 100):
            add(["required_traffic", f"Średnio sesji/mies. NA NARZĘDZIE dla {t} USD przy {n} narzędziach z ruchem", "sesje / narzędzie / mies.",
                 *[int(round(req[s] / n, -1)) for s in SCEN], "wynik", "ilustruje, że katalog nie zastępuje ruchu na narzędzie"])

    for t in TARGETS:
        add(["required_traffic", f"W tym sesje z asystentów AI/mies. dla {t} USD (przy udziale ai_share_of_sessions)", "sesje AI / mies.",
             *[int(round(t / rpm[s] * 1000 * p("ai_share_of_sessions", s), -2)) for s in SCEN], "wynik",
             "porównaj: Omni Calculator ~5-6 tys. wizyt/mies. z ChatGPT+Claude+Gemini przy ~14 mln wizyt (szacunek Semrush, E-AI-14, E-VER-C4)"])
    for t in TARGETS:
        add(["sensitivity", f"WRAŻLIWOŚĆ (poza bazą): sesje/mies. dla {t} USD po przejściu do sieci premium (Journey/Mediavine) z odświeżaniem in-view", "sesje / mies.",
             *[int(round(t / (rpm[s] * PREMIUM_UPLIFT[s]) * 1000, -3)) for s in SCEN], "hipoteza",
             f"mnożnik przychodu na sesję {PREMIUM_UPLIFT}; HIPOTEZA - brak danych dla stron-narzędzi (E-ADS-12, E-ADS-27)"])
    for tools in (5, 15, 50):
        fixed = {s: monthly_fixed_cash(s, tools) for s in SCEN}
        add(["costs", f"Stałe koszty gotówkowe/mies. przy {tools} narzędziach (z utrzymaniem eksperckim)", "USD / mies.",
             *[round(fixed[s]) for s in SCEN], "wynik", "domena+VPS+AI+dane+monitoring + roczne godziny eksperta/12"])
        add(["breakeven", f"Próg rentowności gotówkowej przy {tools} narzędziach", "sesje / mies.",
             *[int(round(fixed[s] / rpm[s] * 1000, -2)) for s in SCEN], "wynik", "koszty stałe / przychód na sesję"])
        full = {s: fixed[s] + owner_cost(s) for s in SCEN}
        add(["breakeven", f"Próg rentowności z wyceną czasu właściciela przy {tools} narzędziach", "sesje / mies.",
             *[int(round(full[s] / rpm[s] * 1000, -2)) for s in SCEN], "wynik", "(koszty stałe + godziny właściciela × stawka) / przychód na sesję"])

    for t in TARGETS:
        sess = {s: t / rpm[s] * 1000 for s in SCEN}
        op = {s: t - monthly_fixed_cash(s, 25) for s in SCEN}
        op_full = {s: op[s] - owner_cost(s) for s in SCEN}
        add(["operating_profit", f"Zysk operacyjny gotówkowy przy {t} USD przychodu i 25 narzędziach", "USD / mies.",
             *[round(op[s]) for s in SCEN], "wynik", "przychód - koszty stałe (25 narzędzi)"])
        add(["operating_profit", f"Zysk po wycenie czasu właściciela przy {t} USD i 25 narzędziach", "USD / mies.",
             *[round(op_full[s]) for s in SCEN], "wynik", "j.w. - czas właściciela"])

    launch_tools = 5
    launch_cash = {s: p("one_time_legal", s) + launch_tools * p("expert_hours_new_tool", s) * p("expert_hourly", s)
                   + 3 * (monthly_fixed_cash(s, launch_tools)) for s in SCEN}
    launch_hours = {s: p("owner_hours_engine", s) + launch_tools * p("owner_hours_new_tool", s) for s in SCEN}
    add(["launch", "Gotówkowy koszt uruchomienia 5 symulatorów (prawo + eksperci + 3 mies. kosztów stałych)", "USD",
         *[round(launch_cash[s], -1) for s in SCEN], "wynik", "jednorazowe"])
    add(["launch", "Czas właściciela na uruchomienie silnika + 5 symulatorów", "h",
         *[round(launch_hours[s]) for s in SCEN], "wynik", "silnik + 5 × narzędzie"])
    add(["launch", "Wycena czasu uruchomienia", "USD",
         *[round(launch_hours[s] * p("owner_hourly_value", s), -1) for s in SCEN], "wynik", "h × stawka właściciela"])

    for s in SCEN:
        pass
    illus = {}
    for s in SCEN:
        sessions, idle = zipf_sessions(s)
        total = sum(sessions)
        illus[s] = (total, total * rpm[s] / 1000, len(sessions), idle)
    add(["illustration_m12", "ILUSTRACJA: łączne sesje/mies. w mies. 12 (rozkład Zipfa między narzędziami z ruchem)", "sesje / mies.",
         *[int(round(illus[s][0], -2)) for s in SCEN], "ilustracja", "suma top/r^s dla narzędzi z ruchem; NIE jest prognozą"])
    add(["illustration_m12", "ILUSTRACJA: przychód reklamowy/mies. w mies. 12", "USD / mies.",
         *[round(illus[s][1]) for s in SCEN], "ilustracja", "sesje × przychód na sesję"])
    add(["illustration_m12", "ILUSTRACJA: narzędzia z ruchem / bez istotnego ruchu", "szt.",
         *[f"{illus[s][2]} / {illus[s][3]}" for s in SCEN], "ilustracja", "share_tools_with_traffic"])
    add(["illustration_m12", "ILUSTRACJA: wynik gotówkowy/mies. w mies. 12", "USD / mies.",
         *[round(illus[s][1] - monthly_fixed_cash(s, p('tools_live_m12', s))) for s in SCEN], "ilustracja", "przychód - koszty stałe"])
    add(["illustration_m12", "ILUSTRACJA: wynik po wycenie czasu właściciela w mies. 12", "USD / mies.",
         *[round(illus[s][1] - monthly_fixed_cash(s, p('tools_live_m12', s)) - owner_cost(s)) for s in SCEN], "ilustracja", "j.w. - czas właściciela"])

    for r in ADDONS:
        add(r)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"wrote {OUT} ({len(rows)-1} rows)")
    for s in SCEN:
        print(s, "USD/1000 sessions:", round(rpm[s], 2), {t: int(t / rpm[s] * 1000) for t in TARGETS})


# Add-on models are reported separately and never enter the base model above.
ADDONS = [
    ["addon_separate", "DODATEK (poza modelem bazowym): afiliacja/lead-gen — udział sesji kończących się kliknięciem partnera", "ułamek",
     0.005, 0.015, 0.03, "założenie", "ZAŁOŻENIE; nie ratuje modelu bazowego"],
    ["addon_separate", "DODATEK: przychód na kliknięcie/lead partnera (średnio)", "USD",
     5, 15, 40, "założenie", "ZAŁOŻENIE; stawki CPL w energii/ubezpieczeniach/kredytach są wyższe, ale wymagają kwalifikacji leadu (E-ADS-33, E-ADS-34)"],
    ["addon_separate", "DODATEK: przychód z afiliacji na 1000 sesji", "USD / 1000 sesji",
     round(0.005 * 5 * 1000, 2), round(0.015 * 15 * 1000, 2), round(0.03 * 40 * 1000, 2), "wynik", "udział × stawka × 1000"],
]

if __name__ == "__main__":
    main()
