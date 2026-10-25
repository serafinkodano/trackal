# -*- coding: utf-8 -*-
"""Generuje aneks §4.1 „Karty rodzin (uzasadnienia ocen)” do market-and-distribution.md.

Źródła: research/data/agent-outputs/family_G1..G7.json (pola families[]: scores, *_pl),
tabela §4 w market-and-distribution.md (oceny po korektach). Teksty kart to skróty
uzasadnień agentów rodzin (bez nowych ocen); podstawa oceny wynika z listy
queries_run danego agenta. Skrypt sprawdza zgodność ocen z tabelą §4.

Użycie: python3 build_annex_4_1.py <katalog_raw> <market.md> <wyjście.md>
"""
import json
import re
import sys

RAW, MARKET, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

KEYS = ['demand', 'commercial', 'integrated_gap', 'ai_fit', 'shared_modeling',
        'data_cost_ease', 'low_error_risk', 'catalog', 'ad_fit', 'low_expert_cost']
LABELS = ['Pop', 'Kom', 'Luka', 'AI', 'Wsp', 'Dane', 'Błąd', 'Kat', 'Rekl', 'Eksp']

# Udane wyszukiwania agentów rodzin (z queries_run; wpisy oznaczone jako wykonane).
QUERIES = {1: 4, 2: 0, 3: 3, 4: 5, 5: 0, 6: 4, 7: 4}

BASIS = {
    'S': 'search-summary',
    'R': 'search-summary tylko dla zmian ulg, reszta z wiedzy modelu',
    'M': 'wiedza modelu — agent rodziny nie wykonał wyszukiwań dla tej rodziny z powodu limitu',
}

