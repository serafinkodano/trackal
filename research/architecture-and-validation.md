# Architektura, strategia domen i plan walidacji

Data: 2026-10-25. Odwołania `E-…` → `evidence-and-assumptions.md`; produkty `XXX-NN` → `product-opportunities.csv`.

## 1. ETAP G — jedna domena czy kilka

### 1.1 Porównanie wariantów

| Kryterium | A. Jedna szeroka domena („decision simulators for everything”) | B. Jedna domena o spójnej funkcji decyzyjnej, kilka powiązanych kategorii | C. Kilka domen tematycznych |
|---|---|---|---|
| Zrozumiałość marki | niska: „kalkulatory do wszystkiego” to pozycja Omni/calculator.net, które mają tysiące narzędzi i lata przewagi | **średnia–wysoka**, jeśli granica to jedna sytuacja użytkownika (dom i jego pieniądze), a nie typ narzędzia | wysoka w każdej niszy, ale każda marka startuje od zera |
| Zaufanie i kontrola jakości | trudne: wiele dziedzin, wielu ekspertów, jedna słaba strona obciąża całość (sygnały site-wide, E-POR2-08) | **dobre**: jeden standard metodologii, wspólni recenzenci dla powiązanych tematów (dach–ubezpieczenie–kredyt) | dobre lokalnie, ale wielokrotny koszt (polityki, strony metodologii, recenzenci) |
| Wspólne dane i silniki | formalnie tak, faktycznie mało współdzielenia między odległymi tematami | **najwięcej**: oś czasu przepływów, finansowanie, wartość domu, ubezpieczenie, podatek od sprzedaży | wspólny kod możliwy (monorepo), ale osobne wdrożenia i dane |
| Koszt obsługi | średni | **najniższy na produkt** | najwyższy: N × (AdSense, CMP, GSC/Bing, analityka, prawo, hosting) |
| Dystrybucja SEO | brak udokumentowanej kary za szerokość; „topic authority” udokumentowane tylko dla newsów [E-POR2-09]; ryzyko rozmycia trafności | spójny klaster ułatwia linkowanie wewnętrzne i ocenę trafności (hipoteza) | każda domena osobno buduje sygnały; nowe domeny są wolniejsze |
| Dystrybucja AI | brak dowodów, że szerokość domeny wpływa na cytowania; liczy się dopasowanie strony do pod-zapytania i rozpoznawalność marki poza witryną [E-AI-12, E-POR2-12] | j.w.; spójna marka łatwiej zdobywa wzmianki tematyczne (hipoteza) | j.w.; wiele słabych marek zamiast jednej |
| Rozdzielenie ryzyk | brak: jedno konto AdSense, jedna kara algorytmiczna, jedna blokada IVT [E-ADS-05, E-ADS-07] | brak (to samo), ale mniejsza powierzchnia ryzyka YMYL | **najlepsze**: kara lub IVT na jednej domenie nie uderza w inne |
| Możliwość późniejszego wydzielenia | trudna (przekierowania wielu kategorii) | **łatwa**: kategoria w podkatalogu (`/home-energy/`, `/car/`) → przekierowania 301 na nową domenę, gdy spełni warunki | nie dotyczy |

### 1.2 Rekomendacja

**Wariant B.** Jedna domena o funkcji „neutralne symulatory dużych decyzji pieniężnych wokół domu i auta” (*household capital decisions: home, its systems, insurance, home equity, car*).

- **Docelowa granica tematyczna:** decyzje, w których gospodarstwo domowe wydaje lub uruchamia **duży kapitał związany z domem lub autem** w horyzoncie 1–15 lat i musi uwzględnić finansowanie, ubezpieczenie i moment sprzedaży. Typy: dach, HVAC, okna i plan kapitałowy; ubezpieczenie domu i katastrofy; kapitał w domu (HELOC, cash-out, HEI); sprzedaż, wynajem, buy-before-sell; auto (ujemny kapitał, koniec leasingu, naprawa vs wymiana).
- **Zakres startowy (pilotaż):** 5 produktów z §3, wszystkie z rodzin RENO / INS / HOME / AUTO, na jednym silniku osi czasu.
- **Kategorie do dodania później** (po spełnieniu kryteriów z §4): FIN (home equity), HOME (sprzedaż, buy-before-sell), AUTO (koniec leasingu), ENER jako gałęzie istniejących symulatorów (PV, zasilanie awaryjne), LIFE-01 (dom dziedziczony).
- **Kategorie wyłączone z tej domeny:**
  - emerytura i podatki osobiste (rynek zajęty przez Boldin, ProjectionLab, MaxiFi, Open Social Security; wysoki koszt eksperta);
  - zdrowie i koszty leczenia (lepiej testować na healthscorer.com — spójność z istniejącą marką; ChatGPT nie pokazuje reklam przy tematach zdrowotnych [E-VER-C9]);
  - kredyty studenckie (oficjalny Loan Simulator);
  - opieka i starzenie (wysoki koszt eksperta, kontrowersyjny lead-gen [E-ADS-34]);
  - mała firma i e-commerce (inna publiczność, B2B, inne reklamy);
  - klify świadczeń dla gospodarstw o niskich dochodach.
- **Warunki uzasadniające osobną domenę** (wszystkie muszą być spełnione):
  1. kategoria ma **inną publiczność lub inny model monetyzacji** (np. e-commerce B2B, subskrypcja);
  2. albo **inny profil ryzyka** (zdrowie/medycyna, prawo);
  3. i ma **zwalidowany popyt**: ≥ 3 symulatory z ≥ 5 tys. sesji ludzi/mies. łącznie albo ≥ 10% ruchu domeny;
  4. i jest **potencjał marki** (wzmianki, linki, zapytania brandowe), który osobna nazwa wzmocni.

  Przykład: symulatory e-commerce (BIZ-04, BIZ-01) — jeżeli w ogóle — od razu na osobnej domenie lub jako sekcja istniejącego serwisu właściciela związanego z e-commerce, a nie w serwisie dla właścicieli domów.

