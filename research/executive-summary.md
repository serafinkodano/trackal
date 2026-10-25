# Streszczenie wykonawcze — serwis symulatorów decyzji (USA)

Data: 2026-10-25 · Zespół: badanie wieloagentowe (~80 agentów, kilkaset zapytań), synteza i kalibracja własna · Odwołania `E-…` → `evidence-and-assumptions.md`

## 1. Werdykt

**Budować warunkowo — i tylko w wersji znacznie węższej niż hipoteza.**

- **Nie budować** wersji „setki zaawansowanych symulatorów na jednej domenie, monetyzowane AdSense, z ruchem głównie z asystentów AI”. Kluczowe założenia tej wersji nie przeszły weryfikacji (sekcja 3).
- **Warunkowo:** jedna domena o spójnej granicy (duże decyzje pieniężne wokół domu i auta), **5 symulatorów na jednym silniku**. Najpierw **2-tygodniowa bramka pomiarowa** (koszt ≈ 0 USD), która rozstrzyga, czy w ogóle zaczynać budowę.
- Jeśli bramka wypadnie negatywnie, a właściciel nie zaakceptuje Google organic jako kanału bazowego: **nie budować** (sekcja 8).

## 2. Najważniejsze dowody

1. **Ruch z asystentów AI jest mały i skoncentrowany.** To 0,1–1% ruchu typowej witryny (Ahrefs: 0,28% w III 2026 na 74 752 stronach; Conductor: 1,08% dla domen enterprise) [E-VER-C5]. ChatGPT daje 81–95% referencji AI [E-AI-03]. Tylko **6,8%** odpowiedzi ChatGPT (USA, desktop) zawiera link, w finansach 8% [E-VER-C3]. Największy katalog kalkulatorów (omnicalculator.com) dostaje z ChatGPT, Claude i Gemini rzędu **0,05% ruchu** (szacunek Semrush) [E-VER-C4].
2. **Asystenci sami budują kalkulatory.** 7.10.2026 OpenAI udostępniło wszystkim użytkownikom ChatGPT „Intelligent UI” (kalkulatory, formularze, wykresy w odpowiedzi) [E-VER-C2]. Google od 19.08.2026 generuje interaktywne narzędzia w AI Mode globalnie po angielsku i wprowadza je do AI Overviews [E-VER-C1]. Interakcja z narzędziami przenosi się do czatu (MCP Apps, aplikacje w ChatGPT bez monetyzacji usług cyfrowych) [E-VER-C10]. Platformy monetyzują intencję u siebie (reklamy w ChatGPT od 9.02.2026) [E-VER-C9].
3. **Google też oddaje mniej kliknięć.** AI Overviews obniżają CTR o 35–61% [E-AI-06..08]. W randomizowanym eksperymencie AI Mode obniżył kliknięcia zewnętrzne o 18,8 pp [E-VER-C6]. Długie pytania decyzyjne mają najwyższy odsetek AI Overviews [E-AI-11].
4. **AdSense płaci za wyświetlenia, a symulator ma ich mało.** Płatność za wyświetlenie (80% po opłacie kupującego, ~68% efektywnie), zakaz odświeżania bez działania użytkownika [E-VER-C7]. Strony-narzędzia mają ~1–1,5 odsłony na sesję [E-ADS-26]. Reklamy nie mogą sąsiadować z elementami interaktywnymi [E-ADS-03].
5. **Głębokie narzędzia decyzyjne nie żyją z display.** ProjectionLab (subskrypcja, ~1 mln USD ARR), Boldin, DealCheck (freemium), FI Calc (darowizny), Rewiring America (non-profit, B2B embed). NerdWallet (836,6 mln USD przychodu w FY2025) i SmartAsset to biznesy lead-gen [E-POR2-01..07]. Display działa u Omni Calculator przy ~3,7 tys. kalkulatorów, 18–23 mln wizyt/mies. i ~70 osobach zespołu [E-POR2-05].
6. **„Luki integracyjne” szybko się zamykają.** W 2025–2026 powstał zalew mikro-serwisów z kalkulatorami. Pomysły startowe B, F i H oraz kandydat RET-03 mają konkurentów bezpośrednich lub prawie bezpośrednich: „Insurance Deductible Optimizer”, Home Energy Planner, BiggerPockets „Sell vs. Keep”, RothHelper/QuantCalc. W 24 z 25 audytów nie znaleziono konkurenta bezpośredniego, ale wszędzie fragmenty pokrywają darmowe narzędzia, a ocena opiera się na streszczeniach wyszukiwarki (strony nieotwierane).
7. **Popyt przesuwa się w stronę „zostać i remontować”.** Mediana posiadania domu 12 lat, sprzedaż domów najniższa od 1995 r., rosnące home equity [E-DEM-02, E-DEM-04, E-DEM-05]. Duży przepływ decyzji: 7,75 mln dostaw AC/pomp ciepła w 2025 r. [E-DEM-08]; 29,1% wymian aut z kredytem ma ujemny kapitał [E-DEM-14]. PV i generatory słabną po wygaśnięciu 25D i przy braku dużych awarii [E-DEM-10, E-DEM-12].
8. **Automatyczne utrzymanie ma granice.** W 12 miesiącach zmieniły się kluczowe reguły (25D, NFIP wygasający dwukrotnie, zniżki FORTIFIED, ACA PTC, RAP), a parametry polityk nie mają stabilnych API [E-REG3-*, E-REG2-*]. Tematy finansowe to YMYL z wyższą poprzeczką jakości [E-ADS-08].