# (indeks rodziny w family_G*.json liczony od 1, korekty ocen z tabeli §4, kod podstawy,
#  opis podstawy, pewność, tekst karty)
CARDS = [
    (9, {'low_expert_cost': 3}, 'M',
     'agent G3 nie szukał danych o autach (limit); skalę zdarzeń (transakcje, nie popyt online) uzupełniono w fali uzupełniającej [E-DEM-13, E-DEM-14, E-REV-07]; AUTO-01…03 w audycie fali 2, AUTO-01 także w fali 2b',
     'niska dla rodziny; niska–średnia dla AUTO-01',
     'Popyt 5: w 2026 prognozuje się 16,1 mln nowych i 38,5 mln używanych aut, a ok. 29–31% aut oddanych w rozliczeniu (trade-in) przy zakupie nowego auta miało ujemny kapitał (Edmunds, Q1–Q3 2026; mianownik w streszczeniach niejasny) [E-DEM-13, E-DEM-14, E-REV-07]; to przepływ transakcji, nie zmierzony popyt na narzędzie. '
     'Luka 3: setki jednocelowych kalkulatorów (rata, lease vs buy, rollover ujemnego kapitału) oraz TCO modeli (Edmunds, KBB) pokrywają fragmenty, ale połączenia awarii, ujemnego kapitału, refinansowania i horyzontu agent nie wskazał; w audycie AUTO-01 nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 3: proste przypadki asystent policzy sam; przewagą narzędzia jest krzywa kapitału w czasie i kilka ścieżek z ryzykiem kolejnych napraw. '
     'Komercyjność 5 i reklama 5 to hipotezy (kredyty, ubezpieczenia, dealerzy; stawek nie sprawdzano). '
     'Wykonalność: matematyka deterministyczna i testowalna (Błąd 4), ale brak tanich danych o wartości aut (Dane 2: wyceny KBB, Edmunds, Black Book są płatne lub zamknięte); jeden silnik obsłuży kilkanaście decyzji (Wsp 5). '
     'Eksp obniżono z 4 do 3, bo przegląd AUTO-01 nie jest tani: według szacunku fali 2b to ok. 24–36 h (specjalista finansowania aut 8–12 h, CPA ds. sales tax dla tabeli 51 jurysdykcji 10–14 h, recenzent ilościowy 4–6 h, prawnik lub compliance 2–4 h).'),
    (4, {}, 'M',
     'agent G2 nie wykonał żadnego wyszukiwania (limit); skalę zdarzeń (kwoty i sztuki, nie popyt online) uzupełniono w fali uzupełniającej [E-DEM-06, E-DEM-07, E-DEM-08, E-REV-06]; RENO-01…04 w audycie fali 2, RENO-02…04 także w fali 2b',
     'niska dla rodziny; niska–średnia dla RENO-02 i RENO-03',
     'Popyt 4: wydatki właścicieli na remonty to ok. 518–526 mld USD rocznie, a dostawy AC i pomp ciepła 7,75 mln sztuk w 2025 [E-DEM-06, E-REV-06, E-DEM-08]; to kwoty i sztuki, nie gospodarstwa ani decyzje, a ok. 5 mln wymian dachów rocznie to szacunek o niskiej wiarygodności [E-DEM-07]. '
     'Luka 4, najwyższa wśród rodzin domowych: narzędzia jednodomenowe są liczne (EnergySage, PVWatts, Rewiring America, cost guides Angi/Fixr, HomeZada), ale agent nie wskazał narzędzia optymalizującego kolejność inwestycji z zależnościami, budżetem i horyzontem sprzedaży; w audytach RENO-01…04 nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 3: pytania o jeden element asystent obsłuży regułami kciuka; narzędzie zyskuje przy danych lokalnych, kilku elementach naraz i horyzoncie sprzedaży. '
     'Komercyjność 5 i reklama 4 to hipotezy (wykonawcy, finansowanie, retail); ryzyko: najlepiej płacący reklamodawcy wolą lead-gen niż display. '
     'Wykonalność średnia: brak darmowych lokalnych kosztów (Dane 3), zmienność zachęt po OBBBA i przegląd dekarza, inżyniera HVAC oraz agenta ubezpieczeniowego (Eksp 3); wspólny szkielet: model elementu domu, graf zależności, finansowanie, horyzont sprzedaży (Wsp 4).'),
    (3, {}, 'M',
     'agent G2 nie wykonał żadnego wyszukiwania (limit); skalę zdarzeń (transakcje, nie popyt online) uzupełniono w fali uzupełniającej [E-DEM-04, E-DEM-05]; HOME-01…04 w audycie fali 2, HOME-02 i HOME-04 także w fali 2b',
     'niska',
     'Popyt 4: sprzedaż istniejących domów 4,06 mln w 2025 (najmniej od 1995) i mediana posiadania 12 lat [E-DEM-04, E-DEM-05] wskazują na efekt zamrożenia stóp, który podnosi wagę decyzji „sprzedać czy wynająć” i „remontować czy się przeprowadzić” (hipoteza). '
     'Luka 3: dobrze finansowani gracze lead-gen (HomeLight, Knock, Orchard, Opendoor, Zillow, Redfin) mają kalkulatory częściowe i stronnicze; w audytach HOME-01…04 nie znaleziono bezpośredniego konkurenta w badanym zakresie, ale TrueHomeCosts, Bellhaven i TeamzLab mogą pokrywać część luki HOME-02 (fala 2b), a w kalibracji luka HOME-02 i HOME-04 spadła do 2. '
     'AI 3: asystent poda regułę „2 z 5 lat” i przybliżony rachunek; narzędzie ma przewagę przy osi zdarzeń, kwalifikacji kredytowej i podatku §121. '
     'Ryzyko błędu jest wysokie (Błąd 2: §121, recapture, DTI, reguły stanowe), a przegląd wymaga CPA/EA i loan officera (Eksp 3); dane są w większości darmowe lub od użytkownika (Dane 4). '
     'Katalog to realnie 10–15 odrębnych decyzji, nie setki (Kat 4), na wspólnym silniku osi czasu (Wsp 5).'),
    (1, {}, 'S',
     '4 wyszukiwania agenta G1 (NY Fed, HELOC, RAP, HEI vs HELOC), potem limit; skalę zdarzeń (transakcje, nie popyt online) uzupełniono w fali uzupełniającej [E-DEM-01, E-DEM-02, E-DEM-03, E-REV-08]; FIN-01 i FIN-02 w audycie fali 2, FIN-01 także w fali 2b',
     'niska dla popytu (dane o transakcjach, nie popyt online); niska–średnia dla luki',
     'Popyt 4: skala transakcji jest najlepiej udokumentowana wśród rodzin. Rośnie liczba nowych kredytów home equity (HELOC 1,4–1,5 mln w 2025; HELOC + HELOAN 2,55 mln), a kredyty gotówkowe osiągnęły rekord 7,2 mln w Q3 2025 [E-DEM-02, E-DEM-03]; to transakcje, nie popyt na narzędzie. '
     'Luka 3: duzi wydawcy (Bankrate, NerdWallet) mają wiele pojedynczych kalkulatorów, heireview.com porównuje dostawców HEI, a studentloancalcs.com obsługuje przejście SAVE → RAP; dla pełnego porównania instrumentów dostępu do kapitału z domu nie znaleziono bezpośredniego konkurenta w badanym zakresie (FIN-01: 7 + 8 zapytań). '
     'AI 3: proste porównania asystent policzy sam; odesłanie jest bardziej prawdopodobne przy nowych regułach (RAP) i wielofazowych przepływach (hipoteza). '
     'Komercyjność 5 i reklama 4 to hipotezy (stawek nie sprawdzano); ryzyko błędu jest wysokie (YMYL: RAP, IBR, PSLF, odliczalność odsetek), stąd Błąd 2 i przegląd CFP lub analityka kredytowego (Eksp 3). '
     'Jeden silnik miesięcznych przepływów obsłuży większość pomysłów (Wsp 5).'),
    (28, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); fakty regulacyjne zebrano później [E-REG3-06, E-REG3-08, E-REV-05]; RENO-02 i INS-03 w audycie fali 2 i w fali 2b',
     'niska dla rodziny',
     'Popyt 3: decyzje są regionalne i wyzwalane zdarzeniem (sezon huraganów, pożary, pismo od ubezpieczyciela); szkodę zgłasza rocznie ok. 5,3–5,6% ubezpieczonych domów (źródło wtórne, pewność niska) [E-DEM-09]. '
     'Luka 4: strony IBHS, programów stanowych i departamentów ubezpieczeń informują o zniżkach i grantach, ale według agenta nie liczą zwrotu w horyzoncie sprzedaży (hipoteza); w audytach RENO-02 i INS-03 nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 3: asystent obsłuży pytanie ogólnie, a lokalne rundy grantów i rabaty ubezpieczycieli zna tylko z wyszukiwania. '
     'Komercyjność 5 i reklama 5 to hipotezy (home improvement, ubezpieczenia). '
     'Wykonalność ograniczają dane (Dane 2: programy stanowe, tabele rabatów i reguły wieku dachu zmieniają się co kwartał lub co rok; NFIP wygasał co najmniej dwukrotnie w 2025–2026 [E-REV-05]); obejście: rabat i składkę wpisuje użytkownik. '
     'Wspólny silnik decyzji kapitałowych domu z rodziną remontów (Wsp 4).'),
    (17, {}, 'M',
     'agent G6 nie szukał danych dla tej rodziny (limit), oceny to hipotezy; populację opisuje [E-DEM-21]; seed I (fala 1) i BIZ-04 (audyt fali 2) dostarczyły dowodów o konkurencji',
     'niska',
     'Popyt 3: dylemat „większe zamówienie z rabatem vs koszt finansowania i magazynu” dotyczy tylko firm z fizycznym zapasem; ok. 500 tys. aktywnych sprzedawców Amazon w USA to szacunek o niskiej pewności [E-DEM-21]. '
     'Luka 4 to hipoteza agenta; według seeda I płatne narzędzia (Cogsy, 8fig, Float, Inventory Planner) i Shopify Sidekick mogą jednak pokrywać znaczną część problemu (funkcje za logowaniem niezweryfikowane; wiedza modelu), a w audycie BIZ-04 nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 3: asystent policzy prosty przypadek; przewaga narzędzia wynika ze struktury wielookresowej, a nie z danych. '
     'Wykonalność dobra: dane głównie od użytkownika (Dane 4), niski koszt eksperta dzięki doświadczeniu właściciela w e-commerce (Eksp 4) i najlepszy rdzeń modelowy zestawu (Wsp 5: tygodniowy rejestr zapasu i gotówki). '
     'Reklama tylko 3: wąska publiczność B2B i słabe dopasowanie do AdSense; ta tematyka jest poza domeną wariantu B, więc ewentualny test powinien odbyć się w istniejącym serwisie e-commerce właściciela, a osobna domena wchodzi w grę dopiero po spełnieniu warunków 3 i 4 (`architecture-and-validation.md` §1.2).'),
    (31, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); jedynym dowodem pośrednim jest zmiana reguł ACA [E-REG2-13]; bez audytu fali 2',
     'niska',
     'Popyt 4 to hipoteza: dochód 1099 ma bardzo wiele osób, pytanie o S-corp wraca co roku, a samozatrudnieni kupujący plany na Marketplace są dotknięci powrotem klifu 400% FPL [E-REG2-13]. '
     'Luka 3: liczne kalkulatory S-corp i Solo 401(k)/SEP to konkurencja częściowa; połączenie pensji w S-corp, wkładu do 401(k), QBI i dopłat ACA jest prawdopodobnie rzadsze, ale tego nie zbadano. '
     'AI 4: asystent poda regułę kciuka, lecz zależności między pensją, limitami, QBI, MAGI i podatkami stanowymi są podatne na błąd, co daje umiarkowaną szansę odesłania (hipoteza). '
     'Komercyjność 5 i reklama 5 to hipotezy (payroll, księgowość, oprogramowanie podatkowe). '
     'Wykonalność słaba: wysokie ryzyko błędu (Błąd 2) i coroczny przegląd CPA dla każdego obsługiwanego stanu (Eksp 2), dlatego werdykt „później”.'),
    (24, {}, 'S',
     'wyszukiwania agenta G7 o ACA i HSA [E-REG2-10, E-REG2-13, E-REG2-14]; konkurencji agent rodziny nie szukał (limit); RET-03 w audycie fali 2',
     'średnia co do zmiany reguł; niska co do luki',
     'Popyt 3: zmiana reguł jest udokumentowana — enhanced PTC wygasły 31.12.2025 i wrócił klif 400% FPL, a przedłużenie przeszło w Izbie, ale nie w Senacie [E-REG2-13]; wyborów planów na Marketplace było w 2026 ok. 5% mniej niż rok wcześniej [E-REG2-14]; liczby osób blisko progu nie zweryfikowano. '
     'Luka 4 pochodzi z fali 1, w której agent nie szukał konkurencji; audyt RET-03 (fala 2, 7 zapytań) znalazł konkurentów bezpośrednich (RothHelper, QuantCalc ACA Bridge Optimizer; search-summary, pewność średnia), więc ocenę luki trzeba czytać jako zawyżoną (liczby w tabeli nie zmieniano). '
     'AI 4: precyzyjne wyliczenie progu wymaga tabel applicable percentage, SLCSP i FPL, co sprzyja odesłaniu, ale asystent z wyszukiwaniem i wykonywaniem kodu może to policzyć sam (niezweryfikowane dla poszczególnych platform). '
     'Ryzyko błędu jest wysokie, bo jeden dolar ponad próg może kosztować tysiące USD dopłaty (Błąd 2); silnik MAGI i podatków jest wspólny z planem zdrowotnym, spadkami i rodziną 1099 (Wsp 5).'),
    (7, {'integrated_gap': 2}, 'M',
     'agent G3 nie szukał popytu ani konkurencji dla tej rodziny (limit), a jedyny wynik (BLUETTI) był przypadkowy; dane o zdarzeniach i sprzedaży (nie popyt online) z fali uzupełniającej [E-DEM-11, E-DEM-12, E-REV-03]; luka obniżona po fali uzupełniającej seedów (seed F) i audycie ENER-03',
     'niska',
     'Popyt 3: popyt jest epizodyczny i regionalny — w 2024 odbiorcy mieli średnio 11 h przerw, z czego 80% przez zdarzenia ekstremalne [E-DEM-11]; u Generac w Q2 2026 spadały generatory przenośne i magazyny energii, ale generatory standby wróciły do wzrostu [E-DEM-12, E-REV-03]. '
     'Luka obniżona z 4 do 2: Home Energy Planner ma klasyfikację sporną (fala 1: bezpośredni, fala 2: częściowy) i wymaga ręcznej weryfikacji, a rynek wypełniają kalkulatory producentów (Generac, EcoFlow, BLUETTI, Jackery, Tesla, Enphase). '
     'AI 3: dobór mocy asystent policzy sam; przewagą narzędzia jest porównanie technologii w czasie (koszt 10-letni, przerwy wielodniowe i zimowe). '
     'Wykonalność dobra: dane są tanie (EIA-861, EAGLE-I; Dane 4), wystarczy przegląd elektryka (Eksp 4), ale potrzebne są ostrzeżenia bezpieczeństwa (CO, zasilanie zwrotne). '
     'Reklama 4 to hipoteza (reklamy sezonowe); werdykt: ograniczyć; ogólny ENER-03 ma status „później”, a wąski przypadek INS-06 (pompa sump przy przerwie zasilania; gałąź ENER-03, nie odrębny pomysł) wraca razem z nim.'),
    (13, {'integrated_gap': 2}, 'M',
     'agent G5 nie wykonał żadnego wyszukiwania (limit); populację opisuje [E-DEM-18]; luka obniżona po seedzie H (fala 1) i audycie RENT-01 (fala 2)',
     'niska',
     'Popyt 4 to hipoteza agenta: duża, stała populacja drobnych właścicieli (osoby fizyczne mają ok. 59% nieruchomości na wynajem; w 2021 r. 15,9 mln nieruchomości 1–4 lokalowych należało do osób fizycznych [E-DEM-18]) i powtarzalne decyzje o wysokiej stawce; odsetek szukających narzędzia jest nieznany. '
     'Luka obniżona z 3 do 2: BiggerPockets „Sell vs Keep” jest konkurentem bezpośrednim dla rdzenia hold/sell seeda H (search-summary, pewność średnia; dla zakresu RENT-01 — 1031, step-up, sprzedaż ratalna — niezweryfikowany), OverlineIQ ma klasyfikację sporną (fala 1: bezpośredni, fala 2: częściowy), a segment zakupowy (DealCheck, kalkulatory BiggerPockets) jest nasycony. '
     'AI 3: asystent da ramę decyzji, ale łatwo pominie zależności (recapture mimo §121, zawieszone straty pasywne). '
     'Ryzyko błędu jest wysokie (Błąd 2) i wymaga przeglądu CPA lub EA (Eksp 3); dane są tanie (Dane 4), a jeden silnik obsłuży 10–20 symulatorów, wspólny z rodziną opieki (Wsp 5).'),
    (5, {'demand': 2}, 'R',
     '3 wyszukiwania agenta G3 dotyczyły tylko ulg (25D, 25C, 30D); popyt obniżony po fali uzupełniającej [E-REG-01, E-DEM-10]; ENER-01 i RENO-01 w audycie fali 2',
     'średnia dla zmian ulg; niska dla pozostałych ocen',
     'Popyt obniżony z 3 do 2: po wygaśnięciu 25D instalacje domowe spadły w Q2 2026 o 12% r/r, a prognozy na 2026 mówią o spadku o 18–23% [E-REG-01, E-DEM-10]. '
     'Luka 3: ogólne „czy PV się opłaca” jest zatłoczone (PVWatts, EnergySage, SolarReviews, oprogramowanie instalatorów); dla decyzji łączących dach, demontaż PV, horyzont sprzedaży i formę własności w audytach ENER-01 i RENO-01 nie znaleziono bezpośredniego konkurenta w badanym zakresie, choć fragmenty pokrywają m.in. roofcalc.org (seed A). '
     'AI 3: asystent nie zna nasłonecznienia adresu ani taryfy eksportowej, ale przewaga aktualnych założeń jest przejściowa. '
     'Ryzyko błędu jest wysokie (Błąd 2: jedno złe założenie o eksporcie energii odwraca wynik), a okno 48E do 2027 skraca życie części produktów. '
     'Silniki produkcji PV, taryf i finansowania są wspólne z innymi rodzinami (Wsp 5); dlatego forma własności PV (ENER-01, na module PV z RENO-02) i magazyn przy istniejącej PV (ENER-02) to odrębne pomysły ze statusem „później”, a pozostałe pytania PV wchodzą jako gałęzie, na przykład RENO-01 w RENO-02.'),
    (6, {}, 'R',
     'wyszukiwania agenta G3 dotyczyły tylko wygaśnięcia 25C; 0 zapytań o konkurencję; dane o dostawach urządzeń (sztuki, nie popyt online) z fali uzupełniającej [E-DEM-08]; RENO-03 w audycie fali 2 i w fali 2b',
     'niska dla rodziny; niska–średnia dla RENO-03',
     'Popyt 4: każdy dom co kilkanaście lat wymienia HVAC, a dostawy AC i pomp ciepła wyniosły 7,75 mln sztuk w 2025 (sztuki, w tym nowe budownictwo; nie gospodarstwa ani decyzje) [E-DEM-08]; kluczowy moment to awaria pod presją czasu. '
     'Luka 3: Rewiring America i ENERGY STAR to narzędzia częściowe, a kalkulatory producentów i darmowa wycena wykonawcy to substytuty; dla decyzji naprawa / wymiana 1:1 / pompa ciepła / dual-fuel nie znaleziono bezpośredniego konkurenta w badanym zakresie (RENO-03: 7 + 8 zapytań). '
     'AI 3: odpowiedź asystenta bywa ogólnikowa, bo precyzja wymaga stopniodni, krzywych COP i cen paliw. '
     'Po wygaśnięciu 25C model mniej zależy od polityki; dane EIA i NOAA są darmowe, koszty instalacji tylko jako zakresy (Dane 3), potrzebny jest przegląd inżyniera HVAC (Eksp 3). '
     'Moduły są wspólne z podgrzewaczem wody, panelem elektrycznym, PV i zasilaniem awaryjnym (Wsp 4).'),
    (19, {}, 'S',
     '1 wyszukiwanie agenta G6 (lease vs buy z Section 179); bez audytu fali 2',
     'niska',
     'Popyt 3: wydawcy celują w temat (kalkulatory i przewodniki z 2026), ale to sygnał podaży, nie pomiar wolumenu; decyzja dotyczy wielu branż, choć pojedyncza firma podejmuje ją rzadko. '
     'Luka 3: ogólne kalkulatory lease vs buy (SurePayroll) i przewodniki to konkurencja częściowa i substytuty; w jednym wyszukiwaniu nie znaleziono bezpośredniego konkurenta z wbudowanym Section 179 (pewność niska). '
     'AI 3: asystent policzy NPV, ale parametry podatkowe się zmieniają, a źródła sobie przeczą (agent odnotował sprzeczność co do bonus depreciation po OBBBA, niezweryfikowaną). '
     'Wykonalność dobra: limity podatkowe zmieniają się raz w roku (Dane 4), przegląd CPA raz w roku (Eksp 3). '
     'Werdykt „później”: słabsza przewaga właściciela niż w e-commerce, a ocena luki opiera się na jednym wyszukiwaniu.'),
    (25, {}, 'M',
     'agent G7 nie szukał popytu ani konkurencji dla tej rodziny (limit); wnioskowanie pośrednie z danych o ACA i HSA [E-REG2-10]; HLTH-02 w audycie fali 2',
     'niska',
     'Popyt 3 to hipoteza: przejście części zapisanych do planów bronze i zgodność bronze z HSA od 2026 [E-REG2-10] zwiększają ekspozycję na koszty własne, ale liczby takich decyzji nie zmierzono. '
     'Luka 4: CareCredit, szpitalne estymatory cen i serwisy price transparency to konkurencja częściowa (wiedza modelu); w audycie HLTH-02 nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 3: asystent poda zasady (reset udziału własnego, pułapka odsetek odroczonych), ale porównanie miesiąca zabiegu, zmiany planu i sposobu finansowania wymaga modelu. '
     'Ryzyko kliniczne wymaga ograniczenia do zabiegów planowych i wyraźnych zastrzeżeń (Błąd 3); kwoty wpisuje użytkownik z wyceny (Dane 3). '
     'To rodzina najbliższa healthscorer.com, więc ewentualny test powinien odbyć się tam, a nie na nowej domenie (`architecture-and-validation.md` §1.2).'),
    (26, {}, 'S',
     '1 wyszukiwanie agenta G7 (inherited IRA); dom dziedziczony bez wyszukiwań (limit); LIFE-01 w audycie fali 2 i w fali 2b',
     'średnia dla inherited IRA; niska dla domu',
     'Popyt 3: co najmniej 8 przewodników i kalkulatorów reguły 10 lat z 2026 to dowód podaży treści, nie wolumenu; liczby dziedziczonych IRA i domów nie zweryfikowano. '
     'Luka 3: rdzeń inherited IRA (harmonogram wypłat wobec progów podatkowych) obsługują co najmniej 2 darmowe kalkulatory (takehometax.com, onetopstop.insure; konkurencja częściowa), a dla domu dziedziczonego z rodzeństwem (LIFE-01) nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 4: asystent wyjaśni zasady, ale wieloletni harmonogram z obowiązkowymi RMD i podział domu między spadkobierców o różnych stawkach wymagają modelu. '
     'Ryzyko błędu jest wysokie dla IRA (wyjątki EDB, data śmierci względem RBD; Błąd 2) i średnie dla domu; reguły federalne są stabilne (Dane 4). '
     'Silniki MAGI/podatków i nieruchomości są wspólne z innymi rodzinami (Wsp 4).'),
    (23, {}, 'S',
     'wyszukiwania agenta G7 o zapisach ACA, HSA i kalkulatorach HDHP/PPO [E-REG2-10, E-REG2-13, E-REG2-14]; bez audytu fali 2',
     'niska dla popytu (dane o zapisach, nie popyt online); niska co do luki',
     'Popyt 5: na Marketplace w 2026 wybrano plany dla ok. 23 mln osób (−5% r/r) [E-REG2-14], do tego dochodzi coroczny wybór planu u pracodawców; popyt jest silnie sezonowy (okresy zapisów), a liczba osób to nie popyt na narzędzie. '
     'Luka 2: jedno wyszukiwanie zwróciło co najmniej 5 darmowych kalkulatorów HDHP vs PPO z 2026 (konkurencja częściowa), a w środowiskach zamkniętych działają narzędzia pracodawców i HealthCare.gov (niezweryfikowane); dla wariantów złożonych (dwie oferty pracodawców, Marketplace z MAGI) nie znaleziono bezpośredniego konkurenta w badanym zakresie (1 zapytanie, pewność niska). '
     'AI 3: asystent odpowie regułą kciuka i sam przeliczy podane liczby. '
     'Komercyjność tylko 3, bo u pracodawcy użytkownik nie zawiera nowej transakcji. '
     'Silniki kosztu planu, podatków i MAGI są wspólne z innymi rodzinami (Wsp 5), więc sens mają tylko warianty złożone.'),
    (22, {}, 'M',
     'agent G6 nie szukał danych dla tej rodziny (limit); oceny to hipotezy',
     'niska',
     'Popyt 3 i luka 2 to hipotezy: kalkulatorów ROAS i break-even ROAS jest bardzo dużo, a połączenie reklamy, zapasu, gotówki i czasu dostaw jest prawdopodobnie rzadkie (niezweryfikowane). '
     'AI 2: asystent natychmiast policzy break-even ROAS ze zwrotami. '
     'Wykonalność jest bardzo dobra (dane od użytkownika — Dane 5, niskie ryzyko błędu — Błąd 4, kompetencje marketingowe właściciela — Eksp 5), ale komercyjność i reklama to tylko 3. '
     'Rodzina ma sens jako moduł wspólnego silnika zapasu i gotówki (np. skalowanie reklam przy ograniczonym zapasie), a nie jako osobna linia produktów.'),
    (12, {}, 'S',
     'wyszukiwania agenta G4 o Peak 65 i porównaniach planerów [E-DEM-17, E-POR2-03]; RET-03 (pomost ACA) w audycie fali 2',
     'wysoka dla zatłoczenia kategorii; niska dla wąskich luk',
     'Popyt 4: ok. 4,1 mln osób rocznie kończy 65 lat do 2027 [E-DEM-17] (źródło związane z branżą annuity; to demografia, nie popyt na symulator), a płatny rynek planerów pokazuje skłonność do płacenia [E-POR2-03]. '
     'Luka 2: kompleksowe planowanie emerytury jest zatłoczone (Boldin, ProjectionLab, MaxiFi, Pralana, Open Social Security); luka może istnieć tylko w wąskich decyzjach z datą (pension lump sum, relokacja na emeryturze, inherited IRA), a pomost ACA (RET-03) odrzucono po audycie z powodu konkurentów bezpośrednich. '
     'AI 3: reguły asystent poda sam, a przy odsyłaniu prawdopodobnie wskaże znane marki (hipoteza). '
     'Wykonalność jest najsłabsza w zestawie: wiele parametrów zmienia się co roku (Dane 2), decyzje są nieodwracalne i mają klify (Błąd 2), potrzebny jest przegląd CFP lub EA, przy annuity także aktuarialny (Eksp 2). '
     'Komercyjność 5 i wspólny roczny silnik podatkowy (Wsp 5) nie równoważą zatłoczenia.'),
    (14, {}, 'M',
     'agent G5 nie wykonał żadnego wyszukiwania (limit); dane o zasobach i postawach (nie popyt online) z fali uzupełniającej [E-DEM-19, E-DEM-20]; seed G (fala 1) i CARE-01 (audyt fali 2 i fala 2b)',
     'niska',
     'Popyt 4: 63 mln opiekunów rodzinnych (2025), mediana kosztu assisted living 74 400 USD rocznie i 75% osób 50+ chcących zostać w domu [E-DEM-19, E-DEM-20] to zasoby i postawy, a sama decyzja jest epizodyczna i wyzwalana zdarzeniem (upadek, hospitalizacja). '
     'Luka 3: istnieje ponad 10 częściowych kalkulatorów (m.in. Riggins, SeniorCareCalc, A Place for Mom, ParentCareCalc; seed G), ale narzędzia łączącego trajektorię opieki, finansowanie z kapitału w domu i próg Medicaid nie znaleziono (CARE-01: nie znaleziono bezpośredniego konkurenta w badanym zakresie, 7 + 8 zapytań). '
     'AI 3: asystent odpowie jakościowo i odeśle do instytucji; tematy zdrowotno-finansowe mogą skłaniać go do autorytatywnych źródeł (hipoteza). '
     'Ryzyko błędu jest wysokie (look-back Medicaid, HECM; Błąd 2), a przegląd prawnika elder law i CFP drogi (Eksp 2); leady senior living są pod lupą Senatu [E-ADS-34]. '
     'Silnik jest wspólny z rodziną wynajmu (Wsp 4); Medicaid może być tylko progiem ostrzegawczym, nigdy planem.'),
    (15, {}, 'S',
     '1 wyszukiwanie agenta G6 (FBA vs 3PL; sygnały podaży); populację opisuje [E-DEM-21]; BIZ-01 w audycie fali 2',
     'niska–średnia',
     'Popyt 3: dostawcy 3PL i prep center inwestują w zapytanie „FBA vs 3PL” (co najmniej 9 stron), co jest sygnałem podaży, a nie wolumenu; populacja sprzedawców jest wąska [E-DEM-21]. '
     'Luka 3: podstawowe porównanie kosztu na zamówienie pokrywają ecomcalculators.io, Calcbee i Amazon Revenue Calculator (konkurencja częściowa); dla wersji sekwencyjnej z sezonowością, migracją i gotówką w zapasie (BIZ-01) nie znaleziono bezpośredniego konkurenta w badanym zakresie. '
     'AI 3: asystent poda ogólną ramę, ale bez datowanych tabel opłat FBA łatwo poda nieaktualne liczby. '
     'Opłaty FBA trzeba aktualizować co najmniej raz w roku (Dane 3), a koszt eksperta jest niski dzięki doświadczeniu właściciela (Eksp 4). '
     'Reklama 3: wąskie środowisko B2B; nie wiadomo, jaka część tego popytu reklamowego trafia do AdSense.'),
    (21, {}, 'M',
     'agent G6 nie szukał danych dla tej rodziny (limit); oceny to hipotezy',
     'niska',
     'Popyt 2: termin „cash conversion cycle” jest raczej edukacyjny; problem opisuje się słowami „profitable but no cash” czy „should I accept net 60 terms” (hipoteza). '
     'Luka 3: kalkulatory CCC są proste i liczne, a zintegrowane prognozy cash flow to płatne SaaS podpinane do księgowości; luka może istnieć w decyzjach scenariuszowych, np. przyjęcie dużego zamówienia. '
     'AI 2: asystent łatwo policzy CCC. '
     'Dane pochodzą od użytkownika (Dane 5), a rodzina ma bardzo wysoką wartość jako wspólny silnik zestawu e-commerce (Wsp 5), dlatego to moduł, nie rodzina produktów.'),
    (34, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); zmiany reguł potwierdzono później [E-REG2-07, E-REG2-08]',
     'niska',
     'Popyt 4 to hipoteza oparta na zmianach reguł: RAP od 1.07.2026 i likwidacja Grad PLUS dla nowych kredytobiorców [E-REG2-07, E-REG2-08] tworzą nowy problem luki finansowania; popyt jest sezonowy (wiosenne oferty pomocy). '
     'Luka 2: College Scorecard, obowiązkowe Net Price Calculators uczelni, federalny Loan Simulator i kalkulatory pożyczkodawców dają gęstą konkurencję częściową (wiedza modelu, niezweryfikowane). '
     'AI 3: asystent porówna dwie oferty, jeśli dostanie liczby; przewagą narzędzia jest model luki po limitach pożyczek. '
     'Werdykt: nie wchodzić w spłaty (oficjalny symulator), ewentualnie porównanie ofert uczelni po weryfikacji zmian ustawowych i konkurencji.'),
    (10, {}, 'R',
     'wyszukiwania agenta G3 dotyczyły końca ulg EV [E-REG-04]; konkurencja z wiedzy modelu; udział EV z fali uzupełniającej [E-DEM-13]',
     'średnia dla ulg; niska dla pozostałych ocen',
     'Popyt 3: ulgi 30D i 25E nie przysługują dla aut nabytych po 30.09.2025 [E-REG-04], a udział nowych EV ustabilizował się na ok. 6% sprzedaży w 2026 [E-DEM-13], więc pytanie „EV czy hybryda” jest mniej pilne (hipoteza agenta). '
     'Luka 2: rynek jest zatłoczony (DOE AFDC Vehicle Cost Calculator, fueleconomy.gov, Edmunds TCO, kalkulatory utility i mediów; seed D). '
     'AI 2: koszt na milę asystent policzy sam. '
     'Dane o energii i zużyciu są darmowe, ale składek ubezpieczeń brak w danych publicznych, dlatego rodzina ma sens jako moduł silnika samochodowego (np. dwa auta w gospodarstwie, ładowanie bez garażu), a nie jako produkt.'),
    (11, {}, 'S',
     '5 wyszukiwań agenta G4 (porównywarki ofert, JOLTS, Peak 65, planery, Reddit) [E-DEM-15]; JOB-02 w audycie fali 2',
     'niska–średnia',
     'Popyt 3: dobrowolnych odejść z pracy było 38,0 mln w 2025 [E-DEM-15], ale tylko nieznana część zmian pracy wiąże się ze złożoną decyzją (equity, vesting, relokacja, luka w ubezpieczeniu). '
     'Luka 3 dotyczy decyzji zdarzeniowych; podstawowe porównanie ofert jest zatłoczone (co najmniej 9 darmowych kalkulatorów w jednym wyszukiwaniu i gotowe „agent skills”). '
     'AI 2: porównanie ofert asystent robi sam; szansa na odesłanie rośnie przy wielu zależnych datach (vesting, clawback). '
     'Komercyjność i reklama 3: sama oferta pracy nie jest zakupem, a otoczenie kariera/HR jest słabsze niż finanse. '
     'JOB-02 (data odejścia × vesting × clawback) ma status „później”; najbliższy jest Calcuja Golden Handcuff Calculator (seed E).'),
    (18, {}, 'M',
     'agent G6 nie szukał danych dla tej rodziny (limit); wszystkie oceny to hipotezy',
     'niska',
     'Popyt 4 i komercyjność 5 to hipotezy: finansowanie małych firm to duża kategoria, mocno obsadzona przez marketplace’y pożyczkowe. '
     'Luka 2: marketplace’y (Lendio, Nav, Fundera, NerdWallet — z wiedzy modelu) i liczne kalkulatory MCA/APR pokrywają porównanie produktów; luka może istnieć tylko w sekwencji czasowej (most do SBA, refinansowanie MCA). '
     'AI 2: ogólne porównanie asystent obsłuży dobrze. '
     'Ryzyko błędu i koszt eksperta są wysokie (YMYL, sporne przeliczenie factor rate na APR, wymogi stanowe; Błąd 2, Eksp 2), a właściciel nie ma tu przewagi, więc werdykt brzmi: nie wchodzić, najwyżej moduł finansowania w symulatorach zapasów.'),
    (29, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); oceny to hipotezy',
     'niska',
     'Popyt 4 to hipoteza: zwierząt domowych jest bardzo dużo, a pytanie „is pet insurance worth it” często pada na forach. '
     'Luka 2: serwisy porównawcze, blogi afiliacyjne z kalkulatorami i silniki wycen ubezpieczycieli to prawdopodobnie gęsta konkurencja częściowa (bezpośredniego konkurenta nie badano). '
     'AI 2: asystent odpowie sam. '
     'Integracja jest płytka (Wsp 2, Kat 2), krzywe wzrostu składek są zastrzeżone, a temat pasuje lepiej do afiliacji niż do AdSense (hipoteza); werdykt: później, z niskim priorytetem.'),
    (32, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); skalę migracji opisuje [E-DEM-16]',
     'niska',
     'Popyt 4 to hipoteza agenta; w rejestrze jest tylko skala zjawiska: do innego stanu przeprowadziło się 2,1% populacji w 2024 [E-DEM-16]. '
     'Luka 2: SmartAsset, NerdWallet i wiele kalkulatorów podatków stanowych i kosztów życia to gęsta konkurencja częściowa (wiedza modelu); rzadsza jest integracja według typu dochodu, ubezpieczenia domu i roku przejściowego (nie badano). '
     'AI 3: asystent chętnie porówna stany szacunkowo. '
     'Koszt danych jest najwyższy spośród rodzin (Dane 1: podatki stanowe i lokalne, podatki od nieruchomości według hrabstw, ubezpieczenia), a pary stanów to cienkie warianty, nie odrębne produkty.'),
    (30, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); koszty opieki opisuje [E-DEM-19]',
     'niska',
     'Popyt 3: decyzja zapada raz lub kilka razy w życiu (zwykle w wieku 50–70 lat); mediana kosztu assisted living 74 400 USD rocznie [E-DEM-19] pokazuje stawkę. '
     'Luka 3: kalkulatory kosztu opieki (CareScout) są częściowe, a narzędzia agentów ubezpieczeniowych nastawione na sprzedaż (bezpośredniego konkurenta nie badano). '
     'AI 3: asystent wyjaśni opcje; modelowanie prawdopodobieństwa potrzeby opieki i podwyżek składek wymaga narzędzia. '
     'Ryzyko błędu i koszt eksperta są wysokie (horyzont kilkudziesięciu lat, look-back Medicaid; Błąd 2, Eksp 2: aktuariusz lub specjalista LTC), a rynek zdominowali agenci.'),
    (33, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); oceny to hipotezy',
     'niska',
     'Popyt 4 to hipoteza: to częsty dylemat rodziców małych dzieci, popularny na forach. '
     'Luka 3: kalkulatory „cost of working” i „is daycare worth it” są częściowe, a arkusze to substytut (nie badano). '
     'AI 3: prosty przypadek asystent przeliczy sam; przewagą narzędzia jest model wieloletni (koszt opieki według wieku dzieci, utracony wzrost zarobków i match 401(k)). '
     'Komercyjność 2 i reklama 2: użytkownik zwykle niczego nie kupuje na podstawie wyniku, a treści parentingowe mają raczej niskie stawki (hipoteza), stąd werdykt „później”.'),
    (2, {'integrated_gap': 1}, 'M',
     'agent G1 nie wykonał wyszukiwań dla tej rodziny (limit); luka obniżona po audycie seedu B (fala 1) i INS-01 (fala 2)',
     'niska dla rodziny; wysoka dla odrzucenia seedu B (top-10 §0)',
     'Popyt 3: polisy ma bardzo wiele gospodarstw, ale decyzje zapadają w konkretnych momentach (odnowienie, szkoda, zmiana planu); szkodę zgłasza rocznie ok. 5,3–5,6% ubezpieczonych domów (źródło wtórne) [E-DEM-09]. '
     'Luka obniżona z 3 do 1: rdzeń seedu B pokrywają konkurenci częściowi (calcbee „Insurance Deductible Optimizer”, InsuranceCalcs, COUNTRY Financial), a brakujące parametry (indywidualna dopłata po szkodzie, prawdopodobieństwo szkody) są niedostępne dla zewnętrznej strony. '
     'AI 2: pytania „zgłosić szkodę?” czy „podnieść udział własny?” asystent zwykle rozwiąże regułą kciuka. '
     'Dane są trudne i często zastrzeżone (Dane 2), a koszt eksperta wyższy niż w finansowaniu (agent, broker lub aktuariusz; Eksp 2). '
     'Zostają moduły: udział procentowy vs rezerwa w RENO-02 i INS-01 („zgłosić szkodę?”, status „później”).'),
    (16, {}, 'S',
     '1 wyszukiwanie agenta G6 (kalkulatory landed cost); bez audytu fali 2',
     'niska',
     'Popyt 4: fala co najmniej 9 kalkulatorów taryf z 2026 sugeruje wzrost zainteresowania, ale to sygnał podaży, nie pomiar popytu; liczby importerów nie zweryfikowano. '
     'Luka 3: obliczanie cła na dany dzień jest zatłoczone, ale dla decyzji „kupić na zapas przed zmianą, czekać, przenieść produkcję czy użyć FTZ” nie znaleziono bezpośredniego konkurenta w badanym zakresie (1 zapytanie, bez fraz o timingu; pewność niska). '
     'AI 3: wiedza asystentów o bieżących taryfach jest z natury nieaktualna, a nawet kalkulatory w wynikach przeczyły sobie co do Section 122. '
     'Ryzyko dezaktualizacji jest najwyższe w zestawie (Dane 1, Błąd 2, Eksp 2: walidacja przez brokera celnego), więc sens ma tylko symulator scenariuszy, w którym stawki wpisuje użytkownik.'),
    (27, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); oceny to hipotezy',
     'niska',
     'Popyt 3: rozwodów jest rocznie setki tysięcy (wiedza modelu, niezweryfikowane), a decyzja o domu dotyczy tylko par z nieruchomością. '
     'Luka 3: profesjonalne oprogramowanie dla CDFA jest płatne i przeznaczone dla specjalistów (substytut), a kalkulatory wykupu są częściowe; o konkurencji konsumenckiej nie da się nic powiedzieć, bo nie wykonano żadnego zapytania. '
     'AI 3: wrażliwość tematu może skłaniać asystentów do odsyłania do prawnika, a nie do narzędzia. '
     'Ryzyko błędu jest najwyższe w zestawie (Błąd 1: granica porady prawnej, prawo stanowe, QDRO), a przegląd CDFA lub prawnika rodzinnego konieczny (Eksp 2); w grę wchodzi najwyżej jeden produkt (dom: zatrzymać, wykupić czy sprzedać).'),
    (20, {}, 'S',
     '1 wyszukiwanie agenta G6 (kalkulatory kosztu pracownika); bez audytu fali 2',
     'niska',
     'Popyt 3: temat jest popularny i obsadzony przez dostawców HR i payroll (co najmniej 5 kalkulatorów), co jest sygnałem podaży. '
     'Luka 2: Terms.Law, Toptal i inni liczą koszt pracownika i kontraktora (konkurencja częściowa, rynek zatłoczony); luka istnieje tylko po stronie pojemności i outsourcingu procesu. '
     'AI 2: reguła 1,25–1,4× pensji jest powszechnie znana, więc asystent nie musi odsyłać do narzędzia. '
     'Koszt danych i eksperta jest wysoki (limity payroll, SUTA, stanowe testy klasyfikacji; Dane 2, Eksp 2), dochodzi ryzyko błędnej klasyfikacji, a właściciel nie ma tu przewagi, więc werdykt brzmi: nie wchodzić.'),
    (8, {}, 'M',
     'agent G3 nie szukał danych dla tej rodziny (limit); brak późniejszych dowodów w rejestrze',
     'niska',
     'Popyt 3 to hipoteza: rosnące rachunki zwiększają zainteresowanie zmianą planu, ale jako samodzielne pytanie popyt jest umiarkowany i silnie lokalny. '
     'Luka 2: narzędzia porównania planów samych utility, działające na danych interwałowych klienta, oraz Power to Choose w Teksasie mają przewagę strukturalną. '
     'AI 2: asystent nie zna danych zużycia użytkownika i najpewniej odeśle do utility. '
     'Koszt danych jest najwyższy (Dane 1: tysiące taryf, często w PDF-ach, częste zmiany), co przeczy celowi automatyzacji; dlatego to warstwa danych dla innych symulatorów (Wsp 5), a nie rodzina produktów.'),
    (35, {}, 'M',
     'agent G7 nie szukał danych dla tej rodziny (limit); oceny to hipotezy',
     'średnia co do monetyzacji; niska co do konkurencji',
     'Problem jest realny przy podwyżce lub zmianie pracy, ale liczba osób, których dotyczy, to nie popyt na narzędzie (Pop 3, hipoteza). '
     'Luka 2: narzędzia typu CLIFF (Atlanta Fed) oraz stanowe i pozarządowe kalkulatory świadczeń to konkurencja bezpośrednia lub częściowa (wiedza modelu, nie badano). '
     'Monetyzacja reklamowa jest bardzo słaba (Kom 1, Rekl 1), a koszt danych i ryzyko błędu skrajne (dziesiątki programów razy 50 stanów; błąd może skłonić do odrzucenia podwyżki). '
     'Werdykt: odrzucić dla modelu AdSense i automatyzacji.'),
]