### 1.3 Pozycjonowanie w jednym zdaniu

> *Neutral, assumption-transparent simulators for big home and car money decisions — compare your real options over time and see exactly what would flip the answer.*
> (PL: neutralne, jawne w założeniach symulatory dużych decyzji pieniężnych wokół domu i auta — porównanie realnych wariantów w czasie i progi, przy których odpowiedź się zmienia.)

## 2. ETAP H — architektura produktu

### Zasada nadrzędna: setki symulatorów = kilkanaście silników + konfiguracja

Serwis nie powinien być zbiorem setek niezależnych aplikacji. Proponowany podział na warstwy:

| Warstwa | Co zawiera | Kto/co ją zmienia | Częstotliwość zmian |
|---|---|---|---|
| 1. Prymitywy obliczeniowe (`engine-core`) | amortyzacja kredytu (stała/zmienna stopa, wcześniejsza spłata, refinansowanie), indeksacja/inflacja, NPV/IRR, podatek dochodowy (uproszczony moduł progów), amortyzacja podatkowa, degradacja wydajności, przepływy energii, rozkłady zdarzeń (awarie, szkody, pustostan) | programista + testy | rzadko |
| 2. Moduły domenowe (`modules/*`) | np. `roof`, `pv`, `battery`, `generator`, `mortgage`, `heloc`, `home-sale`, `insurance-policy`, `claim-history`, `vehicle`, `ev-charging`, `rental-unit`, `inventory-lot` — każdy z jawnie zadeklarowanymi wejściami, wyjściami i jednostkami | programista + przegląd merytoryczny | kwartalnie |
| 3. Zestawy danych i reguł (`rules/*`, `data/*`) | parametry podatkowe wg roku, taryfy, koszty jednostkowe, założenia rynkowe — każdy rekord z `effective_from`, `source_url`, `retrieved_at`, `reviewed_by`, `version` | n8n (pobranie) → testy → zatwierdzenie człowieka | od dni do roku |
| 4. Specyfikacja symulatora (`simulators/*.yaml`) | które moduły łączy, graf zależności, warianty decyzji jako listy zdarzeń w czasie, formularz, presety, wykresy, parametry wrażliwości, teksty | konfiguracja (bez kodu) | przy tworzeniu/zmianie produktu |
| 5. Warstwa treści | metodologia, założenia, ograniczenia, FAQ, przykłady wyników — generowane szablonowo z wyników silnika; LLM tylko redaguje opisy, nie produkuje liczb | LLM + walidator + człowiek dla YMYL | przy zmianie danych lub specyfikacji |
| 6. Prezentacja | statyczne strony (SSG), interaktywny formularz po stronie klienta, wykresy, eksport CSV/PDF, link do scenariusza | programista | rzadko |

### Model obliczeń: symulacja zdarzeń w czasie

Każdy wariant decyzji jest **listą zdarzeń na osi czasu** (miesięczny krok), a nie osobnym wzorem:

```
variant "install_pv_now":      [t=0 PV install (finance: loan_A)], [t=roof_fail_month: roof replace + PV detach/reinstall], [t=sale_month: home sale]
variant "roof_and_pv_together":[t=0 roof replace + PV install (finance: loan_B)], [t=sale_month: home sale]
variant "wait":                [t=roof_fail_month: roof replace], [t=sale_month: home sale]
```

Silnik dla każdego wariantu liczy: przepływy pieniężne miesiąc po miesiącu, saldo zadłużenia, minimalny stan gotówki (ograniczenie płynności), wartość bieżącą netto, skumulowany wynik w dacie sprzedaży, miesiąc progu opłacalności. Porównanie wariantów jest wynikiem głównym; pojedyncza liczba nie jest.

Graf zależności między modułami jest jawny (DAG): np. `roof.remaining_life → pv.detach_reinstall_event`, `home_sale.month → pv.value_capture`, `financing.rate → all.cashflows`, `tariff.export_rate → pv.savings → battery.value`. Symulator jest **produktem** tylko wtedy, gdy co najmniej jedna krawędź DAG zmienia ranking wariantów — to jest test na „sklejone kalkulatory” (patrz kryteria niżej).

### Konfiguracja symulatora (przykład specyfikacji)

```yaml
id: reno-02-aging-roof
version: 1.0.0
ruleset: us-2026.4            # wersja danych/reguł (efektywne daty)
modules: [roof, insurance_policy, storm_risk, financing, home_sale, pv_optional]
inputs:
  roof_age_years:      {type: int, unit: years, range: [0, 60], typical: [10, 30]}
  remaining_life:      {type: range, unit: years, default: [3, 8]}
  replace_quote:       {type: money, unit: USD, default_from: data.roof_cost_by_state}
  policy_settlement:   {type: enum, values: [RCV, ACV, schedule], default: RCV}
  wind_hail_deductible:{type: money_or_pct, base: coverage_a}
  sale_horizon:        {type: int, unit: months, range: [0, 180]}
  financing:           {type: enum, values: [cash, heloc, loan]}
presets: [tx-hail-belt-acv, fl-15yr-nonrenewal, oh-solar-planned]
variants:
  replace_now:     [{t: 0, event: roof.replace, finance: $financing}, {t: $sale_horizon, event: home_sale.sell}]
  repair_wait_N:   [{t: 0, event: roof.repair}, {t: N, event: roof.replace}, {t: $sale_horizon, event: home_sale.sell}]
  self_insure:     [{t: 0, event: none}, {t: storm_risk.event, event: insurance.claim}, {t: $sale_horizon, event: home_sale.sell}]
  sell_as_is:      [{t: $sale_horizon, event: home_sale.sell, credit: roof.buyer_credit}]
outputs: [expected_cost_to_sale, cash_low_point, break_even_replace_year, tornado, switching_values]
sensitivity: {params: [storm_risk.p_annual, sale_horizon, insurance.premium_age_surcharge], switching: [sale_horizon]}
content: {title_template: "...", assumptions_page: true, llm_editable: [intro, faq]}
review: {tier: R1, reviewers: [pc_agent, roofer], last_review: null}
```

