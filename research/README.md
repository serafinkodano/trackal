# Research: serwis symulatorów decyzji (USA) — indeks plików

Badanie z 2026-10-25, poprawione po recenzji adwersaryjnej (fala 3). Start: `executive-summary.md`.

| Plik | Zawartość |
|---|---|
| `executive-summary.md` | werdykt, pozycjonowanie, domena, najważniejsze dowody, ryzyka, rekomendacja zakresu (5 pilotów), trzy obalone założenia (§4a), trzy największe niewiadome (§4b), ekonomika, strategie alternatywne, pierwszy eksperyment (bramka G0), granice pewności, warunek przerwania |
| `market-and-distribution.md` | etap A (teza biznesowa, lejek marki w asystentach), popyt w USA, dystrybucja przez asystentów AI platforma po platformie, etap B (ocena 35 rodzin z kartami uzasadnień) |
| `product-opportunities.csv` | długa lista: 96 wierszy, 95 odrębnych pomysłów (RENO-01 jest gałęzią RENO-02), wszystkie wymagane pola, status, kalibracja i poziom weryfikacji |
| `competitor-audit.csv` | rejestr konkurencji: 1106 wierszy z fal 1, 2 i 2b (data, kwerenda, URL, konkurent, sprawdzone funkcje, ograniczenia dostępu, wniosek, pewność, podstawa dowodu i kolumny kontrolne opisane niżej) |
| `top-10-products.md` | werdykty dla pomysłów startowych A–I, metoda selekcji, ranking 25 audytowanych pozycji (24 odrębne), uzasadnienia per kryterium, rankingi szczegółowe, karty 10 finalistów z promptami testowymi |
| `economics.csv` | model scenariuszowy (konserwatywny / bazowy / optymistyczny) z jednostkami, typem wartości i opisem założeń; 36-miesięczna ilustracja trajektorii |
| `architecture-and-validation.md` | etap G (domeny), etap H (architektura), pilotaż 5 produktów, plan 30/60/90, bramka G0, kryteria decyzji, protokół testu asystentów |
| `evidence-and-assumptions.md` | metoda i ograniczenia, status zadań, źródła pierwotne, rejestr założeń, sprzeczności, kolejka badań, korekty po recenzji, rejestr dowodów (E-…, w tym E-REV-01…09) |
| `tools/` | skrypty generujące pliki (opis niżej) |
| `data/agent-outputs/` | surowe, ustrukturyzowane wyniki agentów (JSON): fundamenty, uzupełnienia, weryfikacje, rodziny, pomysły startowe, audyty, próby obalenia, popyt, kalibracja, statusy końcowe |

## Słownik kolumn CSV

**`product-opportunities.csv`**

- `status` — tylko 4 wartości: `pilot` (kandydat do pilotażu po bramkach, nie decyzja o budowie), `zbadać`, `później`, `odrzucić`. Kwalifikatory („gałąź RENO-02”, „osobna domena”, „test na healthscorer.com”, „poza zakresem startowym domeny”) są w kolumnie `uwaga_statusu`.
- `poziom_pewnosci (oceny/statusu)` — pewność **decyzji o statusie**, nie siła pojedynczego dowodu. Pomysły bez wyszukiwań („koncepcyjne”) mają zawsze „niska”.
- `poziom_weryfikacji` — `koncepcyjny (bez wyszukiwań przypisanych do tego pomysłu)`; `wstępnie sprawdzony w wyszukiwarce (fala 1; N wierszy search-summary)`; `audyt fali 2 (7 zapytań)`; dla 10 finalistów dodatkowo `próba obalenia fali 2b (8 zapytań) + badanie popytu fali 2b`. Wszędzie: strony nieotwierane, dowód ze streszczeń wyszukiwarki.
- `rekomendacja_audytora (top 25)`, `ocena_agenta_0_5 (top 25)`, `ocena_po_kalibracji_0_5 (top 25)`, `zmienione_kryteria_w_kalibracji` — ślad od audytu do decyzji. Gdy status różni się od rekomendacji audytora, powód jest na początku `uzasadnienie_statusu`.
- `bezposredni_konkurent (top 25)` — formuła „Nie znaleziono bezpośredniego konkurenta w badanym zakresie” z zakresem i pewnością; „sporny” tam, gdzie fale klasyfikują ten sam URL różnie.
- `odrebny_pomysl` — „nie” tylko dla RENO-01 (scalony z RENO-02).
- `uwagi_scalenia_i_bliskie_duplikaty` — scalenia i bliskie duplikaty (warianty jednego silnika).
- Wpis „… — ocena koncepcyjna agenta; nie badano w tej sesji (brak danych)” oznacza pole, którego agent nie oparł na żadnym dowodzie.
- Brakujące numery ID (FIN-04, INS-07, JOB-10, CARE-02) to pomysły scalone po recenzji odpowiednio z LIFE-04, INS-03, RET-05 i FIN-02; ich źródła są w `scalone_z_pomyslow_agentow`.