## 3. Ryzyka (od największego)

1. **Kanał AI nie dostarczy wolumenu** (0,1–1%) i jest podatny na decyzje jednej firmy: −52% w VII–VIII 2025, +158% tydzień do tygodnia w V 2026 [E-AI-04].
2. **Substytucja przez generatywne UI asystentów** — interaktywność przestała być przewagą.
3. **Niski przychód na sesję** (bazowo ~7 USD na 1000 sesji) → potrzeba ~150 tys. sesji/mies. na 1000 USD.
4. **Ryzyko algorytmiczne i polityk:** scaled content abuse, sygnały site-wide, odrzucenie AdSense dla „low value content” [E-ADS-06, E-ADS-09, E-POR2-08]. Jedno konto reklamowe to jeden punkt awarii [E-ADS-05].
5. **Koszt utrzymania i eksperta** rośnie z każdą kategorią YMYL.
6. **Konflikt celów:** widoczność w AI koreluje z obecnością marki poza witryną (YouTube, Reddit, Wikipedia) [E-POR2-12], a model wyklucza budowę społeczności i dystrybucję linków.

## 4. Rekomendacja zakresu

- **Pozycjonowanie (1 zdanie):** *Neutral, assumption-transparent simulators for big home and car money decisions — compare your real options over time and see exactly what would flip the answer.* (PL: neutralne, jawne w założeniach symulatory dużych decyzji pieniężnych wokół domu i auta — porównanie realnych wariantów w czasie i progi, przy których odpowiedź się zmienia.)
- **Domena:** jedna, o spójnej funkcji decyzyjnej (wariant B). Kategorie w podkatalogach, aby łatwo je wydzielić. Poza zakresem: emerytura, podatki osobiste, zdrowie (test raczej na healthscorer.com), opieka, kredyty studenckie, e-commerce (ewentualnie osobna domena). Szczegóły: `architecture-and-validation.md` §1.
- **Pięć produktów pilotażowych** (kolejność budowy; szczegóły w `top-10-products.md`):
  1. **RENO-02** — *Aging Roof: Replace, Repair, Fortify or Wait (insurance, sale horizon, optional solar)*;
  2. **RENO-03** — *AC or Furnace Just Died: Repair vs Like-for-Like vs Heat Pump vs Dual-Fuel*;
  3. **HOME-04** — *Remodel vs Move (rate lock-in aware)*;
  4. **HOME-02** — *Sell vs Rent Out When Moving (§121 clock & low-rate value)*;
  5. **AUTO-01** — *Underwater Car Loan Exit Planner (keep, trade now, wait, sell privately, pay the gap)*.
- **Architektura:** kilkanaście współdzielonych silników (oś czasu przepływów, finansowanie, wartość domu, ubezpieczenie, podatek od sprzedaży, amortyzacja i deprecjacja auta). Symulatory jako konfiguracje, obliczenia w przeglądarce, treść w HTML renderowanym po stronie serwera, LLM tylko do redakcji opisów. Szczegóły: `architecture-and-validation.md` §2.