### Schemat zależności modułów (pilotaż)

```
                ┌──────────── financing (amortyzacja, HELOC zmienna, cash-out, pożyczka) ───────────┐
                │                                                                                     │
 roof ──► insurance_policy ──► storm_risk          hvac_unit ──► energy_climate (EIA, bin)           │
   │            │                   │                  │                │                            │
   └────────────┴──── RENO-02 ◄─────┘                  └──── RENO-03 ◄──┘                            │
                         │                                     │                                     │
                    home_sale (§121, koszty transakcji, kredyt dla kupującego) ◄──────────────────────┤
                         │                                                                           │
          HOME-04 ◄── remodel_cost, property_tax          HOME-02 ◄── rental_cashflow, depreciation/recapture
                                                                                                     │
 vehicle (deprecjacja, payoff) ──► auto_sales_tax (51 jurysdykcji) ──► AUTO-01 ◄──────────────────────┘
 wspólne dla wszystkich: timeline (miesięczne przepływy), npv/irr, sensitivity, units, ruleset
```

Krawędzie, które **zmieniają ranking wariantów**, a więc uzasadniają „produkt” zamiast sklejonych kalkulatorów:
- RENO-02: `insurance_policy.settlement × roof.age → expected_out_of_pocket`; `home_sale.horizon → value_recapture`.
- RENO-03: `energy_climate × hvac_unit.cop_curve → operating_cost`; `panel_capacity → feasible_variants`.
- HOME-04: `financing.rate_lock_loss → monthly_cost`.
- HOME-02: `home_sale.121_clock → tax`.
- AUTO-01: `vehicle.depreciation × loan.balance → equity_crossing_month`.

### Analiza wrażliwości i progi

Silnik dostarcza trzy standardowe widoki, wspólne dla wszystkich symulatorów:

1. **Tornado** — zmiana każdego niepewnego parametru o ±X% / w zakresie wiarygodnym i wpływ na różnicę między najlepszym a drugim wariantem.
2. **Próg przełączenia (break-even / switching value)** — dla 1–3 kluczowych parametrów bisekcja: „PV teraz przestaje się opłacać, jeśli sprzedasz dom wcześniej niż za N lat” lub „generator wygrywa z baterią, jeśli awarie trwają średnio dłużej niż X godzin”.
3. **Siatka 2D** — mapa „który wariant wygrywa” dla dwóch parametrów (np. horyzont sprzedaży × stopa procentowa).

Opcjonalnie (moduły ryzyka: awarie, szkody, pustostan): Monte Carlo z jawnymi rozkładami i ziarnem losowym zapisanym w wyniku (odtwarzalność).

### Jednostki, walidacja, wersjonowanie

- Każde pole ma typ, jednostkę (USD, USD/kWh, kWh/rok, %/rok, miesiące), zakres dopuszczalny i zakres „typowy” (ostrzeżenie, nie blokada). Biblioteka jednostek w silniku zapobiega mieszaniu kWh i kW, rocznych i miesięcznych stóp, nominalnych i realnych wartości.
- Wynik zawiera metadane: `engine_version`, `simulator_version`, `ruleset_version` (np. `us-tax-2026.2`), datę danych. Te same wejścia + te same wersje = identyczny wynik (audytowalność, eksport).
- Reguły z datą obowiązywania (`effective_from/to`), aby scenariusz 2026 vs 2027 korzystał z właściwych parametrów (np. wygaśnięcie ulg).

### Testy

| Typ testu | Przykład | Kiedy blokuje wdrożenie |
|---|---|---|
| Jednostkowe modułów | amortyzacja vs tablica referencyjna; NPV vs niezależna implementacja | zawsze |
| Właściwości (property-based) | wyższa stopa → wyższy koszt kredytu; dłuższy horyzont sprzedaży nie zmniejsza wartości PV w wariancie „PV teraz” przy stałych założeniach | zawsze |
| Brzegowe | horyzont 0 miesięcy, sprzedaż przed zakończeniem instalacji, 100% finansowania, ujemny kapitał | zawsze |
| Złote przypadki (golden) | 10–30 ręcznie policzonych scenariuszy na symulator, w tym zweryfikowane przez eksperta lub odtworzone w arkuszu | zawsze |
| Porównawcze z narzędziami referencyjnymi | produkcja PV vs NREL PVWatts; harmonogram kredytu vs kalkulator CFPB/arkusz; koszty pojazdu vs AFDC/fueleconomy.gov | przy zmianie modułu |
| Regresja danych | nowy `ruleset_version` → różnice wyników na złotych przypadkach > próg wymagają akceptacji człowieka | przy każdej aktualizacji n8n |
| Treści | każda liczba w tekście ma pochodzić z wyniku silnika (walidator porównuje liczby w HTML z wynikami) | zawsze dla treści generowanych |

### Oddzielenie obliczeń od LLM

- LLM (Claude Code) **pisze kod i testy** w trakcie budowy oraz **redaguje opisy** na podstawie struktury wyników. LLM nie wylicza liczb publikowanych na stronie i nie interpretuje przepisów bez źródła.
- Teksty generowane: szablon + sloty liczbowe wypełniane wynikami silnika; walidator odrzuca tekst zawierający liczbę spoza wyników/założeń.
- Każdy symulator ma stronę metodologii z listą założeń, źródeł, wersji danych i ograniczeń („czego ten model nie uwzględnia”).

### Prywatność danych finansowych

- Obliczenia w przeglądarce (silnik w TypeScript/WASM); wartości wpisane przez użytkownika nie są wysyłane na serwer.
- Analityka rejestruje zdarzenia (`tool_started`, `tool_completed`, `variant_view`, `export`) i co najwyżej zgrubne kubełki, nigdy wartości kwot ani adresów.
- Link do scenariusza: parametry w fragmencie URL (`#…`), który nie trafia do logów serwera ani do referrera; strony z parametrami `noindex`.
- Upload dokumentów (np. oferty ubezpieczeniowej) — tylko lokalne parsowanie w przeglądarce lub wcale w MVP.

