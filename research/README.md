# Research: serwis symulatorów decyzji (USA) — indeks plików

Badanie z 2026-10-25, poprawione po recenzji adwersaryjnej (fala 3). Start: `executive-summary.md`.

| Plik | Zawartość |
|---|---|
| `executive-summary.md` | werdykt, pozycjonowanie, domena, najważniejsze dowody, ryzyka, rekomendacja zakresu (5 pilotów), trzy obalone założenia (§4a), trzy największe niewiadome (§4b), ekonomika, strategie alternatywne, pierwszy eksperyment (bramka G0), granice pewności, warunek przerwania |
| `market-and-distribution.md` | etap A (teza biznesowa, lejek marki w asystentach), popyt w USA, dystrybucja przez asystentów AI platforma po platformie, etap B (11 rodzin z briefu w 22 podrodzinach + 13 obszarów nieoczywistych = 35 wierszy ocen, z kartami uzasadnień) |
| `product-opportunities.csv` | długa lista: 96 wierszy, 92 odrębne pomysły (RENO-01, INS-06, CARE-07 i BIZ-06 to gałęzie, moduły lub warianty innych), wszystkie wymagane pola, status, kalibracja i poziom weryfikacji |
| `competitor-audit.csv` | rejestr konkurencji: 1192 wierszy z fal 1, 2 i 2b (data, kwerenda, URL, konkurent, sprawdzone funkcje, ograniczenia dostępu, wniosek, pewność, podstawa dowodu i kolumny kontrolne opisane niżej) |
| `top-10-products.md` | werdykty dla pomysłów startowych A–I, metoda selekcji, ranking 25 audytowanych pozycji (24 odrębne), uzasadnienia per kryterium, rankingi szczegółowe, karty 10 finalistów z promptami testowymi |
| `economics.csv` | model scenariuszowy (konserwatywny / bazowy / optymistyczny) z jednostkami, typem wartości i opisem założeń; 36-miesięczna ilustracja trajektorii |
| `architecture-and-validation.md` | etap G (domeny), etap H (architektura), pilotaż 5 produktów, plan 30/60/90, bramka G0, kryteria decyzji, protokół testu asystentów |
| `evidence-and-assumptions.md` | metoda i ograniczenia, status zadań, źródła pierwotne, rejestr założeń, sprzeczności, kolejka badań, korekty po recenzji, rejestr dowodów (E-…, w tym E-REV-01…09) |
| `tools/` | skrypty generujące pliki (opis niżej) |
| `data/agent-outputs/` | surowe, ustrukturyzowane wyniki agentów (JSON): fundamenty, uzupełnienia, weryfikacje, rodziny, pomysły startowe, audyty, próby obalenia, popyt; oraz pliki pośrednie skryptów (all_ideas, longlist, calibration, final_status, evidence_rows, evidence_overrides, csv_stats). Pliki pośrednie `final_status.json` i `calibration.json` mają statusy i uwagi sprzed scaleń i recenzji (np. RENO-01 „pilot”, INS-06 „zbadać”, BIZ-01 i BIZ-04 „osobna domena”); obowiązują `product-opportunities.csv` i `competitor-audit.csv` (generator nakłada na nie poprawki z fali 3) |
| `data/review-wave3/` | recenzja adwersaryjna fali 3 (5 recenzentów) i kontrola spójności po poprawkach (5 soczewek, każde zgłoszenie z werdyktem weryfikatora) |

## Słownik kolumn CSV

**`product-opportunities.csv`**

