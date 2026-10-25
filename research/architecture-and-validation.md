# Architektura, strategia domen i plan walidacji

Data: 2026-10-25 (wersja po recenzji fali 3 i kontroli spójności). Odwołania `E-…`, `Z-…`, `K-…` → `evidence-and-assumptions.md`; produkty `XXX-NN` → `product-opportunities.csv`; liczby ekonomiczne → `economics.csv`.

**Kontekst decyzji.** Werdykt raportu (executive-summary.md §1): **budować warunkowo — wyłącznie jako ograniczony test opcji. W zakładanej formie (setki symulatorów, AdSense jako podstawa przychodu, ruch liczony na asystentach AI): nie budować.** Test opcji to jeden symulator **RENO-02** na minimalnym silniku osi czasu, na nowej domenie wariantu B, z limitem gotówki do ok. 9 tys. USD i czasu właściciela do ok. 300 h na G0 i budowę (bez utrzymania po publikacji), uruchamiany wyłącznie po zaliczeniu bramki G0 (§4.2). W scenariuszu bazowym test mieści się w obu limitach do decyzji 6-miesięcznej, ale jeśli RENO-02 nie osiągnie ok. 250 USD/mies. przychodu, limit gotówki wyczerpuje się ok. 18. mies. od startu budowy; w konserwatywnym test przekracza oba limity jeszcze przed publikacją (§4.2, „Limity w kalendarzu”). Architektura w §2 opisuje docelowy kształt systemu, gdyby test się powiódł; w teście budujemy tylko minimalny silnik i jeden symulator.

## 1. ETAP G — jedna domena czy kilka

### 1.1 Porównanie wariantów

| Kryterium | A. Jedna szeroka domena („decision simulators for everything”) | B. Jedna domena o spójnej funkcji decyzyjnej, kilka powiązanych kategorii | C. Kilka domen tematycznych |
|---|---|---|---|
| Zrozumiałość marki | niska: „kalkulatory do wszystkiego” to pozycja Omni Calculator (ok. 3,7–3,8 tys. kalkulatorów, ok. 14–16,5 mln wizyt/mies. wg Semrush) i calculator.net (56–63 mln wizyt/mies. wg Semrush; liczby jego narzędzi nie weryfikowano w tej sesji), które mają lata przewagi; liczby wizyt to estymacje panelowe [E-POR-02, E-POR2-05, E-VER-C4, E-REV-04, E-AI-14, E-ADS-10] | **średnia–wysoka**, jeśli granica to jedna sytuacja użytkownika (dom i jego pieniądze), a nie typ narzędzia | wysoka w każdej niszy, ale każda marka startuje od zera |
| Zaufanie i kontrola jakości | trudne: wiele dziedzin i wielu ekspertów; Google ocenia głównie strony, ale stosuje też niektóre sygnały site-wide, więc duży odsetek słabych stron może obniżyć ocenę witryny; udokumentowanej kary za samą szerokość nie znaleziono [E-POR2-08, E-POR2-09] | **dobre**: jeden standard metodologii, wspólni recenzenci dla powiązanych tematów (dach–ubezpieczenie–kredyt) | dobre lokalnie, ale wielokrotny koszt (polityki, strony metodologii, recenzenci) |
| Wspólne dane i silniki | formalnie tak, faktycznie mało współdzielenia między odległymi tematami | **najwięcej**: oś czasu przepływów, finansowanie, wartość domu, ubezpieczenie, podatek od sprzedaży | wspólny kod możliwy (monorepo), ale osobne wdrożenia i dane |
| Koszt obsługi | średni | **najniższy na produkt** | najwyższy: N × (AdSense, CMP, GSC/Bing, analityka, prawo, hosting) |
| Dystrybucja SEO | nie znaleziono udokumentowanej kary za szerokość; „topic authority” udokumentowane tylko dla newsów [E-POR2-09]; ryzyko rozmycia trafności | spójny klaster ułatwia linkowanie wewnętrzne i ocenę trafności (hipoteza) | każda domena osobno buduje sygnały; nowe domeny są wolniejsze |
| Dystrybucja AI | nie znaleziono dowodów, że szerokość domeny wpływa na cytowania; w ChatGPT (dane Ahrefs; korelacja) częściej cytowane są strony dopasowane do węższych pod-zapytań, a dla innych asystentów tego nie badano [E-AI-12]; widoczność w ChatGPT, AI Mode i AIO koreluje ze wzmiankami o marce poza witryną (korelacja w danych dostawców, pewność niska; dla Claude i Copilota brak danych) [E-POR2-12] | j.w.; spójna marka łatwiej zdobywa wzmianki tematyczne (hipoteza) | j.w.; wiele słabych marek zamiast jednej |
| Rozdzielenie ryzyk | brak rozdzielenia: jedno konto AdSense, jedna kara algorytmiczna, jedna blokada IVT [E-ADS-05, E-ADS-07] | brak rozdzielenia (to samo), ale mniejsza powierzchnia ryzyka YMYL | **najlepsze**: kara lub IVT na jednej domenie nie uderza w inne |
| Możliwość późniejszego wydzielenia | trudna (przekierowania wielu kategorii) | **łatwa**: kategoria w podkatalogu (`/home-energy/`, `/car/`) → przekierowania 301 na nową domenę, gdy spełni warunki | nie dotyczy |

### 1.2 Rekomendacja

**Wariant B.** Jedna domena o spójnej funkcji decyzyjnej: dom, jego systemy, ubezpieczenie, kapitał w domu i auto (*household capital decisions: home, its systems, insurance, home equity, car*). Kategorie w podkatalogach, z możliwym późniejszym wydzieleniem przez przekierowania 301.

- **Docelowa granica tematyczna:** decyzje, w których gospodarstwo domowe wydaje lub uruchamia **duży kapitał związany z domem lub autem** w horyzoncie 1–15 lat i musi uwzględnić finansowanie, ubezpieczenie i moment sprzedaży. Typy: dach, HVAC, okna i plan kapitałowy; ubezpieczenie domu i katastrofy; kapitał w domu (HELOC, cash-out, HEI); sprzedaż, wynajem, buy-before-sell; auto (ujemny kapitał, koniec leasingu, naprawa vs wymiana).
- **Zakres startowy:** wyłącznie test opcji **RENO-02** na minimalnym silniku osi czasu. Pozostałe produkty pilotażowe z §3 (RENO-03, HOME-04, HOME-02, AUTO-01) są kandydatami warunkowymi; każdy wymaga własnego pomiaru popytu i SERP (jak w G0, kroki 2–3), własnej ręcznej weryfikacji konkurencji i spełnienia reguły dodawania narzędzi (§4.3).
- **Kategorie do dodania później** (po spełnieniu kryteriów z §4.3): RENO-04 (plan kapitałowy, po RENO-02 i RENO-03); INS (szok przy odnowieniu polisy: INS-03, produkt nr 8, start od jednego stanu po inwentaryzacji danych K-08; INS-01 „czy zgłaszać szkodę” jako osobna decyzja); FIN (home equity); HOME (sprzedaż, buy-before-sell); AUTO (koniec leasingu); ENER: ENER-01 (forma własności PV; odrębna decyzja na module PV z RENO-02) i ENER-03 (zasilanie awaryjne; odrębny produkt z gałęzią INS-06), oba „później”, a taryfy jako warstwa danych; LIFE-01 (dom dziedziczony).
- **Kategorie wyłączone z tej domeny:**
  - **samodzielne planery podatku dochodowego** (zeznanie, Roth, withholding) i planowanie emerytalne: rynek zajęty przez Boldin, ProjectionLab, MaxiFi, Open Social Security; wysoki koszt eksperta. **Moduły podatkowe wbudowane w decyzje o domu lub aucie** (np. §121 i recapture w HOME-02, step-up w LIFE-01, podatek od sprzedaży auta w AUTO-01) **są w zakresie**, na poziomie R1, z obowiązkowym przeglądem przez CPA/EA (§2, „Proces kontroli eksperckiej”);
  - zdrowie i koszty leczenia: ewentualny test na healthscorer.com (spójność z istniejącą marką i kontem AdSense, inny profil YMYL), nie na nowej domenie;
  - kredyty studenckie (oficjalny Loan Simulator);
  - opieka i starzenie (wysoki koszt eksperta, kontrowersyjny lead-gen [E-ADS-34]);
  - praca, relokacja i benefity (rodzina JOB): poza docelową granicą tematyczną (w CSV z uwagą „poza zakresem startowym domeny”);
  - mała firma i e-commerce (inna publiczność, B2B, inne reklamy): poza domeną; ewentualny test w istniejącym serwisie e-commerce właściciela, osobna domena dopiero po spełnieniu warunków 3 i 4 (niżej);
  - klify świadczeń dla gospodarstw o niskich dochodach;
  - ubezpieczenie zwierząt (INS-09), opieka nad dziećmi vs praca (LIFE-03), oddłużanie i upadłość konsumencka (FIN-06).
- **Warunki uzasadniające osobną domenę.** Osobna domena ma sens tylko wtedy, gdy spełnione są warunki **(1 lub 2) oraz 3 oraz 4**:
  1. kategoria ma **inną publiczność lub inny model monetyzacji** (np. e-commerce B2B, subskrypcja);
  2. kategoria ma **inny profil ryzyka** (zdrowie/medycyna, prawo);
  3. kategoria ma **zwalidowany popyt**: ≥ 3 symulatory z łącznie ≥ 5 tys. sesji ludzi/mies. albo ≥ 10% ruchu domeny (propozycja decyzyjna, nie norma rynkowa);
  4. istnieje **potencjał marki** (wzmianki, linki, zapytania brandowe), który osobna nazwa wzmocni.

  Przykład: symulatory e-commerce (BIZ-04, BIZ-01) pozostają poza tą domeną. Spełniają warunek 1, ale nie warunek 3, więc ewentualny test powinien się odbyć najpierw w istniejącym serwisie właściciela związanym z e-commerce (jeśli taki jest), a własna domena wchodzi w grę dopiero po spełnieniu warunków 3 i 4.

### 1.3 Pozycjonowanie w jednym zdaniu

Neutralne symulatory dużych decyzji kapitałowych gospodarstwa domowego w USA — dom, jego systemy, ubezpieczenie, kapitał w domu i auto — które w jednym rachunku łączą zależności pomijane przez pojedyncze kalkulatory i typowe odpowiedzi asystentów (ubezpieczenie, finansowanie, termin sprzedaży, podatki) i pokazują, przy jakich założeniach wynik się odwraca.

To, że typowe odpowiedzi asystentów pomijają te zależności, jest hipotezą (Z-12) do sprawdzenia w panelu asystentów (G0, krok 5); funkcje kalkulatorów konkurencji znamy tylko ze streszczeń wyszukiwarki.

Propozycja hasła na stronę (EN): *Neutral, assumption-transparent simulators for big home and car money decisions — compare your real options over time and see exactly what would flip the answer.*

## 2. ETAP H — architektura produktu

### Zasada nadrzędna: wiele symulatorów = kilkanaście silników + konfiguracja

Serwis nie powinien być zbiorem setek niezależnych aplikacji. Architektura ma pozwolić dodawać symulatory jako konfigurację, ale **to opis pojemności, a nie rekomendacja skali**: werdykt dopuszcza na start jeden symulator, a kolejne tylko według reguły dodawania narzędzi (§4.3). Proponowany podział na warstwy:

| Warstwa | Co zawiera | Kto/co ją zmienia | Częstotliwość zmian |
|---|---|---|---|
| 1. Prymitywy obliczeniowe (`engine-core`) | amortyzacja kredytu (stała/zmienna stopa, wcześniejsza spłata, refinansowanie), indeksacja/inflacja, NPV/IRR, podatek dochodowy (uproszczony moduł progów), amortyzacja podatkowa, degradacja wydajności, przepływy energii, rozkłady zdarzeń (awarie, szkody, pustostan) | programista + testy | rzadko |
| 2. Moduły domenowe (`modules/*`) | np. `roof`, `pv`, `battery`, `generator`, `mortgage`, `heloc`, `home-sale`, `insurance-policy`, `claim-history`, `vehicle`, `ev-charging`, `rental-unit`, `inventory-lot` — każdy z jawnie zadeklarowanymi wejściami, wyjściami i jednostkami | programista + przegląd merytoryczny | kwartalnie |
| 3. Zestawy danych i reguł (`rules/*`, `data/*`) | parametry podatkowe wg roku, taryfy, koszty jednostkowe, założenia rynkowe — każdy rekord z `effective_from`, `source_url`, `retrieved_at`, `reviewed_by`, `version` | n8n (pobranie) → testy → zatwierdzenie człowieka (tabela źródeł niżej) | od dni do roku |
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
| Prywatność | żądania tagów reklamowych i analitycznych nie zawierają wartości z formularza ani fragmentu `#…` (test sieciowy w środowisku testowym, z atrapą tagów) | zawsze |

### Oddzielenie obliczeń od LLM

- LLM (Claude Code) **pisze kod i testy** w trakcie budowy oraz **redaguje opisy** na podstawie struktury wyników. LLM nie wylicza liczb publikowanych na stronie i nie interpretuje przepisów bez źródła.
- Teksty generowane: szablon + sloty liczbowe wypełniane wynikami silnika; walidator odrzuca tekst zawierający liczbę spoza wyników/założeń.
- Każdy symulator ma stronę metodologii z listą założeń, źródeł, wersji danych i ograniczeń („czego ten model nie uwzględnia”).

### Prywatność danych finansowych

- Obliczenia w przeglądarce (silnik w TypeScript/WASM); wartości wpisane przez użytkownika nie są wysyłane na serwer.
- Analityka rejestruje zdarzenia (`tool_started`, `tool_completed`, `variant_view`, `export`) i co najwyżej zgrubne kubełki, nigdy wartości kwot ani adresów.
- Link do scenariusza: parametry w fragmencie URL (`#…`) nie trafiają do logów, referrera ani indeksu, więc `noindex` nie jest potrzebny; `noindex` stosujemy tylko wtedy, gdy parametry trafią do query string. Fragment jest jednak widoczny dla skryptów działających na stronie, dlatego obowiązuje zasada z podsekcji „Prywatność i zgody reklamowe”.
- Upload dokumentów (np. oferty ubezpieczeniowej) — tylko lokalne parsowanie w przeglądarce lub wcale w MVP.

### Prywatność i zgody reklamowe

Model przychodu opiera się na AdSense, więc warstwa reklamowa musi spełniać wymogi zgód od pierwszego dnia publikacji. Stan prawny poniżej pochodzi z rejestru dowodów; część wpisów to hipotezy z wiedzy modelu. Przed publikacją zakres obowiązków potwierdza prawnik (w economics.csv jednorazowy koszt polityki prywatności, regulaminu, CMP i audytu dostępności to 1 500 / 600 / 200 USD, kons. / baz. / opt.).

- **CMP dla EOG, UK i Szwajcarii (wymóg Google).** AdSense wymaga certyfikowanego przez Google CMP zintegrowanego z TCF, aby serwować reklamy spersonalizowane w EOG i UK (od 16.01.2024) oraz w Szwajcarii (od 31.07.2024); bez CMP reklamy spersonalizowane nie są tam serwowane [E-ADS-18]. Serwis jest adresowany do USA, ale jest anglojęzyczny, więc część ruchu przyjdzie z Europy. CMP (Google CMP albo inny certyfikowany) wdrażamy przed wnioskiem do AdSense. Wymóg TCF v2.3 od 01.03.2026 znamy tylko ze źródeł wtórnych [E-ADS-18].
- **Stany USA: GPC i RDP.** Trackery prawne podają, że 11–12 stanów wymaga honorowania Global Privacy Control (listy różnią się między trackerami) [E-ADS-19]; kompleksowe ustawy o prywatności ma ok. 19 stanów (hipoteza, wiedza modelu) [E-REG-27]. Od 1.01.2026 obowiązują ustawy w Indianie, Kentucky i Rhode Island; reklama targetowana wymaga w nich oceny DPIA [E-REG3-16]. Od 17.11.2025 AdSense sam odbiera sygnał GPC od użytkowników z Delaware i Oregonu i włącza tryb Restricted Data Processing (reklamy niespersonalizowane) [E-ADS-19]. Nie polegamy wyłącznie na tym automacie: CMP odczytuje GPC dla wszystkich stanów, w których jest wymagany, i przekazuje go do tagów; w AdSense włączamy RDP dla stanów z obowiązkiem. Wydawca narzędzia nie korzysta z wyłączenia GLBA (hipoteza) [E-REG-27].
- **Link „Do Not Sell or Share My Personal Information”** (albo równoważny mechanizm opt-out) w stopce i w CMP. To, czy i od kiedy jest wymagany, zależy od progów ustaw stanowych (np. IN i KY: ponad 100 tys. mieszkańców stanu albo ponad 25 tys. przy ≥ 50% przychodu ze sprzedaży danych; RI: ponad 35 tys. albo ponad 10 tys. przy ≥ 20% przychodu [E-REG3-16]; w Teksasie i Nebrasce bez progu wolumenowego — hipoteza [E-REG-27]) i od tego, czy reklamy personalizowane prawnik uzna za „sprzedaż” lub „udostępnianie” danych. Rekomendujemy wdrożenie od startu, bo koszt jest mały.
- **Wpływ na przychód.** W modelu odsłony z USA w trybie RDP to 15 / 10 / 5% (kons. / baz. / opt.), a ich RPM to 60 / 70 / 80% RPM reklam personalizowanych; to założenia, a testy branżowe bez ciasteczek pokazywały CPM niższe o 30–36% [E-ADS-35, economics.csv]. Udział odsłon bez monetyzacji (adblock, brak zgody, brak wypełnienia) mierzymy porównaniem odsłon GA4 i wyświetleń AdSense (Z-03).
- **Zakaz przekazywania wartości z formularzy do tagów reklamowych i analitycznych.** Wartości wpisane w symulatorze (kwoty, daty, ZIP, stan, warunki polisy, dane kredytu) nie trafiają do `dataLayer`, parametrów zdarzeń GA4, wymiarów niestandardowych, query stringu, tytułu strony ani do żądań reklamowych (np. par klucz–wartość). Ponieważ skrypty na stronie mogą odczytać pełny adres razem z fragmentem `#…`, przy otwarciu linku do scenariusza wartości z fragmentu przenosimy do formularza i usuwamy fragment z paska adresu (`history.replaceState`) przed załadowaniem tagów; analityce przekazujemy jawnie adres strony bez fragmentu. Każde wdrożenie przechodzi test sieciowy z tabeli „Testy”; testy E2E i monitoring nie wyświetlają prawdziwych reklam (ryzyko IVT [E-ADS-05]).
- **Minimalizacja danych.** Obliczenia po stronie klienta; w MVP brak kont i zapisu scenariuszy na serwerze; logi serwera zawierają tylko dane techniczne potrzebne do rozdzielenia botów i ludzi (adres URL, user-agent, czas, referrer), z ograniczonym czasem przechowywania (propozycja: 90 dni) i skróconym IP w raportach.
- **Polityka prywatności** opisuje reklamy Google, CMP, obsługę GPC i opt-out oraz zasadę, że wartości z formularza nie opuszczają przeglądarki.

### Dostępność i mobile

- WCAG 2.2 AA: etykiety pól, obsługa klawiatury, kontrast, wykresy z tabelą alternatywną. WCAG 2.1/2.2 AA jest w USA de facto standardem w sporach o dostępność cyfrową (hipoteza, wiedza modelu) [E-REG-28]. Ryzyko sporów jest realne: w 2025 r. w sądach federalnych złożono 3 117 pozwów o dostępność stron, o 27% więcej niż w 2024 r. (dane kancelarii Seyfarth Shaw) [E-REG3-17].
- Formularz progresywny: tryb „szybki” (5–8 pól z presetami) i „pełny” (wszystkie założenia). Mobile-first, bo ruch z aplikacji asystentów jest w dużej części mobilny (hipoteza do zmierzenia).
- Reklamy nie mogą przesuwać formularza (CLS) ani sąsiadować bezpośrednio z przyciskami (polityka przypadkowych kliknięć).

### Strony indeksowalne: kiedy osobne narzędzie, preset, parametr, strona

| Sytuacja | Rozwiązanie |
|---|---|
| Inna decyzja, inne warianty, inna kolejność zdarzeń lub inny model obliczeń | **osobny symulator** (osobna specyfikacja, osobna strona) |
| Ta sama decyzja, ale typowy profil użytkownika z innymi wartościami domyślnymi (np. „dach asfaltowy 20 lat, sprzedaż za 3 lata”) | **preset** w tym samym symulatorze (bez osobnej strony) |
| Liczba, data, miasto, wiek, kwota | **parametr** (nigdy osobna strona) |
| Ta sama decyzja, ale udokumentowana, odrębna intencja wyszukiwania/pytania z innym językiem problemu (np. „solar lease vs buy when selling house”) i ≥1 wariant/ograniczenie różni się istotnie | **osobna indeksowalna strona-wejście** z własnym presetem i treścią, kanonicznie odrębna — tylko wtedy, gdy pomiar popytu pokaże osobny klaster fraz (np. w G0, krok 2) |
| Region z istotnie innymi regułami (np. stan z inną taryfą net metering) | parametr + zestaw danych; osobna strona dopiero, gdy reguły zmieniają ranking wariantów i jest dowód popytu |

Zakaz: automatyczne generowanie stron dla kombinacji parametrów (miasto × kwota × rok). Polityka Google „scaled content abuse” obejmuje masowe tworzenie stron służących głównie manipulowaniu rankingiem, niezależnie od sposobu ich stworzenia; Google nie publikuje progu liczby stron [E-ADS-06, E-POR2-11].

### Jak kilka modeli obsługuje bardzo wiele pytań

Pytanie użytkownika = (typ decyzji) × (wartości parametrów) × (kontekst). Liczba możliwych kombinacji parametrów jest praktycznie nieograniczona, ale **popyt nie jest równy liczbie kombinacji**. Jeden symulator „roof + solar + sale timing” obsługuje zarówno „roof 18 years old, selling in 3 years, Texas”, jak i „roof 8 years old, staying 15 years, California” — bez osobnych stron. Pojemność serwisu mierzy się liczbą odrębnych **typów decyzji z realnym popytem**, a nie liczbą odpowiedzi. Setki typów decyzji to w najlepszym razie horyzont wieloletni, a nie plan; ruch będzie skrajnie nierówny (rozkład potęgowy — założenie w economics.csv), a tempo rozbudowy wyznacza reguła dodawania narzędzi (§4.3).

### Układ strony pod politykę reklam i czytelność dla AI