### Dostępność i mobile

- WCAG 2.2 AA: etykiety pól, obsługa klawiatury, kontrast, wykresy z tabelą alternatywną.
- Formularz progresywny: tryb „szybki” (5–8 pól z presetami) i „pełny” (wszystkie założenia). Mobile-first, bo ruch z aplikacji asystentów jest w dużej części mobilny (hipoteza do zmierzenia).
- Reklamy nie mogą przesuwać formularza (CLS) ani sąsiadować bezpośrednio z przyciskami (polityka przypadkowych kliknięć).

### Strony indeksowalne: kiedy osobne narzędzie, preset, parametr, strona

| Sytuacja | Rozwiązanie |
|---|---|
| Inna decyzja, inne warianty, inna kolejność zdarzeń lub inny model obliczeń | **osobny symulator** (osobna specyfikacja, osobna strona) |
| Ta sama decyzja, ale typowy profil użytkownika z innymi wartościami domyślnymi (np. „dach asfaltowy 20 lat, sprzedaż za 3 lata”) | **preset** w tym samym symulatorze (bez osobnej strony) |
| Liczba, data, miasto, wiek, kwota | **parametr** (nigdy osobna strona) |
| Ta sama decyzja, ale udokumentowana, odrębna intencja wyszukiwania/pytania z innym językiem problemu (np. „solar lease vs buy when selling house”) i ≥1 wariant/ograniczenie różni się istotnie | **osobna indeksowalna strona-wejście** z własnym presetem i treścią, kanonicznie odrębna — tylko po potwierdzeniu popytu |
| Region z istotnie innymi regułami (np. stan z inną taryfą net metering) | parametr + zestaw danych; osobna strona dopiero, gdy reguły zmieniają ranking wariantów i jest dowód popytu |

Zakaz: automatyczne generowanie stron dla kombinacji parametrów (miasto × kwota × rok). Polityka Google „scaled content abuse” dotyczy masowego tworzenia stron o niskiej wartości niezależnie od metody — patrz evidence-and-assumptions.md.

### Jak kilkaset modeli obsługuje setki tysięcy pytań

Pytanie użytkownika = (typ decyzji) × (wartości parametrów) × (kontekst). Liczba możliwych kombinacji parametrów jest praktycznie nieograniczona, ale **popyt nie jest równy liczbie kombinacji**. Jeden symulator „roof + solar + sale timing” obsługuje zarówno „roof 18 years old, selling in 3 years, Texas”, jak i „roof 8 years old, staying 15 years, California” — bez osobnych stron. Pojemność serwisu mierzy się liczbą odrębnych **typów decyzji z realnym popytem**, a nie liczbą odpowiedzi. Setki typów decyzji to realistyczny horyzont wieloletni, nie start; ruch będzie skrajnie nierówny (rozkład potęgowy — założenie w economics.csv).

### Układ strony pod politykę reklam i czytelność dla AI

- **Sloty reklamowe** tylko poza strefą sterowania: nad nagłówkiem, pod sekcją wyników/porównania, w bocznej kolumnie na desktopie, między sekcjami metodologii. Nigdy obok przycisków „Compare”, suwaków ani zakładek wariantów (polityka „Ads interfering” [E-ADS-03]). Bez reklam na ekranach pośrednich („calculating…”) i na stronach bez treści [E-ADS-02].
- **Bez odświeżania reklam po przeliczeniu.** AdSense dopuszcza nowe żądanie tylko po działaniu użytkownika i w określonych formatach; nie budować modelu na „przeliczenie = nowe wyświetlenie” bez potwierdzenia u Google [E-ADS-04, K-06].
- **Kod reklam w głównym dokumencie**, nie w iframe ani widgecie osadzanym u innych [E-ADS-04].
- **Treść czytelna bez JS:** nagłówek z pytaniem decyzyjnym, 3–5 zdań odpowiedzi „to zależy od…” z progami przełączenia dla domyślnego presetu, tabela przykładowych scenariuszy, założenia i źródła danych — wszystko w HTML renderowanym po stronie serwera (SSG). Systemy AI czytają widoczny HTML; JSON-LD daje efekt zerowy lub marginalny, a `llms.txt` nie wykazał efektu [E-POR2-13, E-POR2-14]. 44% cytowań ChatGPT pochodzi z pierwszych 30% tekstu [E-AI-14], więc wnioski idą na górę strony.
- **robots.txt i CDN:** wpuścić `Googlebot`, `Bingbot`, `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`, `Claude-SearchBot`, `Claude-User`. Boty treningowe (`GPTBot`, `ClaudeBot`, `Google-Extended`) to osobna decyzja, bez wpływu na wyszukiwanie [E-AI-22]. W Cloudflare świadomie zmienić domyślne blokady botów „Agent/Training” na stronach z reklamami [E-VER-C11]. Wykluczyć własne testy E2E i monitoring z wyświetlania reklam (ryzyko IVT [E-ADS-05]).

### Analityka źródeł AI i monetyzacji