- `status` — tylko 4 wartości: `pilot` (kandydat do pilotażu po bramkach, nie decyzja o budowie), `zbadać`, `później`, `odrzucić`. Kwalifikatory („gałąź RENO-02”, „poza domeną; ewentualny test w istniejącym serwisie e-commerce właściciela”, „test na healthscorer.com”, „poza zakresem startowym domeny”) są w kolumnie `uwaga_statusu`.
- `poziom_pewnosci (oceny/statusu)` — pewność **decyzji o statusie**, nie siła pojedynczego dowodu. Pomysły bez wyszukiwań („koncepcyjne”) mają zawsze „niska”.
- `poziom_weryfikacji` — `koncepcyjny (bez wyszukiwań przypisanych do tego pomysłu)`; `wstępnie sprawdzony w wyszukiwarce (fala 1; N wierszy search-summary)`; `audyt fali 2 (7 zapytań)`; dla 10 finalistów dodatkowo `próba obalenia fali 2b (8 zapytań) + badanie popytu fali 2b`. Wszędzie: strony nieotwierane, dowód ze streszczeń wyszukiwarki.
- `rekomendacja_audytora (top 25)`, `ocena_agenta_0_5 (top 25)`, `ocena_po_kalibracji_0_5 (top 25)`, `zmienione_kryteria_w_kalibracji` — ślad od audytu do decyzji. Gdy status różni się od rekomendacji audytora, powód jest na początku `uzasadnienie_statusu`.
- `bezposredni_konkurent (top 25)` — formuła „Nie znaleziono bezpośredniego konkurenta w badanym zakresie” z zakresem i pewnością; „tak: <nazwy>” tam, gdzie audyt znalazł konkurenta bezpośredniego (RET-03); „sporny” tam, gdzie fale klasyfikują to samo narzędzie różnie (Home Energy Planner dla ENER-03, OverlineIQ dla RENT-01).
- `odrebny_pomysl` — reguła z `architecture-and-validation.md` §2: pomysł jest odrębny, jeśli różni się decyzją, wariantami, kolejnością zdarzeń lub modelem obliczeń. „Nie” dla RENO-01 (gałąź RENO-02), INS-06 (gałąź ENER-03), CARE-07 (moduł CARE-01) i BIZ-06 (wariant BIZ-05).
- `uwagi_scalenia_i_bliskie_duplikaty` — scalenia i bliskie duplikaty (warianty jednego silnika).
- Wpis „… — ocena koncepcyjna agenta; nie badano w tej sesji (brak danych)” oznacza pole, którego agent nie oparł na żadnym dowodzie.
- Brakujące numery ID (FIN-04, INS-07, JOB-10, CARE-02) to pomysły scalone po recenzji odpowiednio z LIFE-04, INS-03, RET-05 i FIN-02; ich źródła są w `scalone_z_pomyslow_agentow`.

**`competitor-audit.csv`**