## 5. Ekonomika (rząd wielkości, bez pozornej precyzji)

| | Konserwatywnie | Bazowo | Optymistycznie |
|---|---|---|---|
| Przychód reklamowy na 1000 sesji (średnia roczna) | ~2 USD | ~7 USD | ~22 USD |
| Sesje/mies. dla 1 000 USD | ~550 tys. | ~140 tys. | ~45 tys. |
| Sesje/mies. dla 3 000 USD | ~1,6 mln | ~430 tys. | ~130 tys. |
| Sesje/mies. dla 10 000 USD | ~5,5 mln | ~1,4 mln | ~450 tys. |
| Próg rentowności gotówkowej (5 narzędzi) | ~480 tys. sesji | ~50 tys. sesji | ~8 tys. sesji |
| Próg rentowności z wyceną czasu właściciela (5 narzędzi) | ~1,3 mln sesji | ~160 tys. sesji | ~24 tys. sesji |
| Uruchomienie: gotówka / czas właściciela | ~14 tys. USD / ~520 h | ~6 tys. USD / ~315 h | ~2,6 tys. USD / ~190 h |

Wszystkie wartości to **założenia** skalibrowane do zakresów rynkowych (`economics.csv`, `tools/economics_model.py`).

Przy 25 narzędziach z ruchem 1 000 USD/mies. oznacza bazowo średnio ~6 tys. sesji/mies. **na każde** narzędzie. Katalog nie zastępuje ruchu na narzędzie, a ruch rozkłada się potęgowo.

Lead-gen/afiliacja (osobny model, poza bazą) dałaby ilustracyjnie 20–500 USD na 1000 sesji. To pokazuje, dlaczego rynek głębokich narzędzi finansowych zarabia głównie na leadach.

## 6. Pierwszy eksperyment (dni 0–14, ~0 USD)

1. **Logi healthscorer.com:** ile jest *ludzkich* sesji z referrerem lub `utm_source` asystentów po odfiltrowaniu pobrań botów (`ChatGPT-User`, `Claude-User`…) i ile zarabiają.
2. **Panel promptów:** 5 asystentów × prompty z `top-10-products.md` × 3 powtórzenia. Mierzymy: % odpowiedzi z linkiem do zewnętrznego narzędzia, % z samodzielnie wygenerowanym kalkulatorem, pominięte zależności.
3. **Ręczna weryfikacja** najbliższych konkurentów 5 produktów (strony, formularze).

**Bramka G0:** budujemy RENO-02, jeśli spełniony jest przynajmniej jeden warunek:
- ≥ 10% odpowiedzi na prompty z prośbą o kalkulator linkuje do zewnętrznego narzędzia;
- healthscorer.com ma ≥ 300 ludzkich sesji z AI/mies.;
- właściciel świadomie przyjmuje Google organic jako kanał bazowy.

## 7. Granice pewności

- Funkcje konkurentów oceniono **bez otwierania stron** (blokada sieci). Twierdzenia „nie znaleziono konkurenta bezpośredniego” mają pewność niską–średnią, a negatywne streszczenia wyszukiwarki to słaby dowód.
- **Brak wolumenów słów kluczowych** i **brak testów asystentów**; wyników nie symulowano.
- Część agentów fali 1 miała tylko 4–11 zapytań (wspólny limit wyszukiwań); ich wnioski uzupełniono falą „top-up”, ale oceny rodzin mają niską–średnią pewność.
- RPM to najsłabiej zmierzony parametr (zakresy vendorskie różnią się kilkukrotnie). Rozstrzygnie go dopiero pilotaż.

## 8. Warunek przerwania projektu

Przerwać, jeśli:
- bramka G0 wykaże brak linkowania do narzędzi, a właściciel nie przyjmie Google organic jako kanału bazowego;
- **albo** po 6 miesiącach od publikacji pierwszych 3 symulatorów przychód reklamowy jest < ~100 USD/mies. i ruch nie rośnie przez 3 kolejne miesiące;
- **albo** domena dostanie karę obejmującą całą witrynę.

Dalsza praca miałaby wtedy sens tylko w innym modelu (lead-gen, B2B embed, subskrypcja) i jako osobna decyzja.