- **Sloty reklamowe** tylko poza strefą sterowania: nad nagłówkiem, pod sekcją wyników/porównania, w bocznej kolumnie na desktopie, między sekcjami metodologii. Nigdy obok przycisków „Compare”, suwaków ani zakładek wariantów (polityka „Ads interfering” [E-ADS-03]). Bez reklam na ekranach pośrednich („calculating…”) i na stronach bez treści [E-ADS-02].
- **Bez odświeżania reklam po przeliczeniu.** AdSense nie pozwala odświeżać strony ani jej elementów, w tym reklam, bez żądania użytkownika; odświeżanie czasowe dopuszcza tylko Ad Manager/AdX [E-VER-C7, E-ADS-04]. Nie budujemy modelu na „przeliczenie = nowe wyświetlenie” bez potwierdzenia u Google (K-06).
- **Kod reklam w głównym dokumencie**, nie w iframe ani widgecie osadzanym u innych [E-ADS-04].
- **Treść czytelna bez JS:** nagłówek z pytaniem decyzyjnym, 3–5 zdań odpowiedzi „to zależy od…” z progami przełączenia dla domyślnego presetu, tabela przykładowych scenariuszy, założenia i źródła danych — wszystko w HTML renderowanym po stronie serwera (SSG). W teście Ahrefs (1 885 stron; 5 systemów, w tym ChatGPT i Perplexity) systemy wyciągały tylko widoczny HTML, a JSON-LD był ignorowany; Bing (Copilot) deklaruje, że schema pomaga; pozostałe dane to korelacje (pewność niska) [E-POR2-14]. Wniosek: kluczowa treść w widocznym HTML, JSON-LD jako tani dodatek. Badania nie wykazały efektu `llms.txt` [E-POR2-13]. Według jednego badania ok. 44% cytowań ChatGPT pochodzi z pierwszych 30% tekstu (korelacja, pewność niska; dla innych asystentów nie badano) [E-AI-14]; wnioski i tak umieszczamy na górze strony, bo to tania zmiana, ale nie traktujemy tej korelacji jako reguły dla wszystkich asystentów.
- **robots.txt i CDN:** wpuścić `Googlebot`, `Bingbot`, `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`, `Claude-SearchBot`, `Claude-User`. `GPTBot` i `ClaudeBot` (trening) nie wpływają na wyszukiwanie w ChatGPT i Claude; ich blokada to osobna decyzja. `Google-Extended` nie wpływa na Google Search, AIO ani AI Mode, ale steruje groundingiem w aplikacji Gemini: blokada usuwa stronę z odpowiedzi Gemini [E-AI-22, E-AI-25]. Nie blokujemy `Google-Extended`, jeśli Gemini ma być kanałem. W Cloudflare świadomie zmieniamy domyślne blokady botów „Agent/Training” na stronach z reklamami; uwaga: crawlery wielozadaniowe (Googlebot, Bingbot, Applebot) podlegają regule Training, więc taka blokada może wyłączyć także indeksowanie [E-VER-C11]. Własne testy E2E i monitoring wykluczamy z wyświetlania reklam (ryzyko IVT [E-ADS-05]).

### Analityka źródeł AI i monetyzacji