**`competitor-audit.csv`**

- `produkt_ID_agenta` — identyfikator użyty przez agenta (np. „Seed B”, „G2-01, G2-03”); `produkt_ID_final` — ID z `product-opportunities.csv` (lista rozdzielona „;”). Wierszy bez przypisania: 0.
- `typ_wiersza` — `konkurent` / `sygnał_popytu` / `źródło_reguł_lub_danych` / `brak_wyniku`. Liczniki konkurentów licz tylko z `konkurent`.
- `klasyfikacja (automatyczna z wniosku)` — `bezpośredni` / `prawdopodobnie bezpośredni (niezweryfikowany)` (wiersze z wiedzy modelu) / `sporny (częściowy lub bezpośredni)` / `częściowy` / `substytut` / `niezweryfikowany` / `nie-konkurent`; wyprowadzona z pierwszego określenia we wniosku agenta, więc przy decyzjach czytaj też `wniosek` (np. wiersze „DIRECT dla G6-03; PARTIAL dla G6-02” dotyczą dwóch produktów naraz).
- `podstawa_dowodu` — `search-summary – opis w wyniku wyszukiwania`; `wyszukiwanie wykonane – brak w wynikach; wiedza modelu`; `wiedza modelu – bez wyszukiwania`; `notatka fali 1 – niepotwierdzona w fali 2`. Pewność wierszy z wiedzy modelu lub z URL innego podmiotu jest ograniczona do „niska”, a wierszy search-summary do „średnia” (żadnej strony nie otwarto).
- `url_zgodny_z_nazwa_konkurenta` — „nie” oznacza, że URL to wzmianka lub artykuł innego serwisu, a strona narzędzia jest nieustalona.
- `uwaga_reguly_9` — wniosek mówi o braku funkcji, choć strony nie otwarto; czytać jako „niezweryfikowane”, nie „brak”.
- `konflikt_klasyfikacji` — ten sam URL lub konkurent sklasyfikowany różnie w różnych wierszach; `zastapiony_przez_nowsza_fale` — dla tego produktu obowiązuje ocena z nowszego etapu.
- Fala 2b: agent podał listę 8 zapytań, ale nie przypisał kandydatów do zapytań; pełna lista jest w `data/agent-outputs/refute_<ID>.json` (pole `queries_run`).

## Skrypty i odtwarzalność

- `tools/economics_model.py` — samodzielny generator `economics.csv`: `python3 research/tools/economics_model.py`.
- Pozostałe skrypty składały CSV, karty i rejestr z wyników agentów. Uruchamia się je w katalogu roboczym, w którym `raw/` = `data/agent-outputs/`, a pliki tekstowe z `tools/inputs/` leżą w katalogu głównym: `build_longlist.py` (z `longlist_map.py`) → `raw/longlist.json`; `build_outputs.py` → oba CSV; `build_top10.py` (woła `build_cards.py`) → `top-10-products.md`; `evidence.py` + `build_evidence.py` → `evidence-and-assumptions.md`.

## Ograniczenia, o których trzeba pamiętać przy lekturze

- Odczyt stron był zablokowany przez politykę sieci (WebFetch, curl), więc dowody o konkurencji i rynku pochodzą ze streszczeń wyników wyszukiwania; funkcji narzędzi nie testowano.
- Nie było dostępu do danych SEO (wolumeny, pozycje) ani do testów asystentów AI; zamiast wyników jest plan testu.
- Wspólny limit 200 wyszukiwań na turę ograniczył część agentów fali 1.
- Liczby ekonomiczne to scenariusze na założeniach, nie prognoza.

Szczegóły: `evidence-and-assumptions.md` §1.