- `produkt_ID_agenta` — identyfikator użyty przez agenta (np. „Seed B”, „G2-01, G2-03”); `produkt_ID_final` — ID z `product-opportunities.csv` (lista rozdzielona „;”). Wierszy bez przypisania: 0.
- `typ_wiersza` — `konkurent` / `sygnał_popytu` / `źródło_reguł_lub_danych` / `brak_wyniku`. Liczniki konkurentów licz tylko z `konkurent`.
- `klasyfikacja (automatyczna z wniosku)` — `bezpośredni` / `sporny (do ręcznej weryfikacji; wiedza modelu)` (wiersze z wiedzy modelu, w których agent pisał o konkurencie bezpośrednim) / `sporny (częściowy lub bezpośredni)` / `niezweryfikowany (wniosek dotyczy innego zakresu)` (wiersz rozbity na produkty, a wniosek mówi o innym pomyśle) / `częściowy` / `substytut` / `niezweryfikowany` / `nie-konkurent`; wyprowadzona z pierwszego określenia we wniosku agenta, więc przy decyzjach czytaj też `wniosek` Wiersze fali 1, których wniosek klasyfikuje kilka pomysłów różnie („DIRECT dla G6-03; PARTIAL dla G6-02”), rozbito na osobne wiersze dla każdego produktu.
- `podstawa_dowodu` — `search-summary – opis w wyniku wyszukiwania`; `wyszukiwanie wykonane – brak w wynikach; wiedza modelu`; `wiedza modelu – bez wyszukiwania`; `notatka fali 1 – niepotwierdzona w fali 2`. Pewność wierszy z wiedzy modelu lub z URL innego podmiotu jest ograniczona do „niska”, a wierszy search-summary do „średnia” (żadnej strony nie otwarto).
- `url_zgodny_z_nazwa_konkurenta` — „nie” oznacza, że URL to wzmianka lub artykuł innego serwisu, a strona narzędzia jest nieustalona.
- `uwaga_reguly_9` — wniosek mówi o braku funkcji, choć strony nie otwarto; czytać jako „niezweryfikowane”, nie „brak”.
- `konflikt_klasyfikacji` — ten sam URL lub konkurent sklasyfikowany różnie w różnych wierszach; `zastapiony_przez_nowsza_fale` — „tak” oznacza, że dla tego produktu obowiązuje ocena z nowszego etapu; „nie – klasyfikacja sporna” (Home Energy Planner dla ENER-03, OverlineIQ dla RENT-01) oznacza, że rozstrzyga ręczna weryfikacja (K-03); „nie – brak oceny w nowszej fali” (np. BiggerPockets Sell vs Keep dla RENT-01) oznacza, że nowsza fala tego narzędzia nie oceniała. W tekstach raportu kategorię „sporny” stosujemy tylko do wierszy niezastąpionych nowszą oceną.
- `status_weryfikacji` — zawsze „strona nieotwierana”, z dopiskiem o niezgodnym URL albo o potrzebie ręcznej weryfikacji.
- Fala 2b: agent podał listę 8 zapytań, ale nie przypisał kandydatów do konkretnych zapytań; kolumna `kwerenda` zawiera więc pełną listę 8 zapytań z dopiskiem „kandydat nieprzypisany”.

## Skrypty i odtwarzalność

- `tools/economics_model.py` — samodzielny generator `economics.csv`: `python3 research/tools/economics_model.py`.
- Pozostałe skrypty składały CSV, karty i rejestr z wyników agentów. Wymagają katalogu roboczego, w którym `raw/` to kopia `data/agent-outputs/`, a pliki z `tools/inputs/` (`top10_head.md`, `top10_rankings.md`, `evidence_head.md`) leżą w katalogu głównym, obok podkatalogu `tools/` ze skryptami. Kolejność: `allideas.py` → `raw/all_ideas.json`; `build_longlist.py` (z `longlist_map.py`) → `raw/longlist.json`; `build_outputs.py` → oba CSV; `build_top10.py` (woła `build_cards.py`, czyta `product-opportunities.csv`) → `top-10-products.md`; `evidence.py` → `raw/evidence_rows.json`, potem `build_evidence.py` (z `evidence_overrides.json`) → `evidence-and-assumptions.md`; `build_annex_4_1.py <raw> <market.md> <wyjście>` → aneks §4.1 w `market-and-distribution.md`.
- **Uwaga:** `build_outputs.py`, `build_top10.py`, `build_cards.py` i `build_evidence.py` zapisują wyniki pod ścieżką `/home/user/trackal/research/` (ścieżka z sesji badawczej) — przed uruchomieniem w innym miejscu trzeba ją zmienić. Pliki `.md` poza generowanymi częściami redagowano też ręcznie, więc skrypty odtwarzają strukturę i dane, a nie każde zdanie.

## Ograniczenia, o których trzeba pamiętać przy lekturze

- Odczyt stron był zablokowany przez politykę sieci (WebFetch, curl), więc dowody o konkurencji i rynku pochodzą ze streszczeń wyników wyszukiwania; funkcji narzędzi nie testowano.
- Nie było dostępu do danych SEO (wolumeny, pozycje) ani do testów asystentów AI; zamiast wyników jest plan testu.
- Wspólny limit 200 wyszukiwań na turę ograniczył część agentów fali 1.
- Liczby ekonomiczne to scenariusze na założeniach, nie prognoza.

Szczegóły: `evidence-and-assumptions.md` §1.