- Klasyfikacja źródła wizyty: referrer (`chatgpt.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com`, `claude.ai`), `utm_source=chatgpt.com` i podobne, brak referrera (aplikacje mobilne — część ruchu AI wpada do „Direct”). Około 8–15.10.2026 linki z ChatGPT straciły UTM, a referrera nadal brakuje w większości kliknięć z ChatGPT także po poprawce [E-VER-C12]. Ruch AI mierzony referrerem i UTM jest więc zaniżony; jako wskaźnik pośredni śledzimy udział „Direct” na podstronach narzędzi.
- Logi serwera: osobna ewidencja botów pobierających strony na żądanie użytkownika (np. `ChatGPT-User`, `Perplexity-User`, `Claude-User`), crawlerów indeksujących (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`, `Bingbot`, `Googlebot`) i treningowych (`GPTBot`, `ClaudeBot`, `Google-Extended` jako token). Pobranie przez bota „user” ≠ wizyta człowieka.
- Lejek per strona i źródło: wejście → `tool_started` → `tool_completed` → odsłony reklam → przychód (kanały URL w AdSense lub raport wg stron).
- Monitoring obecności w asystentach: stała pula promptów (§5), wykonywana ręcznie lub przez oficjalne API z wyszukiwaniem, z zapisem daty, platformy, trybu, odpowiedzi i linków; wyniki raportowane osobno dla każdej platformy; świadomość, że wyniki API ≠ wyniki aplikacji konsumenckiej.

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

**Próg akceptacji (propozycja):** automatyczne wdrożenie tylko wtedy, gdy na żadnym złotym przypadku nie zmienia się ranking wariantów, a wynik główny zmienia się o mniej niż 2%; w przeciwnym razie decyduje człowiek.

**Źródła danych pilotażu i częstotliwość aktualizacji.** Cykl publikacji podajemy tylko tam, gdzie wynika z rejestru dowodów lub z opisu źródła; pozostałe trzeba potwierdzić przed budową. Licencje sprawdzamy dla każdej serii osobno [E-REG-21, E-REG3-11].

| Źródło (produkt) | Cykl publikacji źródła | Cron n8n (propozycja) | Kto zatwierdza zmianę |
|---|---|---|---|
| Freddie Mac PMMS / FRED `MORTGAGE30US` (HOME-04, HOME-02, moduł finansowania) | co tydzień, w czwartek; wymagana atrybucja (hipoteza) [E-REG-22] | co tydzień | automatycznie w progu; powyżej progu właściciel (R3) |
| Prime rate i marże HELOC (moduł finansowania) | do potwierdzenia | co miesiąc | automatycznie w progu; powyżej progu właściciel (R3) |
| EIA: ceny prądu i gazu wg stanu, STEO (RENO-03, AUTO-01) | co miesiąc [E-REG-21, E-REG3-10] | co miesiąc | automatycznie w progu; powyżej progu właściciel (R2) |
| Ceny benzyny (AAA/EIA) i fueleconomy.gov (AUTO-01) | do potwierdzenia; fueleconomy.gov udostępnia usługi REST bez klucza [E-REG3-10] | co miesiąc | automatycznie w progu; powyżej progu właściciel (R2) |
| Fed G.19, oprocentowanie kredytów samochodowych (AUTO-01) | do potwierdzenia | co miesiąc | automatycznie w progu; powyżej progu właściciel (R3) |
| Edmunds, raporty o ujemnym kapitale (AUTO-01, presety) | raporty kwartalne | n8n tworzy zadanie co kwartał | właściciel |
| FHFA HPI (HOME-02, HOME-04) | do potwierdzenia | co kwartał | właściciel (R3) |
| Czynsze: Zillow ZORI / ACS (HOME-02) | ACS 1-year ok. IX, 5-year ok. XII [E-REG-21]; licencja Zillow niezweryfikowana [E-REG3-12, E-REG-23] | po potwierdzeniu licencji; ACS raz w roku | właściciel |
| Verisk Roof Report: koszty wymiany i naprawy dachu (RENO-02) | raport roczny (wydanie 2026 z danymi za 2025) | n8n tworzy zadanie raz w roku | właściciel; dekarz przy zmianie zakresów domyślnych (R2) |
| Remodeling Cost vs Value (RENO-02, HOME-04) | do potwierdzenia | raz w roku (zadanie) | właściciel (R2) |
| FEMA NRI / OpenFEMA (RENO-02, poza MVP) | wersję NRI sprawdzić przed budową; OpenFEMA bez klucza, z wymaganą klauzulą o źródle [E-REG3-10] | sprawdzenie wersji co kwartał | właściciel (R2) |
| NOAA Climate Normals / NREL TMY, NEEP Cold-Climate ASHP List, AHRI (RENO-03) | do potwierdzenia | co kwartał | właściciel; modelarz energetyczny przy zmianie metody (R2) |
| Lincoln Institute 50-State Property Tax (HOME-04) | do potwierdzenia | raz w roku (zadanie) | właściciel (R3) |
| IRS: Pub 523, 527, 946, Form 4797, parametry roczne (HOME-02, HOME-04) | parametry IRS raz w roku, ok. X–XI (hipoteza) [E-REG-22] | monitoring IRS newsroom i Federal Register → zadanie | CPA/EA (R1) |
| FS 627.7011(5) i inne reguły stanowe ubezpieczeń (RENO-02) | nieregularnie (zmiany ustaw i regulacji) | monitoring komunikatów regulatorów → zadanie | licencjonowany agent lub underwriter P&C (R1) |
| Podatek od sprzedaży auta i ulga trade-in, 51 jurysdykcji (AUTO-01) | nieregularnie; tabela zbierana ręcznie ze stron departamentów skarbowych | sprawdzenie co kwartał → zadanie | CPA ds. sales tax (R1) |

### Rola VPS

- Serwowanie statycznego serwisu (Caddy/Nginx) za CDN; strony są statyczne, więc VPS nie jest wąskim gardłem.
- n8n, zadania pobierania danych, analiza logów (boty AI vs ludzie), kopie zapasowe.
- CI (testy silnika) — w GitHub Actions lub na VPS; deploy tylko z zielonych testów.
- Brak przetwarzania danych finansowych użytkowników po stronie serwera.

### Proces kontroli eksperckiej

| Poziom ryzyka | Przykłady | Kontrola |
|---|---|---|
| R1 — przepisy i pieniądze z konsekwencjami prawnymi | podatki (w tym moduły wbudowane w decyzje: §121, recapture, step-up, podatek od sprzedaży auta), zasiłki, Medicare/ACA, wypłaty emerytalne, ubezpieczenia (logika ACV/RCV, harmonogramy, nieodnowienia) | ekspert zewnętrzny (EA/CPA/CFP lub licencjonowany agent) przed publikacją i po zmianach reguł |
| R2 — założenia techniczne | produkcja PV, zapotrzebowanie mocy, koszty remontów | walidacja względem narzędzi referencyjnych + przegląd fachowca przy starcie |
| R3 — finanse ogólne | harmonogramy kredytu, NPV, płynność | testy porównawcze, bez stałego eksperta |

Recenzja jest zapisana w repozytorium (kto, kiedy, jaka wersja, co sprawdzono) i widoczna na stronie metodologii.

### Ryzyko prawne

Poniższe ustalenia to w większości hipotezy z wiedzy modelu albo dane pośrednie; nie są poradą prawną. Przed publikacją RENO-02 prawnik przegląda disclaimery, regulamin, politykę prywatności i CMP.

- **Wyłączenie wydawcy (publisher exclusion) a doradztwo.** Publikacje bezosobowe, rzetelne (bona fide) i w regularnym, ogólnym obiegu są objęte wyłączeniem wydawcy z sekcji 202(a)(11)(D) Advisers Act (Lowe v. SEC); poza nim jest porada dopasowana do portfela lub potrzeb konkretnego klienta [E-REG3-13, E-REG-24]. Nie znaleziono rozstrzygnięć dotyczących interaktywnych kalkulatorów, więc zastosowanie tej reguły do symulatorów to hipoteza [E-REG3-13]. Decyzje o dachu, HVAC, aucie czy ubezpieczeniu zasadniczo leżą poza Advisers Act (hipoteza [E-REG-24]); ryzyko rośnie, gdy wynik dotyczy inwestowania (np. wariant „sprzedaj i zainwestuj” w HOME-02). Zasady: (a) wynik to porównanie wariantów i progi przełączenia przy jawnych założeniach, a nie polecenie „zrób X”; (b) stopę zwrotu z inwestycji wpisuje użytkownik, a serwis nie wskazuje konkretnych papierów wartościowych, funduszy ani produktów; (c) brak relacji jeden na jeden (konsultacji, spersonalizowanych e-maili z rekomendacjami); (d) treść i metodologia są publiczne i aktualizowane regularnie.
- **Ryzyko „insurance producer”.** Zabieganie o klienta, negocjowanie lub sprzedaż ubezpieczenia wymaga licencji producenta w każdym stanie, a ogólne treści edukacyjne i porównania koncepcyjne zwykle jej nie wymagają; prowizja zależna od sprzedaży polisy wymaga licencji (hipoteza [E-REG-25]). Model NAIC 218 dopuszcza opłaty dla osób bez licencji, o ile nie sprzedają, nie zabiegają o klienta i nie negocjują; regulator ocenia całość zachowania, a w stanie Waszyngton strony z recenzjami bez licencji, które zabiegają o mieszkańców, naruszają kodeks ubezpieczeniowy [E-REG3-14]. Zasady dla RENO-02 i przyszłych produktów INS: **nie sprzedawać ani nie polecać konkretnych polis, ubezpieczycieli ani agentów**; nie porównywać składek nazwanych ubezpieczycieli; warunki polisy (ACV/RCV, harmonogram wypłat, udział własny) wpisuje użytkownik, a wynik pokazuje skutki tych założeń, zamiast interpretować umowę; przy wynikach odesłanie „sprawdź warunki u swojego agenta lub ubezpieczyciela”; żadnych płatnych leadów ani prowizji ubezpieczeniowych bez osobnej opinii prawnej.
- **Disclaimery i regulamin.** Przy wynikach każdego symulatora krótkie zastrzeżenie (wersja angielska do akceptacji prawnika): narzędzie edukacyjne; nie jest poradą finansową, podatkową, prawną ani ubezpieczeniową; wynik zależy od wpisanych danych i jawnych założeń; przy decyzji skonsultuj się z licencjonowanym specjalistą. W regulaminie: ograniczenie odpowiedzialności, brak relacji doradczej, data i wersja danych (`ruleset_version`). Ewentualne linki afiliacyjne (poza modelem bazowym) wymagają ujawnienia „clear and conspicuous” blisko linku (hipoteza [E-REG-26]). Jeśli serwis kiedyś pokaże opinie lub rekomendacje użytkowników, obowiązuje Consumer Reviews and Testimonials Rule FTC (od X 2024): w XII 2025 FTC wysłała pierwsze listy ostrzegawcze z groźbą kar do 53 088 USD za naruszenie [E-REG3-15].
- **Przegląd R1.** Moduły podatkowe (§121, recapture, step-up, podatek od sprzedaży auta) sprawdza CPA/EA przed publikacją i po każdej zmianie reguł; logikę ubezpieczeniową RENO-02 sprawdza licencjonowany agent lub underwriter P&C (K-07). Eskalacja do prawnika jest obowiązkowa przed: dodaniem lead-genu lub afiliacji w ubezpieczeniach albo kredytach (także zgody TCPA); funkcją zbierającą dane kontaktowe; wynikami wskazującymi konkretne produkty lub firmy; odpowiedzią na pismo regulatora lub skargę.

## 3. Pilotaż: pięć produktów (start tylko od RENO-02)

Start projektu to wyłącznie **RENO-02** jako test opcji. Produkty 2–5 to kandydaci warunkowi. Każdy z nich przed budową wymaga: (a) własnego pomiaru popytu i SERP jak w G0, kroki 2–3 (Keyword Planner i Google Trends dla 10–20 fraz produktu, z 12-miesięcznym profilem sezonowym; te same progi co w §4.2, czyli propozycje decyzyjne); (b) ręcznej weryfikacji konkurencji (reguła z G0, krok 4: produkt odpada, jeśli jedno narzędzie pokrywa ≥ 3 jego kluczowe zależności); (c) spełnienia reguły dodawania narzędzi (§4.3). Każdy ma też własny zegar od indeksacji. „Pilot” w CSV oznacza kandydata do pilotażu po bramkach, nie decyzję o budowie. Kolejność wynika z zależności modułów: każdy kolejny produkt dokłada 1–2 nowe moduły i używa wcześniejszych. Szczegółowe wejścia, warianty, źródła danych i prompty — w kartach w `top-10-products.md`. **Pracochłonność i godziny eksperta to szacunki** (właściciel pracuje z Claude Code; zakresy przeglądu eksperckiego i godziny podali agenci fali 2b w kartach produktów). Przegląd ekspercki finansujemy **etapami**: kolejny produkt dostaje eksperta dopiero po decyzji „Kontynuować” dla RENO-02 i przy spełnionej regule dodawania narzędzi (§4.3), więc gotówka wydawana na start to tylko test opcji RENO-02 (w bazie ok. 5,9 tys. USD do publikacji: prawo/CMP, ekspert RENO-02 i koszty stałe za okres budowy; §4.2).

| # | Produkt | Minimalny wartościowy zakres (MVP) | Świadomie odłożone | Źródła danych i testy obliczeń | Ekspert (szac.) | Pracochłonność właściciela (szac.) |
|---|---|---|---|---|---|---|
| 1 | **RENO-02** Aging Roof: Replace, Repair, Fortify or Wait — test opcji nr 1 i warunek startu projektu | 5 wariantów (wymiana teraz; naprawa + wymiana za N lat; czekanie z samoubezpieczeniem i wypłatą ACV; wymiana przed wystawieniem domu; sprzedaż as-is z kredytem dla kupującego) + przełącznik PV (koszt demontażu i ponownego montażu). Wejścia: wiek i materiał dachu, zakres pozostałej żywotności, wyceny, RCV/ACV/harmonogram wypłat (edytowalna tabela), udział wiatr/grad kwotowy lub %, składka i dopłata za wiek, p(nieodnowienie), horyzont sprzedaży, finansowanie. Wyniki: oczekiwany koszt do daty sprzedaży, próg roku wymiany, tornado, lista założeń | ryzyko gradu na poziomie ZIP/hrabstwa (FEMA NRI, NOAA); biblioteka harmonogramów ubezpieczycieli (SERFF); Monte Carlo; pełna ekonomika PV; reguły stanowe poza FL | Verisk 2026 Roof Report (koszty 2025), poradniki kosztu demontażu PV, FS 627.7011(5) (FL), Remodeling Cost vs Value; FEMA NRI (wersję sprawdzić przed budową). Testy: złote przypadki ręczne (ACV, harmonogram, udział %), własności (wyższe p szkody → wcześniejsza wymiana nie jest droższa), brzegowe (sprzedaż w roku 0) | agent lub underwriter P&C 6–10 h; dekarz lub inspektor dachów 4–6 h; agent nieruchomości lub rzeczoznawca 3–5 h; CFP lub analityk finansowy 3–4 h; instalator PV 2–3 h; przegląd prawny disclaimerów ok. 2 h (może się pokrywać z jednorazowym kosztem prawa/CMP) — razem ok. 20–30 h | 50–70 h (w tym moduły: dach, ubezpieczenie, sprzedaż, finansowanie) + silnik 90–220 h; razem 140–290 h |
| 2 | **RENO-03** AC or Furnace Just Died: Repair vs Like-for-Like vs Heat Pump vs Dual-Fuel — dopiero po wyniku RENO-02, pomiarze popytu i SERP oraz ręcznej weryfikacji konkurencji | 6 wariantów: naprawa z odroczeniem 1–3 lat; AC 1:1; dual-fuel (HP + istniejący piec, ekonomiczny punkt przełączania); HP z grzałką; cold-climate HP; wymiana obu urządzeń. Wejścia: ZIP/stan (ceny EIA, klimat z 20–25 miast reprezentatywnych), wiek urządzeń, paliwo, wycena naprawy, zużycie gazu, AFUE/SEER; opcjonalnie panel 100/150/200 A, horyzont, eskalacja, rabaty wpisywane ręcznie | mini-split; silnik ulg (Rewiring America API, HEAR); taryfy TOU (URDB); Manual J; olej opałowy; PV | EIA (ceny prądu i gazu wg stanu), NOAA Climate Normals / NREL TMY (rozkład temperatur), NEEP Cold-Climate ASHP List, AHRI; testy porównawcze z kalkulatorami ENERGY STAR i Rewiring America; złote przypadki „metoda bin” | wykonawca HVAC lub technik NATE 6–10 h; inżynier lub modelarz energetyczny 8–12 h; specjalista od ulg (CPA/EA lub program stanowy) 2–3 h; opcjonalnie analityk taryf 2 h — razem ok. 16–27 h | 40–60 h (nowe moduły: energia/klimat, urządzenie) |
| 3 | **HOME-04** Remodel vs. Move (Rate Lock-In Aware) — pilot warunkowy (luka obniżona w kalibracji 3→2) | warianty: zostać + projekt (rozbudowa/piwnica/ADU) z finansowaniem HELOC / home equity loan / gotówka / cash-out refi; przeprowadzka z nowym kredytem (koszty sprzedaży i zakupu, nowy podatek od nieruchomości); baseline. Wyniki: przepływy, majątek netto na koniec horyzontu, break-even, rozbicie „skąd różnica” (stopa, podatek, transakcje, remont), wrażliwość | kredyt assumable; podatek od nieruchomości 50 stanów (MVP: wpis + presety CA/FL); pełny podatek dochodowy; dochód z ADU; kredyty budowlane | Freddie Mac PMMS, prime rate + marże, FHFA (rozkład stóp), Lincoln Institute 50-State Property Tax, IRS Pub 523/936; testy: harmonogramy kredytów vs arkusz/CFPB, złote przypadki „kara za utratę stopy” | loan officer NMLS 4–6 h; CPA/EA 3–5 h; kosztorysant lub wykonawca remontów 3–4 h; agent nieruchomości lub rzeczoznawca 2–4 h; specjalista podatku od nieruchomości (presety CA i FL) 2–3 h; opcjonalnie CFP lub prawnik/compliance 2–3 h — razem ok. 16–25 h przed startem; aktualizacje ok. 2–4 h kwartalnie | 30–45 h (reużywa finansowania i sprzedaży; nowe: remont, podatek lokalny) |
| 4 | **HOME-02** Sell vs. Rent Out When Moving (Exclusion Clock & Low-Rate Value) — pilot warunkowy; TrueHomeCosts, Bellhaven i TeamzLab mogą pokrywać część luki (fala 2b) | (A) „zegar wyłączenia §121”: ostatnia bezpieczna data zamknięcia, zalecana data wystawienia, ostrzeżenia (częściowe wyłączenie, MFJ, extended duty), plik .ics; (B) 4 warianty w horyzoncie do 10 lat: sprzedaż teraz i inwestycja; najem N lat i sprzedaż przed terminem; najem długoterminowy i sprzedaż po utracie wyłączenia; samodzielny zarząd vs firma zarządzająca; (C) podatki uproszczone, ale poprawne co do struktury (amortyzacja 27,5 roku, recapture, LTCG) | najem średnioterminowy; podatki stanowe; pełne NIIT/PAL/AMT; 1031; kredyt assumable | IRS Pub 523, 527, 946, Form 4797, IRC §121; PMMS; FHFA HPI; Zillow ZORI/ACS (czynsze — sprawdzić licencję [E-REG3-12]); złote przypadki G1–G9 zatwierdzone przez CPA | **CPA/EA 6–10 h (bez tego nie publikować)**; loan officer lub underwriter 2–4 h; property manager lub broker najmu 2–3 h — razem ok. 10–17 h; z opcjonalnymi (CFP 2–3 h, prawnik od nieruchomości 1–2 h) ok. 13–22 h; coroczna rewizja CPA ok. 2–4 h | 35–50 h (nowe: podatek od sprzedaży i amortyzacja najmu) |
| 5 | **AUTO-01** Underwater Car Loan Exit Planner (Keep, Trade Now, Wait, or Pay the Gap) — pilot warunkowy, test drugiej puli popytu | 6 wariantów na miesięcznej osi czasu (36–84 mies.): zatrzymaj do dodatniego kapitału; wymień teraz z przeniesieniem długu; wymień i dopłać lukę; sprzedaj prywatnie i weź pożyczkę na lukę; refinansuj i zostań; poczekaj N miesięcy (suwak 0–24). Wejścia: payoff, APR, wartość trade-in i private party, presety deprecjacji, stan (tabela 51 jurysdykcji: podatek i ulga trade-in), nowe auto, ładowanie w domu, gotówka, limit raty. EV jako typ napędu | leasing z ujemnym kapitałem; wyceny na żywo (KBB/Edmunds API — licencje); macierz APR wg scoringu i gap insurance; podatek lokalny po ZIP; ulga odsetkowa OBBBA tylko jako informacja z datą | Edmunds (raporty kwartalne), CFPB Data Spotlight, fueleconomy.gov, EIA (prąd), AAA/EIA (benzyna), Fed G.19 (APR); tabela podatków ze stron departamentów skarbowych (do zebrania); testy amortyzacji vs arkusz; własności (wyższa deprecjacja → późniejszy miesiąc przecięcia) | specjalista finansowania aut (F&I lub CFP) 8–12 h; CPA ds. sales and use tax 10–14 h na start (+ ok. 3–4 h rocznie); recenzent ilościowy lub aktuarialny 4–6 h; prawnik lub compliance 2–4 h — razem ok. 24–36 h | 30–40 h (nowe: auto, podatek od sprzedaży auta) |

Łącznie, szacunkowo (suma zakresów z tabeli): **silnik 90–220 h + 5 produktów 185–265 h** pracy właściciela oraz **ok. 86–135 h eksperta** według kart agentów fali 2b (RENO-02 20–30 h, RENO-03 16–27 h, HOME-04 16–25 h, HOME-02 10–17 h, AUTO-01 24–36 h), finansowane etapami.

**Jak tabela ma się do modelu w economics.csv.** Model przyjmuje (kons. / baz. / opt.): silnik 220 / 155 / 90 h; RENO-02 70 / 60 / 50 h czasu właściciela (osobne wejście, bo RENO-02 buduje moduły wspólne: dach, ubezpieczenie, sprzedaż, finansowanie); każde kolejne narzędzie 53 / 45 / 37 h. Godziny eksperta: RENO-02 30 / 25 / 20 h, każde kolejne narzędzie 27 / 22 / 17 h (średnia z kart fali 2b: 86–135 h dla 5 pilotów, czyli 17–27 h na narzędzie), utrzymanie eksperckie 12 / 6 / 3 h na narzędzie rocznie (karty: HOME-04 ok. 2–4 h kwartalnie, HOME-02 ok. 2–4 h rocznie, AUTO-01 ok. 3–4 h rocznie, RENO-02 coroczny przegląd kosztów; część to założenie). Daje to dla silnika i 5 symulatorów 502 / 395 / 288 h czasu właściciela (kons. 502 h przekracza sumę z tabeli 275–485 h, bo 53 h na narzędzie to zapas ponad średnią z kart produktów 2–5: 30–60 h, średnio ok. 34–49 h) oraz gotówkę (prawo/CMP i eksperci, bez kosztów stałych) ok. 36 / 20,4 / 11,2 tys. USD. Godziny eksperta wynoszą od 10–17 h (HOME-02) do 24–36 h (AUTO-01), więc AUTO-01 może przekroczyć założenie konserwatywne 27 h. Test opcji (silnik + RENO-02) to w modelu 290 / 215 / 140 h, a z G0 (25–35 h) ok. 315–325 / 240–250 / 165–175 h. Wariant konserwatywny przekracza więc limit ok. 300 h (§4.4, pkt 4). Dlatego zakres MVP RENO-02 trzeba pilnować, a przekroczenie limitu traktować jako sygnał przerwania, a nie powód do jego podniesienia.

### 3.1 Kluczowa hipoteza, miary i warunek zatrzymania (dla każdego produktu)

Zegar każdego produktu liczymy **od jego indeksacji** w Google i Bing (nie od publikacji); jeśli 60 dni po publikacji strony nadal nie ma w indeksie Google i Bing, zegar liczymy od publikacji (reguła awaryjna, §4.3). Progi to **propozycje decyzyjne**, nie normy rynkowe. Wszystkie produkty podlegają wspólnym progom z §4.3 (progi ruchu po korekcie sezonowej): **90 dni od indeksacji** — ≥ 500 wyświetleń GSC/mies., CTR ≥ 1,5%, `tool_completed`/`tool_started` ≥ 35%; **6 mies. od indeksacji** — zmierzony przychód ≥ 5 USD na 1000 sesji ludzi, ≥ 3 tys. sesji ludzi/mies. z trendem ≥ +15% m/m przez 3 mies. i spełniona reguła dodawania narzędzi. **Monetyzację** każdego produktu raportujemy od pierwszych 2 000 odsłon (odczyt kierunkowy): page RPM (USA i ogółem) oraz przychód na 1000 sesji ludzi, z korektą sezonową (§4.3). Tabela poniżej dodaje miary specyficzne dla hipotezy produktu; nie zastępują one progów z §4.3.

| Produkt | Kluczowa hipoteza | Przed budową | 90 dni od indeksacji (miary dodatkowe) | 6 mies. od indeksacji (monetyzacja) | Warunek zatrzymania produktu |
|---|---|---|---|---|---|
| RENO-02 | Właściciele, którzy dostają od ubezpieczyciela zmianę warunków dla starego dachu (ACV, harmonogram, nieodnowienie) albo planują sprzedaż, szukają rachunku „wymienić teraz czy czekać” (hipoteza). Symulator pomija mniej zależności niż odpowiedź asystenta (hipoteza Z-12) | bramka G0 (§4.2): kroki 2, 3 i 4 spełnione jednocześnie | cytowania w panelu (§5) i w Bing AI Performance, osobno dla każdej platformy; test porównawczy: czy asystenci pomijają ≥ 2 zależności (ACV/harmonogram, horyzont sprzedaży, demontaż PV) | przychód ≥ 5 USD/1000 sesji ludzi; page RPM USA na stronie z formularzem porównany z założeniem 2,4 / 8 / 18 USD (kons. / baz. / opt.) | warunek przerwania projektu (§4.4, pkt 1–4). Sygnał ostrzegawczy, nie osobny warunek: asystenci w ≥ 90% uruchomień dają pełne porównanie wariantów bez linków |
| RENO-03 | Awaria generuje pilne, mobilne sesje; użytkownik chce porównać 4–6 dróg w kilka minut (hipoteza). Reklamodawcy usług HVAC mogą płacić wysokie stawki w wyszukiwarce, ale to warstwa CPC reklamodawcy, a nie page RPM serwisu (do pomiaru) | wynik RENO-02 („Kontynuować”); pomiar popytu i SERP jak w G0, kroki 2–3 (10–20 fraz produktu, profil sezonowy z Trends; progi z §4.2); ręczna weryfikacja konkurencji z karty (reguła ≥ 3 zależności); reguła dodawania narzędzi | udział mobile ≥ 50% (test hipotezy pilności); ≥ 1 cytowanie w panelu lub w Bing AI Performance. Sezonowości popytu (awarie podczas upałów i mrozów) w economics.csv nie modelowano; progi ruchu porównujemy po korekcie o indeks sezonowy z Google Trends (§4.3) | przychód ≥ 5 USD/1000 sesji ludzi; page RPM USA | wspólny warunek (niżej); dodatkowo: ukończenie < 15% po 2 iteracjach formularza („tryb szybki”) w ciągu 3 mies. od decyzji „Zmodyfikować” |
| HOME-04 | Efekt zamrożenia stóp tworzy pytania „remont czy przeprowadzka”, a rozbicie „kary za utratę stopy” wyróżnia produkt, bo asystenci nie liczą go spójnie (hipoteza; luka obniżona w kalibracji 3→2) | pomiar popytu i SERP jak w G0, kroki 2–3 (10–20 fraz produktu, profil sezonowy z Trends; progi z §4.2); ręczna weryfikacja konkurencji z karty (reguła ≥ 3 zależności); reguła dodawania narzędzi | ≥ 1 cytowanie w panelu lub w Bing AI Performance; udział sesji, w których użytkownik otworzył rozbicie „skąd różnica” (`variant_view`) | przychód ≥ 5 USD/1000 sesji ludzi; page RPM USA | wspólny warunek (niżej) |
| HOME-02 | Moduł „zegar §121” (data graniczna liczona od daty wyprowadzki) to potencjalnie wyróżniający, cytowalny wynik (TrueHomeCosts, Bellhaven i TeamzLab do weryfikacji), który może zwiększyć szansę na link z asystenta lub forum mimo zatłoczonej kategorii „rent vs sell” (hipoteza) | pomiar popytu i SERP jak w G0, kroki 2–3 (10–20 fraz produktu, profil sezonowy z Trends; progi z §4.2); ręczna weryfikacja TrueHomeCosts, Bellhaven i TeamzLab (fala 2b: konkurenci częściowi); produkt odpada, jeśli jedno narzędzie pokrywa ≥ 3 kluczowe zależności z karty (np. zegar §121, recapture, wartość niskiej stopy, warianty najmu i sprzedaży); przegląd CPA/EA przed publikacją | ≥ 2 cytowania w panelu lub w Bing AI Performance (test hipotezy cytowalności) | przychód ≥ 5 USD/1000 sesji ludzi; page RPM USA | wspólny warunek (niżej) |
| AUTO-01 | Auta to druga pula popytu, niezależna od domu (hipoteza). Integracja 6 wariantów może się wyróżniać mimo wielu prostych kalkulatorów ujemnego kapitału (np. CarCalcPro: konkurent częściowy, do ręcznej weryfikacji). Koszt ekspercki nie jest niski: ok. 24–36 h | pomiar popytu i SERP jak w G0, kroki 2–3 (10–20 fraz produktu, profil sezonowy z Trends; progi z §4.2); ręczna weryfikacja konkurencji z karty (reguła ≥ 3 zależności); reguła dodawania narzędzi | ≥ 1 cytowanie w panelu lub w Bing AI Performance | przychód ≥ 5 USD/1000 sesji ludzi; page RPM USA | wspólny warunek (niżej); dodatkowo: CTR < 0,5% przy ≥ 1 000 wyświetleń GSC/mies. przez 3 mies. po decyzji „Zmodyfikować” (sygnał, że wyniki zajmują kalkulatory i kredytodawcy; składu SERP Google dotąd nie zweryfikowano, K-04/K-05) |

**Wspólny warunek zatrzymania produktów 2–5** (odpowiednik pkt 2–3 z §4.4 na poziomie produktu): 90 dni od indeksacji (albo od publikacji, jeśli 60 dni po publikacji strony nadal nie ma w indeksie) < 100 wyświetleń GSC/mies. i 0 cytowań w panelu oraz w Bing AI Performance → wycofać produkt; 6 mies. od indeksacji zmierzony przychód < 2 USD na 1000 sesji ludzi albo < 1 tys. sesji ludzi/mies. bez wzrostu przez 3 kolejne miesiące (po korekcie sezonowej) → wycofać produkt. „Wycofać” oznacza brak dalszych nakładów; o utrzymaniu strony albo jej wyłączeniu decyduje właściciel. Dla RENO-02 te same progi oznaczają przerwanie całego projektu (§4.4).

### 3.2 Produkty kolejne (jeśli pilotaż przejdzie do „kontynuować”)

6. **RENO-04** Whole-Home Capital Plan Sequencer (składa moduły RENO-02 i RENO-03). 7. **LIFE-01** Inherited House Decision: Keep, Rent, Sell or Buy Out Siblings (po zaangażowaniu CPA/prawnika spadkowego). 8. **INS-03** Home Insurance Shock Response: Mitigate vs Higher Wind Deductible vs FAIR/Citizens vs Surplus Lines vs Sell (po inwentaryzacji danych stanowych). 9. **FIN-01** Keep-the-Low-Rate Equity Access Simulator (HELOC vs Home Equity Loan vs Cash-Out Refi vs Personal Loan vs Phasing). 10. **AUTO-02** Lease-End Decision: Buy Out, Return, Re-Lease, or Sell the Lease Equity. W CSV mają one status „zbadać”, nie „pilot”. Dalej: ENER-01 (forma własności PV: gotówka, kredyt, lease, PPA) to odrębna decyzja, ale korzysta z modułu PV zbudowanego dla RENO-02; INS-06 (pompa sump) to gałąź ENER-03 (zasilanie awaryjne), a nie osobny produkt. Każdy z nich podlega tym samym regułom: pomiar popytu i SERP, ręczna weryfikacja konkurencji, reguła dodawania narzędzi i limit tempa (§4.3).

## 4. Plan 30/60/90 dni od publikacji, kalendarz produktów i kryteria decyzji

### 4.1 Zasada: rozdzielić sześć warstw lejka

Brak ruchu po 30 dniach **nie jest** dowodem braku rynku. Każdą warstwę mierzy się osobno i diagnozuje w kolejności:

| Warstwa | Pytanie | Miara | Źródło danych |
|---|---|---|---|
| 1. Dostępność | czy strona działa szybko i jest czytelna dla botów? | uptime, LCP/CLS (mobile), HTML z treścią bez JS; 200 dla `Googlebot`, `Bingbot`, `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` | monitoring, logi, test `curl -A` |
| 2. Indeksacja | czy strona jest w indeksach? | zaindeksowane URL-e w GSC i Bing WMT (data indeksacji uruchamia zegar produktu; jeśli 60 dni po publikacji strony nadal nie ma w indeksie, zegar liczymy od publikacji); pierwsze pobrania przez `OAI-SearchBot` / `PerplexityBot` w logach | GSC, Bing WMT, logi |
| 3. Widoczność | czy pojawia się w wynikach i odpowiedziach? | wyświetlenia GSC; raport GSC „Generative AI” (wyświetlenia AIO/AI Mode); Bing „AI Performance” (cytowania Copilot); panel promptów: % odpowiedzi z cytowaniem, osobno dla każdej platformy (reguł Google nie przenosimy na innych asystentów) | GSC, Bing WMT, panel |
| 4. Kliknięcia | czy ktoś przychodzi? | kliknięcia GSC, CTR; sesje z referrerem AI / `utm_source` (zaniżone przez brak referrera i błąd UTM z 8–15.10.2026 [E-VER-C12]); udział „Direct” na podstronach narzędzi jako wskaźnik pośredni | GSC, GA4, logi |
| 5. Użycie narzędzia | czy ludzie kończą symulację? | `tool_started` / sesję, `tool_completed` / `tool_started`, `variant_view`, `sensitivity_view`, `export` | GA4 (zdarzenia bez wartości) |
| 6. Monetyzacja | czy sesja zarabia? | page RPM (USA i ogółem), przychód na 1000 sesji ludzi (wszystkie kraje, jednostka jak w economics.csv), udział odsłon z wyświetloną reklamą; odczyty korygowane sezonowo (§4.3) | AdSense (raport URL) + GA4 |

#### Plan 30/60/90 dni od publikacji produktu

Pierwsze 90 dni projektu to bramka G0 i budowa (§4.2), więc w tym oknie żadna warstwa lejka nie daje jeszcze danych. Plan 30/60/90 dni liczymy dlatego **od publikacji każdego produktu**. Progi to propozycje decyzyjne, nie normy rynkowe. Przed punktem 90 dni od indeksacji służą one do diagnozy i poprawek, a nie do decyzji „przerwać”.

| Warstwa | Dzień 30 od publikacji | Dzień 60 od publikacji | Dzień 90 od publikacji | Działanie, jeśli sygnału brak |
|---|---|---|---|---|
| 1. Dostępność | kod 200 dla wszystkich botów z tabeli wyżej; LCP i CLS w normie na mobile; HTML z treścią bez JS; uptime bez przerw | stan utrzymany (monitoring) | stan utrzymany | naprawa techniczna przed jakąkolwiek oceną rynkową |
| 2. Indeksacja | URL w indeksie GSC i Bing WMT (data indeksacji uruchamia zegar produktu); pierwsze pobrania `OAI-SearchBot` i `PerplexityBot` w logach | jeśli strony nadal nie ma w indeksie Google i Bing — **reguła awaryjna**: zegar produktu liczymy od publikacji | — | diagnoza techniczna (robots.txt, reguły Cloudflare [E-VER-C11], mapa witryny, canonical, IndexNow), a nie decyzja rynkowa |
| 3. Widoczność | zwykle za wcześnie na ocenę | pierwsze wyświetlenia GSC; raport AI w GSC i Bing AI Performance; wyniki pełnego panelu (§5), uruchomionego tuż po indeksacji | wyświetlenia GSC/mies. porównane z progami 90-dniowymi z §4.3 (≥ 500; 100–500; < 100), po korekcie sezonowej | tytuły, opisy, strony-presety tylko dla zmierzonych klastrów fraz |
| 4. Kliknięcia | — | pierwsze kliknięcia GSC; sesje z referrerem lub UTM asystentów (zaniżone [E-VER-C12]) | CTR wobec progów z §4.3 (≥ 1,5%; < 1%) | tytuły i opisy, treść odpowiedzi w HTML |
| 5. Użycie narzędzia | — | `tool_completed`/`tool_started` przy ≥ 100 startach | ukończenie wobec progów z §4.3 (≥ 35%; < 20%) | tryb szybki, presety, mniej pól |
| 6. Monetyzacja | wniosek do AdSense złożony przy publikacji (§4.2) | status wniosku; pierwsze wyświetlenia reklam | pierwszy kierunkowy odczyt page RPM, tylko przy ≥ 2 000 odsłon, po korekcie sezonowej | brak 2 000 odsłon oznacza brak odczytu, a nie wynik |

Formalna decyzja 90-dniowa (§4.3) jest liczona od indeksacji, więc zwykle wypada ok. dnia 100–120 od publikacji.

### 4.2 Bramka G0 i harmonogram

#### Bramka G0 (dni 0–14; ok. 0 USD; ok. 25–35 h właściciela: panel 10–15 h, krok 4 ok. 6–10 h, kroki 1a–3 ok. 5–10 h) — mierzalna

Koszt gotówkowy jest bliski zeru, ale czas właściciela wyceniony stawką z economics.csv (40 USD/h) to ok. 1,0–1,4 tys. USD.

- **1a. Kanał AI (kierunkowo, inna domena i tematyka):** healthscorer.com, GA4 i logi za 90 dni: sesje ludzi z referrerem lub `utm_source` asystentów, osobno ChatGPT, Gemini/AI Mode, Perplexity, Copilot, Claude; odfiltrowane boty (`ChatGPT-User`, `OAI-SearchBot`, `Claude-User` itd.); Bing Webmaster „AI Performance”. Okno ok. 8–15.10.2026, gdy linki z ChatGPT straciły UTM, raportujemy osobno, a ruch „Direct” na podstronach wejściowych szacujemy jako wskaźnik pośredni [E-VER-C12].
- **1b. Kalibracja monetyzacji (kierunkowo):** z AdSense i GA4 healthscorer.com: page RPM (USA i ogółem), odsłony na sesję, udział odsłon z wyświetloną reklamą na stronach z formularzem; wyniki wpisać do economics.csv jako kalibrację (Z-01…Z-05, K-06). Jeśli dane obejmują XI–XII, odczyty dzielimy przez mnożnik sezonowy 1,2–1,36.
- **2. Popyt w Google dla RENO-02 (K-04):** Keyword Planner (bezpłatnie z kontem Google Ads, bez kampanii) i Google Trends dla 10–20 fraz w 3–5 klastrach (np. wiek dachu a ubezpieczenie, ACV vs RCV dachu, wymiana dachu przed sprzedażą, naprawa vs wymiana dachu, nieodnowienie polisy z powodu dachu); zapisujemy też 12-miesięczny profil sezonowy fraz z Trends (potrzebny do korekty progów ruchu w §4.3). **Próg (propozycja decyzyjna, nie norma rynkowa): łącznie ≥ 10 tys. wyszukiwań/mies. w USA dla mierzonych fraz.** Jeśli narzędzie pokazuje przedziały zamiast liczb, do progu liczymy dolne granice przedziałów. Wyprowadzenie progu (założenia własne): cały klaster z długim ogonem to ok. 2× wolumen mierzonych fraz, czyli ok. 20 tys. wyszukiwań/mies.; po dojrzeniu produkt przechwytuje 10–15% ruchu klastra, co daje ok. 2–3 tys. sesji ludzi/mies., czyli tylko składnik ruchu z wiersza „Kontynuować” w §4.3 (≥ 3 tys. sesji ludzi/mies.) i zarazem górną granicę wiersza „Wstrzymać”. Pełne „Kontynuować” wymaga też reguły dodawania (ok. 250 USD/mies., czyli ok. 39–50 tys. sesji ludzi/mies. przy 6,4–5 USD na 1000 sesji ludzi). Przy tych samych założeniach (×2 długi ogon, 10–15% przechwycenia) odpowiada to ok. 130–250 tys. wyszukiwań/mies. mierzonych fraz. Próg 10 tys. to więc warunek konieczny, a nie poziom „Kontynuować”; jego spełnienie nie oznacza też, że produkt osiągnie nawet 2–3 tys. sesji ludzi/mies.
- **3. SERP i AI w Google (K-05):** dla 10 najważniejszych fraz: czy pojawia się AIO/AI Mode i czy generuje własny kalkulator lub tabelę wariantów; ile wyników w top 10 to fora lub domeny o niskim autorytecie. **Próg (propozycja): dla ≥ 3 fraz w top 10 są ≥ 2 wyniki z forów lub małych domen, a AI Mode/AIO nie generuje pełnego porównania wariantów w więcej niż połowie fraz.**
- **4. Ręczna weryfikacja konkurencji RENO-02 (K-03):** otworzyć strony wszystkich kandydatów z „Listy do ręcznej weryfikacji (G0 krok 4)” w karcie RENO-02 (`top-10-products.md`) i przetestować formularze. To jedyna pełna lista; łączy wyniki próby obalenia (fala 2b) i audytu (fala 2) z `competitor-audit.csv`. Z fali 2b: kalkulatory Roof ROI (Weathershield Roofers, CalculateMyRoof, ShinglesCalculator), BuildFolio, Hammerio, InsuranceCostCity, RoofingCalculatorUSA, Roof Decision Guide (hub narzędzi), kalkulatory szkód gradowych (ShinglesCalculator, RoofingCalculatorHQ) oraz Paperform Roof Replacement Financing Calculator. Z fali 2: SubcontractorHub, Roof Decision Guide (kalkulator naprawa vs wymiana), RoofTap, RoofQuote, kalkulatory kosztu wymiany dachu (TheRooferFinder i in.) oraz ServiceAgent.ai. Uzupełnienie z fali 1 (m.in. Shingles Calculator – Roof Depreciation, ACV & Replacement Planning, który według streszczenia może dotykać dwóch zależności: ACV i horyzontu; RateMyPolicy, TeamzLab, roofcalc.org) jest w tej samej liście w karcie. W pierwszej kolejności sprawdzamy kalkulatory Roof ROI (Weathershield Roofers, CalculateMyRoof, ShinglesCalculator). Kandydaci to 14 konkurentów częściowych (8 z fali 2b, 6 z fali 2) i 13 substytutów z fal 2 i 2b oraz 8 narzędzi częściowych z fali 1; klasyfikacja opiera się wyłącznie na streszczeniach wyszukiwarki, a kluczowe funkcje kandydatów są niezweryfikowane. **Reguła: produkt odpada, jeśli jedno narzędzie pokrywa ≥ 3 kluczowe zależności** (ACV/RCV lub harmonogram wypłat za dach; udział własny wiatr/grad; horyzont sprzedaży; demontaż i ponowny montaż PV; finansowanie). RENO-02 jest warunkiem startu całego projektu.
- **5. Panel asystentów — pomiar bazowy (nie warunek):** 5 produktów pilotażowych × (2 prompty bez prośby o narzędzie + 2 z prośbą o kalkulator) × 5 asystentów × 2 powtórzenia = 200 uruchomień (ok. 10–15 h). Używamy promptów nr 1 i 2 z kategorii „Bez prośby o narzędzie” oraz nr 1 i 2 z kategorii „Z prośbą o kalkulator” z karty każdego pilota w `top-10-products.md`. Odsetek linków raportujemy osobno dla obu kategorii promptów i osobno dla każdej platformy (ChatGPT, AI Mode/AIO, Perplexity, Copilot, Claude). Pule promptów pozostałych finalistów (RENO-04, LIFE-01, INS-03, CARE-01, FIN-01) testujemy dopiero przed decyzją o ich budowie. Szczegóły zapisu: §5.

**Reguła bramki:** budować test opcji (RENO-02) tylko jeśli **spełnione są jednocześnie kroki 2, 3 i 4**. Kroki 1a, 1b i 5 nie otwierają bramki, tylko kalibrują oczekiwania: jeśli 1a pokaże ≥ 1% sesji ludzi z AI i ≥ 2 tys. takich sesji/mies., kanał AI traktujemy jako realny dodatek (wskaźnik pośredni); z odczytów 1b liczymy przychód na 1000 sesji ludzi (page RPM USA × odsłony na sesję × miks USA/poza USA × udział odsłon z reklamą) i porównujemy go z progami decyzyjnymi 2 / 3 / 5 USD (§4.4 pkt 3 / „Zmodyfikować” / „Kontynuować”; w strukturze bazowej modelu odpowiada to page RPM USA ≈ 2,5 / 3,8 / 6,3 USD). Wynik < ok. 2 USD zapowiada warunek przerwania z §4.4, pkt 3: to sygnał ostrzegawczy do decyzji właściciela przed startem. Wynik < 5 USD oznacza, że „Kontynuować” wymaga więcej odsłon na sesję lub wyższego RPM niż zmierzony. Deklaracja właściciela („akceptuję Google organic”) **nie jest** warunkiem bramki.

Jeśli bramka nie przechodzi, zachodzi warunek przerwania z §4.4, pkt 1. Ewentualną dalszą pracę rozważamy wtedy tylko w innym modelu, osobną decyzją (strategie alternatywne w executive-summary.md).

**Najtańsza alternatywa przed budową (opcjonalna, za zgodą właściciela):** MVP RENO-02 bez pełnego silnika + płatny ruch (Google Ads) przez 2 tygodnie: pomiar ukończenia (`tool_completed`/`tool_started`) i CTR. Odczyt ukończenia wymaga ≥ 100 startów (§4.1). W Search (CPC ok. 3,44 USD [E-ADS-15]) 300–500 USD daje tylko ok. 87–145 kliknięć, więc potrzeba ok. 500–700 USD (przy założeniu własnym 50–70% startów na sesję). W GDN (CPC ok. 0,86 USD) 300–500 USD daje ok. 350–580 kliknięć, ale ruch ma inną intencję, więc odczyt jest kierunkowy. RPM w tym budżecie nie jest mierzalny: odczyt kierunkowy wymaga ≥ 2 000 odsłon, czyli ok. 1,3–5,3 tys. USD płatnego ruchu (CPC jest tu kosztem zakupu kliknięć, a nie przychodem serwisu [E-ADS-15]), i zatwierdzonej witryny w AdSense. Do tego rozmowy z 5 potencjalnymi klientami B2B (dekarze, agenci ubezpieczeniowi, credit unions). Ten wariant przesuwa kalendarz budowy.

#### Harmonogram testu opcji przy dostępności właściciela ok. 15 h/tydzień

Plan zakłada ok. **15 h/tydzień** pracy właściciela (ok. 60–65 h/mies., czyli tyle, ile scenariusz bazowy economics.csv: 60 h/mies.). Przy takim tempie w pierwszych 90 dniach nie powstaje jeszcze żaden gotowy symulator, a pięciu nie da się zbudować w pierwszym kwartale. Budowa testu opcji (silnik + RENO-02, w bazie ok. 215 h) zajmuje ok. 14 tygodni po G0, więc **publikacja RENO-02 wypada ok. dnia 105–120** (ok. 4. miesiąca). Scenariusze economics.csv łączą zakres prac z dostępnością właściciela: w konserwatywnym (290 h przy 40 h/mies.) publikacja wypada ok. 8. miesiąca od startu budowy, a w optymistycznym (140 h przy 80 h/mies.) ok. 2. miesiąca.

| Okres | Co się dzieje (ok. godzin właściciela) | Wynik |
|---|---|---|
| **Dni 0–14** | bramka G0: kroki 1a, 1b, 2, 3, 4, 5 (ok. 25–35 h) | decyzja: start testu opcji albo przerwanie (§4.4, pkt 1) |
| **Dni 15–30** (ok. 35 h) | domena, hosting statyczny za CDN, robots.txt i świadoma konfiguracja Cloudflare [E-VER-C11], GSC, Bing WMT, IndexNow, GA4 z kanałem AI i zdarzeniami bez wartości; **CMP, polityka prywatności, konfiguracja GPC/RDP i link opt-out**; szkielet silnika (oś czasu, jednostki, finansowanie); zapytania ofertowe do ekspertów RENO-02 (K-07); inwentaryzacja danych RENO-02 (K-08), w tym sprawdzenie wersji FEMA NRI | infrastruktura i warstwa zgód gotowe |
| **Dni 31–60** (ok. 65 h) | moduły silnika: `financing`, `home_sale`, `insurance_policy`, `roof`, `storm_risk`; testy jednostkowe, właściwości i brzegowe; pierwsze złote przypadki; specyfikacja YAML RENO-02 | silnik minimalny z testami |
| **Dni 61–90** (ok. 65 h) | formularz (tryb szybki i pełny), wyniki, tornado, progi przełączenia; strona metodologii; treść HTML; przekazanie wersji do przeglądu eksperckiego (agent P&C, dekarz, agent nieruchomości, CFP, instalator PV) | RENO-02 w przeglądzie eksperckim |
| **Dni 91–120** (ok. 50 h) | poprawki po przeglądzie eksperckim; disclaimery i regulamin po przeglądzie prawnika; testy dostępności, CLS i test sieciowy prywatności; złote przypadki zatwierdzone przez ekspertów | RENO-02 gotowy do publikacji (ok. dnia 105–120) |
| **Ok. dnia 105–120** | publikacja RENO-02, strony metodologii i ewentualnych stron-presetów (tylko dla odrębnych klastrów fraz zmierzonych w G0, krok 2); zgłoszenie do GSC, Bing i IndexNow; **wniosek o dodanie witryny do AdSense dopiero teraz**, gdy strona ma treść (nowa witryna podlega ocenie [E-ADS-09]); test porównawczy (ten sam scenariusz w ChatGPT i AI Mode: czas, błędy, brakujące zależności) | zegar RENO-02 startuje w dniu indeksacji |
| **Od publikacji do decyzji** | plan 30/60/90 dni od publikacji (§4.1); utrzymanie (ok. 9 h/mies. w bazie), comiesięczna analiza lejka (warstwy 1–6), pierwszy odczyt RPM po 2 000 odsłon (kierunkowo), pełny panel §5 dla RENO-02 tuż po indeksacji i przed punktem 90 dni | dane do decyzji |
| **Ok. mies. 7–8 od startu** | punkt 90 dni od indeksacji RENO-02: decyzja według §4.3 i §4.4, pkt 2 | kontynuować / zmodyfikować / wstrzymać / przerwać |
| **Ok. mies. 10–11 od startu** | punkt 6 mies. od indeksacji RENO-02: decyzja według §4.3 i §4.4, pkt 3 | j.w. |

Indeksacja następuje zwykle kilka dni do kilku tygodni po publikacji (założenie planistyczne; datę odczytujemy w GSC), dlatego punkty kontrolne mogą przesunąć się w stronę górnej granicy podanych przedziałów. Górną granicę wyznacza reguła awaryjna: jeśli 60 dni po publikacji strony nadal nie ma w indeksie Google i Bing, zegar liczymy od publikacji (§4.3). Przy starcie G0 pod koniec X 2026 publikacja RENO-02 wypada ok. połowy II 2027, punkt 90 dni ok. V–VI 2027, a punkt 6 mies. ok. VIII–IX 2027.

**Limity w kalendarzu.** Limit testu opcji to ok. 9 tys. USD gotówki i ok. 300 h czasu właściciela na G0 i budowę, bez utrzymania po publikacji. W bazie gotówka do publikacji RENO-02 wynosi ok. 5,9 tys. USD (prawo/CMP, ekspert RENO-02 i koszty stałe do miesiąca publikacji), a czas — ok. 215 h budowy plus 25–35 h G0 (razem ok. 240–250 h). Po publikacji dochodzą koszty stałe jednego narzędzia, ok. 290 USD/mies. (z utrzymaniem eksperckim), i ok. 9 h/mies. czasu właściciela na utrzymanie (economics.csv). Do decyzji 6-miesięcznej (ok. mies. 10–11) gotówka dochodzi więc do ok. 8 tys. USD: w bazie test mieści się w limicie, ale z niewielkim zapasem. Jeśli RENO-02 nie osiągnie ok. 250 USD/mies. przychodu, limit ok. 9 tys. USD wyczerpuje się w bazie ok. 18. mies. od startu budowy (ok. 14 mies. po publikacji), czyli zachodzi warunek przerwania z §4.4, pkt 4. W scenariuszu konserwatywnym gotówka do publikacji to ok. 13 tys. USD, a czas 290 h budowy (z G0 ok. 315–325 h). Oba limity zostają przekroczone przed publikacją, czyli zachodzi warunek przerwania z §4.4, pkt 4, chyba że właściciel jawnie obetnie koszty (np. koszty stałe w fazie budowy). W scenariuszu optymistycznym test kosztuje ok. 3,0 tys. USD i 140 h.

#### Kalendarz produktów (zegar od indeksacji każdego produktu)

Kolejny produkt może powstać dopiero po decyzji „Kontynuować” dla RENO-02, po własnym pomiarze popytu i SERP (jak w G0, kroki 2–3), po ręcznej weryfikacji jego konkurencji i przy spełnionej regule dodawania narzędzi (mediana przychodu narzędzi z ruchem); tempo to maksymalnie 1 nowy symulator miesięcznie (§4.3). Daty poniżej to **najwcześniejsze możliwe**, przy założeniu, że każda bramka przechodzi.

| Produkt | Warunek startu budowy | Budowa (h właściciela; przy 15 h/tydz.) | Publikacja (najwcześniej, mies. od startu) | 90 dni od indeksacji | 6 mies. od indeksacji |
|---|---|---|---|---|---|
| RENO-02 | G0 zaliczona | silnik + produkt: ok. 215 h w bazie (140–290 h); ok. 14 tyg. | ok. dnia 105–120 (ok. mies. 4) | ok. mies. 7–8 | ok. mies. 10–11 |
| RENO-03 | RENO-02 „Kontynuować” + pomiar popytu i SERP + weryfikacja konkurencji + reguła dodawania | 40–60 h; ok. 3–4 tyg. + przegląd eksperta | ok. mies. 8–9 | ok. mies. 11–12 | ok. mies. 14–15 |
| HOME-04 | reguła dodawania nadal spełniona + pomiar popytu i SERP + weryfikacja konkurencji; ≥ 1 mies. po poprzednim produkcie | 30–45 h; ok. 2–3 tyg. + ekspert | ok. mies. 9–10 | ok. mies. 12–13 | ok. mies. 15–16 |
| HOME-02 | j.w.; CPA/EA przed publikacją | 35–50 h; ok. 3 tyg. + ekspert | ok. mies. 10–11 | ok. mies. 13–14 | ok. mies. 16–17 |
| AUTO-01 | j.w. | 30–40 h; ok. 2–3 tyg. + ekspert | ok. mies. 11–12 | ok. mies. 14–15 | ok. mies. 17–18 |

Ocena całego pilotażu pięciu produktów jest więc możliwa najwcześniej ok. 17–18 mies. od startu. W ilustracji bazowej z economics.csv najlepsze narzędzie osiąga ok. 15 tys. sesji zarejestrowanych/mies. (ok. 14 tys. sesji ludzi) dopiero po 12 mies., a reguła dodawania wymaga mediany ok. 250 USD/mies., czyli ok. 39 tys. sesji ludzi/mies. na narzędzie (ok. 42 tys. zarejestrowanych; baza). Realnie kolejne produkty mogą więc nie powstać w pierwszym roku albo wcale.

### 4.3 Kryteria decyzji (propozycje decyzyjne, nie normy rynkowe)

Jedna tabela obowiązuje wszystkie produkty. Zegar produktu liczymy **od indeksacji produktu** w Google i Bing (nie od publikacji). **Reguła awaryjna:** jeśli 60 dni po publikacji strony nadal nie ma w indeksie Google i Bing, zegar produktu liczymy od publikacji (brak indeksacji to najpierw diagnoza techniczna, §4.1). Punkty kontrolne: **90 dni od indeksacji** i **6 mies. od indeksacji**. Progi sesji dotyczą sesji ludzi (po filtrach botów). Przychód liczymy na 1000 sesji ludzi ze wszystkich krajów; w economics.csv to 1,2 / 6,4 / 21,6 USD (kons. / baz. / opt.). Uwaga na jednostki: progi ruchu w economics.csv (progi rentowności, sesje na narzędzie) są liczone w sesjach zarejestrowanych, z botami, przy przychodzie 1,0 / 5,9 / 21 USD na 1000 takich sesji.

| Decyzja | 90 dni od indeksacji | 6 mies. od indeksacji |
|---|---|---|
| **Kontynuować** — przygotować kolejny produkt z listy pilotów (maks. 1 nowy symulator/mies. do osiągnięcia progu rentowności gotówkowej) | ≥ 500 wyświetleń GSC/mies.; CTR ≥ 1,5%; `tool_completed`/`tool_started` ≥ 35% | zmierzony przychód ≥ 5 USD na 1000 sesji ludzi **i** produkt na ścieżce do zwrotu: ≥ 3 tys. sesji ludzi/mies. z trendem ≥ +15% m/m przez 3 mies. **i** spełniona reguła dodawania narzędzi |
| **Zmodyfikować** | wyświetlenia są, ale CTR < 1% albo ukończenie < 20% → tytuły, presety, tryb szybki, treść HTML | ruch rośnie, ale przychód < 3 USD/1000 sesji ludzi → test formatu; afiliacja tylko jako dodatek |
| **Wstrzymać** (nie budować nowych, iterować istniejący maks. 3 mies.) | 100–500 wyświetleń GSC/mies. | 1–3 tys. sesji ludzi/mies. bez trendu |
| **Przerwać** (odpowiednik „odrzucić” z briefu) | zob. §4.4 | zob. §4.4 |

**Korekta sezonowa progów.** Progi ruchu (wyświetlenia GSC, sesje ludzi) w punktach 90 dni i 6 mies. porównujemy po korekcie o indeks sezonowy z Google Trends dla miesięcy pomiaru: odczyt dzielimy przez stosunek indeksu Trends w miesiącu pomiaru do średniej z 12 miesięcy. Profil sezonowy RENO-02 pochodzi z G0 (krok 2), a produktów 2–5 — z ich własnego pomiaru popytu. Sezonowości popytu nie modelowano w economics.csv; jej skalę zmierzy dopiero Trends. Przychód i RPM porównujemy po korekcie sezonowej RPM (economics.csv; średnia roczna mnożnika = 1,0): odczyty z XI–XII dzielimy przez 1,2–1,36, a z I–II przez ok. 0,75–0,85. Decyzji nie opieramy na samym IV kwartale ani na samym dołku styczniowym [E-ADS-20]. Przy kalendarzu z §4.2 pierwsze odczyty RPM przypadną ok. III–V 2027, a punkt 6 mies. ok. VIII–IX 2027; w tych miesiącach mnożniki RPM wynoszą ok. 0,95–1,0, ale korektę stosujemy zawsze.

**Reguła dodawania narzędzi:** nowe narzędzie tylko wtedy, gdy **mediana miesięcznego przychodu narzędzi z ruchem ≥ koszt gotówkowy nowego narzędzia / 24 + utrzymanie eksperckie** — i nie więcej niż 1 nowe narzędzie miesięcznie do osiągnięcia gotówkowego progu rentowności. W bazie to ok. 3 850 USD / 24 + ok. 90 USD ≈ **250 USD/mies.**, czyli ok. **39 tys. sesji ludzi/mies. na narzędzie** przy 6,4 USD na 1000 sesji ludzi (kons. / opt.: ok. 530 / 120 USD/mies., czyli ok. 442 tys. / 5,5 tys. sesji ludzi). Przy minimalnym przychodzie z wiersza „Kontynuować” (5 USD na 1000 sesji ludzi) te same 250 USD/mies. wymagają ok. 50 tys. sesji ludzi/mies. W praktyce próg w sesjach liczymy z RPM zmierzonego. W punkcie 90 dni spełnienie wiersza „Kontynuować” pozwala przygotować kolejny produkt (pomiar popytu i SERP, ręczna weryfikacja konkurencji, specyfikacja), ale wydatek na eksperta i publikacja wymagają spełnienia tej reguły.

**Limity testu opcji:** ok. 9 tys. USD gotówki i ok. 300 h czasu właściciela na G0 i budowę, bez utrzymania po publikacji (§4.4, pkt 4); każda kolejna transza wymaga spełnienia reguły dodawania.

**Wyniki pomiędzy wierszami.** Wynik, który nie pasuje do żadnego wiersza (np. CTR 1–1,5% albo ukończenie 20–35% przy ≥ 500 wyświetleniach; < 100 wyświetleń przy ≥ 1 cytowaniu; dobry przychód i wzrost bez spełnionej reguły dodawania), traktujemy jak „Wstrzymać”: bez nowych narzędzi, z iteracją istniejącego i comiesięcznym pomiarem, aż wynik trafi do wiersza „Kontynuować” albo do warunku przerwania.

**Zdarzenia nadzwyczajne** (ręczna kara obejmująca domenę, dwukrotne odrzucenie wniosku AdSense, blokada konta za IVT) wymagają osobnej decyzji właściciela; nie są dodatkowym automatycznym warunkiem przerwania, a ich skutki finansowe i tak wchodzą do limitu straty.

**Powiązanie z progiem rentowności i zyskiem operacyjnym (economics.csv; ilustracja, nie prognoza; kons. / baz. / opt.).**
- Koszty stałe gotówkowe (z utrzymaniem eksperckim 12 / 6 / 3 h na narzędzie rocznie): 5 narzędzi 1 710 / 640 / 290 USD/mies.; 15 narzędzi 4 210 / 1 510 / 600 USD/mies.; 25 narzędzi 6 710 / 2 390 / 910 USD/mies.
- Próg rentowności gotówkowej (sesje zarejestrowane/mies.): 5 narzędzi 1,68 mln / 109 tys. / 14 tys.; 15 narzędzi 4,12 mln / 259 tys. / 29 tys.; 5 narzędzi z amortyzacją gotówki uruchomienia w 24 mies.: 3,14 mln / 254 tys. / 36 tys.; 5 narzędzi z wyceną czasu właściciela: 2,51 mln / 191 tys. / 27 tys.
- Zwrot gotówki budowy jednego narzędzia w 24 mies. (z utrzymaniem eksperckim) wymaga 520 tys. / 42 tys. / 5,7 tys. sesji zarejestrowanych/mies. na narzędzie, a zwrot pełnego kosztu (z czasem właściciela) 628 tys. / 55 tys. / 7,9 tys.
- Zysk operacyjny gotówkowy przy 25 narzędziach: przy 1000 USD przychodu −5 710 / −1 390 / +90 USD/mies. (marża −571% / −139% / +9%); przy 3000 USD −3 710 / +610 / +2 090 USD/mies.; przy 10 000 USD +3 290 / +7 610 / +9 090 USD/mies. Po wycenie czasu właściciela przy 1000 USD przychodu: −7 560 / −2 510 / −540 USD/mies.
- Kryterium „Kontynuować” w 6. miesiącu nie oznacza rentowności. Przy 3 tys. sesji ludzi/mies. i stałym wzroście +15% m/m próg reguły dodawania (ok. 39 tys. sesji ludzi na narzędzie) zostaje osiągnięty po ok. 18 kolejnych miesiącach, a gotówkowy próg rentowności 5 narzędzi (109 tys. sesji zarejestrowanych, czyli ok. 100 tys. sesji ludzi) po ok. 25 miesiącach (rachunek ilustracyjny). Dlatego wiążąca jest reguła dodawania, a nie samo kryterium „Kontynuować”.
- Ścieżka bez tej reguły: economics.csv ilustruje pełną budowę ograniczoną tylko czasem właściciela (40 / 60 / 80 h/mies.; mies. 1 = listopad). W 12. miesiącu liczba działających narzędzi wynosi 4 / 12 / 23, a przychód ok. 1 / 100 / 3 370 USD/mies.; w 24. miesiącu przychód to ok. 3 / 220 / 4 940 USD/mies., a wynik gotówkowy −1 710 / −1 290 / +3 870 USD/mies. Skumulowany wynik gotówkowy po 12 / 24 / 36 mies. wynosi w bazie −54 / −82 / −97 tys. USD (kons. −38 / −65 / −86 tys.; opt. −40 / −16 / +27 tys.), a z wyceną czasu właściciela po 36 mies. −139 / −156 / −31 tys. USD. Zwrot gotówki pojawia się tylko w scenariuszu optymistycznym (ok. mies. 29); z wyceną czasu właściciela żaden scenariusz nie zwraca się w 36 mies. Reguła dodawania i limity testu mają nie dopuścić do tej ścieżki, jeśli zmierzony przychód jej nie uzasadnia.

### 4.4 Warunek przerwania projektu

Przerwać projekt (nie tylko produkt), jeśli zajdzie którekolwiek z poniższych: (1) bramka G0 nie przechodzi — ręczna weryfikacja znajduje narzędzie pokrywające ≥ 3 kluczowe zależności RENO-02 albo pomiar popytu i SERP w Google nie spełnia progów; (2) 90 dni od indeksacji RENO-02 (albo od publikacji, jeśli 60 dni po publikacji strony nadal nie ma w indeksie): < 100 wyświetleń GSC/mies. i 0 cytowań w panelu asystentów oraz w Bing AI Performance; (3) 6 mies. od indeksacji RENO-02: zmierzony przychód < 2 USD na 1000 sesji ludzi albo < 1 tys. sesji ludzi/mies. bez wzrostu przez 3 kolejne miesiące (po korekcie sezonowej); (4) skumulowana strata gotówkowa przekracza ok. 9 tys. USD albo czas właściciela na G0 i budowę testu (silnik + RENO-02, bez utrzymania po publikacji) przekracza ok. 300 h, zanim spełnione zostaną kryteria kontynuacji. Progi to propozycje decyzyjne, nie normy rynkowe. Po przerwaniu ewentualną kontynuację rozważać tylko w innym modelu (B2B embed/white-label, lead-gen, subskrypcja), osobną decyzją.

Ten sam tekst znajduje się w executive-summary.md §8.

---

## 5. Protokół testu dystrybucji przez asystentów (do wykonania przez właściciela)

Wyników tego testu w raporcie nie ma: to plan, a nie wyniki. Test ma dwa zakresy: **pomiar bazowy w G0** (krok 5) i **pełny protokół** po publikacji, tylko dla zbudowanych produktów.

1. **Platformy:** ChatGPT (Free i Plus, jeśli dostępne), Google AI Mode i zwykłe wyszukiwanie z AI Overviews, Perplexity, Microsoft Copilot, Claude. Konta prywatne, bez historii; lokalizacja USA, jeśli zgodnie z warunkami usług dostępna (VPN tylko tam, gdzie regulamin na to pozwala); język angielski.
2. **Prompty:** w G0 — 5 produktów pilotażowych × (2 prompty bez prośby o narzędzie + 2 z prośbą o kalkulator), z kart w `top-10-products.md`; pule promptów pozostałych finalistów testujemy dopiero przed decyzją o ich budowie. W pełnym protokole — zestaw z karty danego produktu: 4 bez prośby o narzędzie, 4 z prośbą o kalkulator, 2–4 z prośbą o porównanie scenariuszy.
3. **Powtórzenia:** w G0 — 2 uruchomienia każdego promptu; w pełnym protokole — 3 uruchomienia w nowym czacie, w różnych dniach. Listy rekomendacji powtarzają się identycznie rzadziej niż w 1 na 100 uruchomień [E-AI-23].
4. **Zapis** (arkusz): platforma, wersja/tryb, data i godzina, prompt, czy włączono wyszukiwanie, pełna odpowiedź (zrzut), czy asystent **sam** zbudował kalkulator lub tabelę, lista linków (URL, typ: narzędzie / artykuł / forum / sklep / lead-gen), czy któryś link prowadzi do narzędzia realizującego pełny problem, brakujące zależności w odpowiedzi (np. pominięty koszt demontażu PV, ACV vs RCV, horyzont sprzedaży), błędy merytoryczne.
5. **Miary** (zawsze osobno dla każdej platformy, bez sumowania asystentów): % odpowiedzi z jakimkolwiek linkiem; % z linkiem do narzędzia; udział linków do małych domen bez rozpoznawalnej marki obok linków do dużych wydawców finansowych; % z samodzielnie wygenerowanym kalkulatorem; liczba brakujących zależności (jakość); po publikacji — % odpowiedzi z cytowaniem naszej domeny. Odsetek linków liczymy też osobno dla promptów bez prośby o narzędzie, bo prompty z prośbą o kalkulator ten odsetek zawyżają.
6. **Czas:** pomiar bazowy w G0 to 200 uruchomień w ok. 10–15 h (ok. 3–4,5 min na uruchomienie z zapisem). Pełny protokół dla jednego produktu (10–12 promptów × 5 asystentów × 3 powtórzenia = 150–180 uruchomień) to ok. 8–14 h na rundę.
7. **Zakazy:** bez automatyzacji interfejsów konsumenckich wbrew regulaminom; oficjalne API (np. z narzędziem wyszukiwania) tylko jako uzupełnienie, z adnotacją, że wyniki API ≠ wyniki aplikacji [E-AI-23].