def load_families():
    fams = []
    for g in range(1, 8):
        d = json.load(open(f'{RAW}/family_G{g}.json'))
        for f in d['families']:
            fams.append((g, f))
    return fams


def parse_table(md):
    """Wiersze tabeli §4: nazwa, 10 ocen (str), średnia, werdykt."""
    sec = md.split('## 4. ETAP B')[1].split('Średnia jest nieważona')[0]
    sec = sec.split('| Rodzina | Źr. |')[1]
    rows = []
    for line in sec.splitlines():
        if not line.startswith('| ') or line.startswith('| Rodzina') or line.startswith('|---'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 14:
            continue
        rows.append((cells[0], cells[2:12], cells[12], cells[13], cells[1]))
    return rows


def short_verdict(v):
    v = re.sub(r'\*\*', '', v)
    v = re.sub(r'\s*\((?!poza domeną wariantu B\))[^()]*\)', '', v)
    return re.split(r' — |;', v)[0].strip()


def fmt_scores(scores, adj):
    out = []
    for k, lab in zip(KEYS, LABELS):
        if k in adj:
            out.append(f'{lab} {scores[k]}→{adj[k]}')
        else:
            out.append(f'{lab} {scores[k]}')
    return ' · '.join(out)


def main():
    md = open(MARKET, encoding='utf-8').read()
    table = parse_table(md)
    fams = load_families()
    assert len(fams) == 35, len(fams)
    assert len(table) == 35, len(table)
    assert len(CARDS) == 35
    assert sorted(c[0] for c in CARDS) == list(range(1, 36))

    lines = []
    counts = {'S': 0, 'R': 0, 'M': 0}
    for i, (card, row) in enumerate(zip(CARDS, table), start=1):
        idx, adj, code, basis, conf, text = card
        g, fam = fams[idx - 1]
        sc = fam['scores']
        # zgodność z tabelą §4
        expect = []
        for k in KEYS:
            expect.append(f'{sc[k]}→{adj[k]}' if k in adj else str(sc[k]))
        if expect != row[1]:
            raise SystemExit(f'Niezgodne oceny w wierszu {i} ({row[0]}): JSON {expect} vs tabela {row[1]}')
        vals = [adj.get(k, sc[k]) for k in KEYS]
        avg = sum(vals) / 10
        avg_s = f'{avg:.1f}'.replace('.', ',')
        if avg_s != row[2]:
            raise SystemExit(f'Średnia {avg_s} ≠ {row[2]} w wierszu {i}')
        nsent = len(re.findall(r'[.!?](?=\s+[A-ZĄĆĘŁŃÓŚŹŻ„]|\s*$)', text))
        if not 3 <= nsent <= 6:
            raise SystemExit(f'Karta {i}: {nsent} zdań')
        counts[code] += 1
        if code == 'M':
            basis = re.sub(r'^agent G\d[^;]*;\s*', '', basis)
        src = row[4]
        if src == 'G7':
            if g != 7:
                raise SystemExit(f'Wiersz {i}: Źr. G7, a JSON G{g}')
            label = 'G7, obszar nieoczywisty'
        else:
            nr, grp = [x.strip() for x in src.split('/')]
            if grp != f'G{g}':
                raise SystemExit(f'Wiersz {i}: Źr. {src}, a JSON G{g}')
            label = f'rodzina z briefu nr {nr}, {grp}'
        lines.append(f'**{i}. {row[0]}** ({label}) — {fmt_scores(sc, adj)} · śr. {avg_s} · werdykt: {short_verdict(row[3])}  ')
        lines.append(f'*Podstawa:* {BASIS[code]}; {basis}. *Pewność:* {conf}.  ')
        lines.append(text)
        lines.append('')

    intro = [
        '### 4.1. Karty rodzin (uzasadnienia ocen)',
        '',
        'Karty streszczają uzasadnienia agentów rodzin i dodają późniejsze dowody z rejestru (fala uzupełniająca, audyt fali 2). Pełne teksty są w `data/agent-outputs/family_G1.json` … `family_G7.json`: dziesięć pól uzasadnień, po jednym na wymiar oceny (`demand_pl`, `commercial_pl`, `integrated_competition_pl`, `ai_fit_pl`, `shared_modeling_pl`, `data_cost_pl`, `error_risk_pl`, `catalog_potential_pl`, `ad_fit_pl`, `expert_cost_pl`), oraz werdykt agenta (`verdict_pl`). Karta streszcza tylko wymiary decydujące o werdykcie; uzasadnienia pozostałych wymiarów są w tych polach JSON. Karty nie dodają nowych ocen; korekty oznaczone „→” pochodzą z tabeli powyżej. Kolejność jak w tabeli, a nagłówek karty podaje źródło wiersza (rodzina z briefu albo obszar nieoczywisty G7).',
        '',
        'Uzasadnienia oceny „AI” (co asystent policzy sam, kiedy odeśle do narzędzia) to oceny agentów rodzin, a nie wyniki testów asystentów; traktujemy je jako hipotezy do sprawdzenia w panelu asystentów (krok 5 bramki G0).',
        '',
        f'**Na czym opierają się oceny.** Agenci 7 grup rodzin wykonali łącznie {sum(QUERIES.values())} udanych wyszukiwań na 35 rodzin (od 0 do 5 na agenta; agenci G2 i G5 — zero), bo wspólny limit 200 wyszukiwań na turę wyczerpał się wcześniej. '
        f'W efekcie {counts["S"]} rodzin ma oceny oparte na wyszukiwaniach agenta rodziny (search-summary, zwykle 1–4 zapytania), {counts["R"]} — na wyszukiwaniach dotyczących wyłącznie zmian ulg, a {counts["M"]} — na wiedzy modelu (brak wyszukiwań z powodu limitu). '
        'Część rodzin ma późniejsze dowody: dane o skali zdarzeń z fali uzupełniającej (25 zapytań, wpisy E-DEM; transakcje, sztuki i zasoby, a nie popyt online) i konkurencję z audytu 25 produktów (fala 2). '
        'Podaż treści i kalkulatorów to sygnał pośredni, a nie pomiar popytu; bezpośrednich dowodów popytu online (wolumenów) w tej sesji nie zebrano, więc kryterium „popyt” ma pewność niską.',
        '',
        '**Formuła konkurencji.** „Nie znaleziono bezpośredniego konkurenta w badanym zakresie” oznacza w kartach: audyt fali 2 — 7 zapytań WebSearch na produkt, u finalistów dodatkowo 8 zapytań próby obalenia (fala 2b); anglojęzyczny web USA; 2026-10-25; wyłącznie streszczenia wyszukiwarki, strony nieotwierane; pewność niska–średnia. Przy ocenach agentów rodzin zakres podano w karcie. Kategorie: bezpośredni / częściowy / substytut / sporny.',
        '',
    ]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(intro + lines).rstrip() + '\n')
    print('OK', counts, 'queries', sum(QUERIES.values()))


if __name__ == '__main__':
    main()