- Klasyfikacja źródła wizyty: referrer (`chatgpt.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com`, `claude.ai`), `utm_source=chatgpt.com` i podobne, brak referrera (aplikacje mobilne — część ruchu AI wpada do „direct”).
- Logi serwera: osobna ewidencja botów pobierających strony na żądanie użytkownika (np. `ChatGPT-User`, `Perplexity-User`, `Claude-User`), crawlerów indeksujących (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`, `Bingbot`, `Googlebot`) i treningowych (`GPTBot`, `ClaudeBot`, `Google-Extended` jako token). Pobranie przez bota „user” ≠ wizyta człowieka.
- Lejek per strona i źródło: wejście → `tool_started` → `tool_completed` → odsłony reklam → przychód (kanały URL w AdSense lub raport wg stron).
- Monitoring obecności w asystentach: stała pula promptów (sekcja walidacji), wykonywana ręcznie lub przez oficjalne API z wyszukiwaniem, z zapisem daty, platformy, trybu, odpowiedzi i linków; świadomość, że wyniki API ≠ wyniki aplikacji konsumenckiej.

### Bezpieczne aktualizacje przez n8n

```
[cron n8n] → pobierz dane (API publiczne) → zapisz surowe + sumę kontrolną
          → porównaj z poprzednią wersją → jeżeli brak zmian: koniec
          → zbuduj kandydat ruleset_version → uruchom testy (CI)
          → testy OK i zmiana < progu → automatyczny PR + deploy na staging
          → zmiana reguły prawnej / > progu → zadanie do przeglądu człowieka (e-mail/Slack)
          → po akceptacji: deploy + wpis do changelogu metodologii
```

n8n nigdy nie zmienia logiki obliczeń ani reguł podatkowych bez akceptacji człowieka. Zmiany prawa (np. wygaśnięcie ulg) wykrywa się monitorowaniem źródeł (Federal Register, IRS newsroom, komunikaty stanowych regulatorów) — n8n tworzy zadanie, a nie zmianę.

### Rola VPS

- Serwowanie statycznego serwisu (Caddy/Nginx) za CDN; strony są statyczne, więc VPS nie jest wąskim gardłem.
- n8n, zadania pobierania danych, analiza logów (boty AI vs ludzie), kopie zapasowe.
- CI (testy silnika) — w GitHub Actions lub na VPS; deploy tylko z zielonych testów.
- Brak przetwarzania danych finansowych użytkowników po stronie serwera.

### Proces kontroli eksperckiej

| Poziom ryzyka | Przykłady | Kontrola |
|---|---|---|
| R1 — przepisy i pieniądze z konsekwencjami prawnymi | podatki, zasiłki, Medicare/ACA, wypłaty emerytalne, ubezpieczenia | ekspert zewnętrzny (EA/CPA/CFP lub licencjonowany agent) przed publikacją i po zmianach reguł |
| R2 — założenia techniczne | produkcja PV, zapotrzebowanie mocy, koszty remontów | walidacja względem narzędzi referencyjnych + przegląd fachowca przy starcie |
| R3 — finanse ogólne | harmonogramy kredytu, NPV, płynność | testy porównawcze, bez stałego eksperta |

Recenzja jest zapisana w repozytorium (kto, kiedy, jaka wersja, co sprawdzono) i widoczna na stronie metodologii.

## 3. Pilotaż: pierwsze 5 produktów

Kolejność budowy wynika z zależności modułów: każdy kolejny produkt dokłada 1–2 nowe moduły i używa wcześniejszych. Szczegółowe wejścia, warianty, źródła danych i prompty — w kartach w `top-10-products.md`. **Pracochłonność i godziny eksperta to szacunki** (właściciel pracuje z Claude Code; eksperci według zakresów zaproponowanych przez agentów fali 2b). Przegląd ekspercki finansujemy **etapami**: produkt nr N dostaje eksperta dopiero po przejściu bramki dla produktu N−1, więc gotówka wydawana na start to głównie RENO-02.

| # | Produkt | Minimalny wartościowy zakres (MVP) | Świadomie odłożone | Źródła danych i testy obliczeń | Ekspert (szac.) | Pracochłonność właściciela (szac.) |
|---|---|---|---|---|---|---|
| 1 | **RENO-02** Aging Roof: Replace, Repair, Fortify or Wait | 5 wariantów (wymiana teraz; naprawa + wymiana za N lat; czekanie z samoubezpieczeniem i wypłatą ACV; wymiana przed wystawieniem domu; sprzedaż as-is z kredytem dla kupującego) + przełącznik PV (koszt demontażu i ponownego montażu). Wejścia: wiek i materiał dachu, zakres pozostałej żywotności, wyceny, RCV/ACV/harmonogram wypłat (edytowalna tabela), udział wiatr/grad kwotowy lub %, składka i dopłata za wiek, p(nieodnowienie), horyzont sprzedaży, finansowanie. Wyniki: oczekiwany koszt do daty sprzedaży, próg roku wymiany, tornado, lista założeń | ryzyko gradu na poziomie ZIP/hrabstwa (FEMA NRI, NOAA); biblioteka harmonogramów ubezpieczycieli (SERFF); Monte Carlo; pełna ekonomika PV; reguły stanowe poza FL | Verisk 2026 Roof Report (koszty 2025), poradniki kosztu demontażu PV, FS 627.7011(5) (FL), Remodeling Cost vs Value; FEMA NRI (v1.1). Testy: złote przypadki ręczne (ACV, harmonogram, udział %), własności (wyższe p szkody → wcześniejsza wymiana nie jest droższa), brzegowe (sprzedaż w roku 0) | agent/underwriter P&C 6–10 h; dekarz/inspektor 4–6 h; agent nieruchomości 2–3 h | 50–70 h (w tym moduły: dach, ubezpieczenie, sprzedaż, finansowanie) + silnik 90–220 h |
| 2 | **RENO-03** AC or Furnace Just Died | 6 wariantów: naprawa z odroczeniem 1–3 lat; AC 1:1; dual-fuel (HP + istniejący piec, ekonomiczny punkt przełączania); HP z grzałką; cold-climate HP; wymiana obu urządzeń. Wejścia: ZIP/stan (ceny EIA, klimat z 20–25 miast reprezentatywnych), wiek urządzeń, paliwo, wycena naprawy, zużycie gazu, AFUE/SEER; opcjonalnie panel 100/150/200 A, horyzont, eskalacja, rabaty wpisywane ręcznie | mini-split; silnik ulg (Rewiring America API, HEAR); taryfy TOU (URDB); Manual J; olej opałowy; PV | EIA (ceny prądu i gazu wg stanu), NOAA Climate Normals / NREL TMY (rozkład temperatur), NEEP Cold-Climate ASHP List, AHRI; testy porównawcze z kalkulatorami ENERGY STAR i Rewiring America; złote przypadki „metoda bin” | wykonawca HVAC/NATE 6–10 h; modelarz energetyczny 8–12 h | 40–60 h (nowe moduły: energia/klimat, urządzenie) |
| 3 | **HOME-04** Remodel vs Move (rate lock-in aware) | warianty: zostać + projekt (rozbudowa/piwnica/ADU) z finansowaniem HELOC / home equity loan / gotówka / cash-out refi; przeprowadzka z nowym kredytem (koszty sprzedaży i zakupu, nowy podatek od nieruchomości); baseline. Wyniki: przepływy, majątek netto na koniec horyzontu, break-even, rozbicie „skąd różnica” (stopa, podatek, transakcje, remont), wrażliwość | kredyt assumable; podatek od nieruchomości 50 stanów (MVP: wpis + presety CA/FL); pełny podatek dochodowy; dochód z ADU; kredyty budowlane | Freddie Mac PMMS, prime rate + marże, FHFA (rozkład stóp), Lincoln Institute 50-State Property Tax, IRS Pub 523/936; testy: harmonogramy kredytów vs arkusz/CFPB, złote przypadki „kara za utratę stopy” | loan officer NMLS 4–6 h; CPA/EA 3–5 h; kosztorysant 3–4 h | 30–45 h (reużywa finansowania i sprzedaży; nowe: remont, podatek lokalny) |
| 4 | **HOME-02** Sell vs Rent Out When Moving | (A) „zegar wyłączenia §121”: ostatnia bezpieczna data zamknięcia, zalecana data wystawienia, ostrzeżenia (częściowe wyłączenie, MFJ, extended duty), plik .ics; (B) 4 warianty w horyzoncie do 10 lat: sprzedaż teraz i inwestycja; najem N lat i sprzedaż przed terminem; najem długoterminowy i sprzedaż po utracie wyłączenia; samodzielny zarząd vs firma zarządzająca; (C) podatki uproszczone, ale poprawne co do struktury (amortyzacja 27,5 roku, recapture, LTCG) | najem średnioterminowy; podatki stanowe; pełne NIIT/PAL/AMT; 1031; kredyt assumable | IRS Pub 523, 527, 946, Form 4797, IRC §121; PMMS; FHFA HPI; Zillow ZORI/ACS (czynsze — sprawdzić licencję [E-REG3-12]); złote przypadki G1–G9 zatwierdzone przez CPA | **CPA/EA 6–10 h (bez tego nie publikować)**; loan officer 2–4 h | 35–50 h (nowe: podatek od sprzedaży i amortyzacja najmu) |
| 5 | **AUTO-01** Underwater Car Loan Exit Planner | 6 wariantów na miesięcznej osi czasu (36–84 mies.): zatrzymaj do dodatniego kapitału; wymień teraz z przeniesieniem długu; wymień i dopłać lukę; sprzedaj prywatnie i weź pożyczkę na lukę; refinansuj i zostań; poczekaj N miesięcy (suwak 0–24). Wejścia: payoff, APR, wartość trade-in i private party, presety deprecjacji, stan (tabela 51 jurysdykcji: podatek i ulga trade-in), nowe auto, ładowanie w domu, gotówka, limit raty. EV jako typ napędu | leasing z ujemnym kapitałem; wyceny na żywo (KBB/Edmunds API — licencje); macierz APR wg scoringu i gap insurance; podatek lokalny po ZIP; ulga odsetkowa OBBBA tylko jako informacja z datą | Edmunds (raporty kwartalne), CFPB Data Spotlight, fueleconomy.gov, EIA (prąd), AAA/EIA (benzyna), Fed G.19 (APR); tabela podatków ze stron departamentów skarbowych (do zebrania); testy amortyzacji vs arkusz; własności (wyższa deprecjacja → późniejszy miesiąc przecięcia) | specjalista finansowania aut (F&I/CFP) 8–12 h; CPA ds. sales tax 3–5 h | 30–40 h (nowe: auto, podatek od sprzedaży auta) |

Łącznie, szacunkowo: **silnik 90–220 h + 5 produktów 185–265 h** pracy właściciela oraz **~55–90 h eksperta** (przy stawkach 125–250 USD/h ≈ 7–22 tys. USD, finansowane etapami).

### 3.1 Kluczowa hipoteza, miara sukcesu i warunek zatrzymania (dla każdego produktu)

Miary liczymy od dnia, w którym strona jest zaindeksowana w Google i Bing (nie od publikacji). Progi to **propozycje decyzyjne**, nie normy rynkowe.

| Produkt | Kluczowa hipoteza | Miara sukcesu (90 dni po indeksacji) | Warunek zatrzymania produktu |
|---|---|---|---|
| RENO-02 | Właściciele, którzy dostają od ubezpieczyciela zmianę warunków dla starego dachu (ACV, harmonogram, nieodnowienie) albo planują sprzedaż, szukają rachunku „wymienić teraz czy czekać”. Symulator daje wynik lepszy niż odpowiedź asystenta (mniej pominiętych zależności) | ≥ 500 wyświetleń GSC/mies.; CTR ≥ 1,5%; `tool_completed`/`tool_started` ≥ 35%; ≥ 1 cytowanie w panelu promptów lub w Bing AI Performance; w teście porównawczym asystenci pomijają ≥ 2 zależności (ACV/harmonogram, horyzont sprzedaży, demontaż PV) | < 100 wyświetleń/mies. po 90 dniach od indeksacji **i** brak cytowań; albo asystenci w ≥ 90% uruchomień dają pełne porównanie wariantów bez linków, a GSC stoi |
| RENO-03 | Moment awarii generuje pilne, mobilne sesje; użytkownik chce porównać 4–6 dróg w kilka minut; wartość reklamowa usług HVAC jest wysoka | ≥ 500 wyświetleń/mies.; ukończenie ≥ 30% (sesje pilne); udział mobile ≥ 50%; RPM strony ≥ średniej serwisu | < 100 wyświetleń/mies. albo ukończenie < 15% po 2 iteracjach formularza („tryb szybki”) |
| HOME-04 | Efekt zamrożenia stóp tworzy pytania „remont czy przeprowadzka”, a rozbicie „kary za utratę stopy” jest wyróżnikiem, którego asystenci nie liczą spójnie | ≥ 400 wyświetleń/mies.; CTR ≥ 1%; ukończenie ≥ 30%; ≥ 1 cytowanie | < 100 wyświetleń/mies. i brak cytowań po 90 dniach |
| HOME-02 | Moduł „zegar §121” to unikalny, cytowalny wynik (konkretna data), który zwiększa szansę na link z asystenta lub forum mimo zatłoczonej kategorii „rent vs sell” | ≥ 500 wyświetleń/mies.; ≥ 2 cytowania w panelu lub w Bing AI; ukończenie ≥ 35% | brak cytowań i < 150 wyświetleń/mies. po 90 dniach; albo wykrycie konkurenta, który liczy zegar i 4 warianty (wtedy wycofać się z kategorii) |
| AUTO-01 | Druga pula popytu (auta) o niskim koszcie eksperckim; integracja 6 wariantów wyróżnia się mimo 10+ prostych kalkulatorów | ≥ 800 wyświetleń/mies.; CTR ≥ 1%; ukończenie ≥ 30% | CTR < 0,5% przy ≥ 1 000 wyświetleń (SERP zdominowany przez kalkulatory i lenderów) albo < 150 wyświetleń/mies. |

### 3.2 Produkty kolejne (jeśli pilotaż przejdzie do „kontynuować”)

6. **RENO-04** Whole-Home Capital Plan Sequencer (składa moduły RENO-02 i RENO-03). 7. **LIFE-01** Inherited House (po zaangażowaniu CPA/prawnika spadkowego). 8. **INS-03** Home Insurance Renewal Shock (po inwentaryzacji danych stanowych). 9. **FIN-01** Equity Access (HELOC vs HEL vs cash-out, z zachowaniem niskiej stopy). 10. **AUTO-02** Lease-End Decision. Dalsze gałęzie: ENER-01 (forma własności PV) jako gałąź RENO-02; INS-06 (pompa sump) jako gałąź zasilania awaryjnego.

## 4. Plan 30/60/90 dni i kryteria decyzji

### 4.1 Zasada: rozdzielić sześć warstw lejka

Brak ruchu po 30 dniach **nie jest** dowodem braku rynku. Każdą warstwę mierzy się osobno i diagnozuje w kolejności:

| Warstwa | Pytanie | Miara | Źródło danych |
|---|---|---|---|
| 1. Dostępność | czy strona działa szybko i jest czytelna dla botów? | uptime, LCP/CLS (mobile), HTML z treścią bez JS; 200 dla `Googlebot`, `Bingbot`, `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` | monitoring, logi, test `curl -A` |
| 2. Indeksacja | czy strona jest w indeksach? | zaindeksowane URL-e w GSC i Bing WMT; pierwsze pobrania przez `OAI-SearchBot` / `PerplexityBot` w logach | GSC, Bing WMT, logi |
| 3. Widoczność | czy pojawia się w wynikach i odpowiedziach? | wyświetlenia GSC; raport GSC „Generative AI” (wyświetlenia AIO/AI Mode); Bing „AI Performance” (cytowania Copilot); panel promptów: % odpowiedzi z cytowaniem | GSC, Bing WMT, panel |
| 4. Kliknięcia | czy ktoś przychodzi? | kliknięcia GSC, CTR; sesje z referrerem AI / `utm_source`; udział „Direct” na podstronach narzędzi | GSC, GA4, logi |
| 5. Użycie narzędzia | czy ludzie kończą symulację? | `tool_started` / sesję, `tool_completed` / `tool_started`, `variant_view`, `sensitivity_view`, `export` | GA4 (zdarzenia bez wartości) |
| 6. Monetyzacja | czy sesja zarabia? | page RPM, przychód / 1000 sesji ludzi z USA; udział odsłon z reklamą | AdSense (raport URL) + GA4 |

### 4.2 Harmonogram

**Dni 0–14 — eksperyment pomiarowy, bez budowy (koszt ≈ 0 USD, ~15–20 h pracy):**
1. Logi healthscorer.com za 30–90 dni: rozdzielenie pobrań botów (`ChatGPT-User`, `Claude-User`, `Perplexity-User`, `OAI-SearchBot`…) od sesji ludzi z referrerem lub `utm_source` asystentów; przychód AdSense z tych sesji (kanały URL). Wynik: liczba **ludzi** z AI miesięcznie i ich RPM.
2. Panel promptów (§5) dla 5 rekomendowanych produktów: 5 asystentów × 8–12 promptów × 3 powtórzenia. Wynik: odsetek odpowiedzi z klikalnym linkiem do zewnętrznego narzędzia oraz czy asystent sam generuje kalkulator (Intelligent UI / generatywne UI).
3. Ręczne otwarcie stron najbliższych konkurentów (lista w `top-10-products.md`) i test formularzy, czyli tego, czego ta sesja nie mogła zrobić.

**Bramka G0 (dzień 14):** budować pilot **tylko jeśli** spełniony jest przynajmniej jeden warunek:
- (a) w panelu ≥ 10% odpowiedzi na prompty z prośbą o kalkulator linkuje do zewnętrznego narzędzia (dowolnego), a nie tylko do artykułów;
- (b) healthscorer.com ma ≥ 300 sesji ludzi z AI miesięcznie po odfiltrowaniu botów;
- (c) właściciel świadomie akceptuje, że kanałem bazowym będzie Google organic (wtedy oceniać według §4.3 bez oczekiwań co do AI).

Jeżeli żaden warunek nie jest spełniony: **nie budować domeny symulatorów.** Ewentualnie przetestować jeden symulator na healthscorer.com (HLTH-02) jako najtańszy test.

**Dni 15–30 — budowa minimalna:**
- domena, hosting statyczny za CDN, robots.txt (wpuścić boty wyszukiwania, świadomie skonfigurować Cloudflare [E-VER-C11]), GSC, Bing WMT, IndexNow, GA4 z kanałem AI i zdarzeniami;
- silnik osi czasu + **1 symulator** (produkt nr 1) + strona metodologii + 3–5 stron-presetów z udokumentowaną odrębną intencją;
- wniosek o dodanie witryny do AdSense (nowa witryna podlega ocenie [E-ADS-09]);
- przegląd ekspercki produktu nr 1 (zakres w §3).

**Dni 31–60 — rozszerzenie:**
- produkty nr 2 i 3 na tym samym silniku; porównanie jakości wyniku z generatywnym UI asystentów (ten sam scenariusz w ChatGPT i AI Mode: czas, błędy, brakujące zależności);
- pierwszy pomiar RPM na realnym ruchu, nawet małym (minimum 2 000 odsłon do odczytu kierunkowego);
- powtórzenie panelu promptów dla produktu nr 1 (czy strona jest cytowana).

**Dni 61–90 — ocena:**
- produkty nr 4 i 5;
- trzeci pomiar panelu; analiza lejka (warstwy 1–6) dla wszystkich produktów;
- decyzja według §4.3. **Nie oceniać RPM na danych z I–II** (sezonowy dołek [E-ADS-20]).

### 4.3 Kryteria decyzji (propozycje decyzyjne, nie normy rynkowe)

Progi sesji odnoszą się do sesji **ludzi** (po filtrach botów), mierzonych na koniec dnia 90 i po 6 miesiącach.

| Decyzja | Dzień 90 (wczesne sygnały) | Miesiąc 6 (sygnały ekonomiczne) |
|---|---|---|
| **Kontynuować** (dodawać 2–4 symulatory/mies.) | ≥ 3 z 5 produktów zaindeksowane i z ≥ 500 wyświetleniami GSC/mies.; `tool_completed` / `tool_started` ≥ 35%; ≥ 1 cytowanie w panelu promptów lub w Bing AI Performance | ≥ 15 tys. sesji/mies. łącznie z trendem ≥ +15% m/m przez 3 mies.; przychód ≥ 5 USD / 1000 sesji z USA; ≥ 2 produkty z ≥ 3 tys. sesji/mies. |
| **Zmodyfikować** | wyświetlenia są, ale CTR < 1% albo ukończenie < 20% → zmiana tytułów, presetów, formularza (tryb szybki), treści HTML | ruch rośnie, ale przychód < 3 USD / 1000 sesji → test innego formatu (raport wielostronicowy, eksport), afiliacji jako **dodatku** albo innej niszy; ruch nie rośnie, ale RPM dobry → zmiana kategorii |
| **Wstrzymać** (nie budować nowych, utrzymywać istniejące) | < 100 wyświetleń GSC/mies. na produkt mimo indeksacji i 0 cytowań w panelu i w Bing AI; albo dwukrotne odrzucenie AdSense | < 5 tys. sesji/mies. łącznie albo przychód < 50 USD/mies. przy ≥ 5 produktach |
| **Odrzucić** (zamknąć projekt jako biznes reklamowy) | — | po 9–12 mies.: < 10 tys. sesji/mies. łącznie **i** przychód < 3 USD / 1000 sesji **i** udział AI < 5% sesji ludzi; albo kara ręczna / algorytmiczna obejmująca domenę |

### 4.4 Warunek przerwania projektu (rekomendacja)

Przerwać, jeżeli **po 6 miesiącach od publikacji pierwszych 3 symulatorów** przychód reklamowy pozostaje poniżej ok. 100 USD/mies. **i** ruch nie rośnie przez 3 kolejne miesiące, **albo** jeśli bramka G0 wykaże, że asystenci nie linkują do zewnętrznych narzędzi w badanych decyzjach, a właściciel nie akceptuje Google organic jako kanału bazowego. W obu przypadkach model „setki symulatorów + AdSense” nie ma podstaw. Ewentualną kontynuację warto wtedy rozważać wyłącznie w innym modelu (lead-gen, B2B embed, subskrypcja) i osobną decyzją.

---

## 5. Protokół testu dystrybucji przez asystentów (do wykonania przez właściciela)

1. **Platformy:** ChatGPT (Free i Plus, jeśli dostępne), Google AI Mode i zwykłe wyszukiwanie z AI Overviews, Perplexity, Microsoft Copilot, Claude. Konta prywatne, bez historii; lokalizacja USA, jeśli zgodnie z warunkami usług dostępna (VPN tylko tam, gdzie regulamin na to pozwala); język angielski.
2. **Prompty:** zestawy z `top-10-products.md` (dla każdego produktu: 4 bez prośby o narzędzie, 4 z prośbą o kalkulator, 2–4 z prośbą o porównanie scenariuszy).
3. **Powtórzenia:** 3 uruchomienia każdego promptu w nowym czacie, w różnych dniach. Listy rekomendacji powtarzają się identycznie rzadziej niż w 1 na 100 uruchomień [E-AI-23].
4. **Zapis** (arkusz): platforma, wersja/tryb, data i godzina, prompt, czy włączono wyszukiwanie, pełna odpowiedź (zrzut), czy asystent **sam** zbudował kalkulator lub tabelę, lista linków (URL, typ: narzędzie / artykuł / forum / sklep / lead-gen), czy któryś link prowadzi do narzędzia realizującego pełny problem, brakujące zależności w odpowiedzi (np. pominięty koszt demontażu PV, ACV vs RCV, horyzont sprzedaży), błędy merytoryczne.
5. **Miary:** % odpowiedzi z jakimkolwiek linkiem; % z linkiem do narzędzia; % z samodzielnie wygenerowanym kalkulatorem; liczba brakujących zależności (jakość); po publikacji — % odpowiedzi z cytowaniem naszej domeny.
6. **Zakazy:** bez automatyzacji interfejsów konsumenckich wbrew regulaminom; oficjalne API (np. z narzędziem wyszukiwania) tylko jako uzupełnienie, z adnotacją, że wyniki API ≠ wyniki aplikacji [E-AI-23].
