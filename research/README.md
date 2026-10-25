# Research: serwis symulatorów decyzji (USA) — indeks plików

Badanie z 2026-10-25. Start: `executive-summary.md`.

| Plik | Zawartość |
|---|---|
| `executive-summary.md` | werdykt, najważniejsze dowody, ryzyka, rekomendacja, ekonomika, pierwszy eksperyment, warunek przerwania |
| `market-and-distribution.md` | etap A (teza biznesowa), popyt w USA, dystrybucja przez asystentów AI platforma po platformie, etap B (ocena rodzin) |
| `product-opportunities.csv` | długa lista 100 odrębnych pomysłów ze wszystkimi wymaganymi polami, statusem i poziomem weryfikacji |
| `competitor-audit.csv` | rejestr konkurencji (data, kwerenda, URL, konkurent, sprawdzone funkcje, ograniczenia dostępu, wniosek, pewność, podstawa dowodu) |
| `top-10-products.md` | werdykty dla pomysłów startowych A–I, ranking 25 propozycji, rankingi szczegółowe, karty 10 finalistów z promptami testowymi |
| `economics.csv` | model scenariuszowy (konserwatywny / bazowy / optymistyczny) z jednostkami i opisem założeń |
| `architecture-and-validation.md` | etap G (domeny), etap H (architektura), pilotaż 5 produktów, plan 30/60/90, kryteria decyzji, protokół testu asystentów |
| `evidence-and-assumptions.md` | metoda i ograniczenia, status zadań, źródła pierwotne, rejestr założeń, sprzeczności, kolejka badań, rejestr 245 dowodów |
| `tools/economics_model.py` | generator `economics.csv` (`python3 research/tools/economics_model.py`) |
| `tools/*.py` (pozostałe) | skrypty, które złożyły CSV i karty z wyników agentów; uruchamiano je w katalogu roboczym, w którym `raw/` = `data/agent-outputs/` |
| `data/agent-outputs/` | surowe, ustrukturyzowane wyniki agentów (JSON): fundamenty, uzupełnienia, weryfikacje, rodziny, pomysły startowe, audyty, próby obalenia, popyt |

**Ograniczenia, o których trzeba pamiętać przy lekturze:**
- odczyt stron był zablokowany przez politykę sieci, więc dowody o konkurencji pochodzą ze streszczeń wyników wyszukiwania;
- nie było dostępu do danych SEO ani do testów asystentów AI;
- wspólny limit 200 wyszukiwań na turę ograniczył część agentów fali 1.

Szczegóły: `evidence-and-assumptions.md` §1.
