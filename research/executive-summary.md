# Streszczenie wykonawcze — serwis symulatorów decyzji (USA)

Data: 2026-10-25 · Badanie wieloagentowe (74 agentów w falach 1–2b, recenzja adwersaryjna w fali 3) · Odwołania `E-…`, `Z-…`, `K-…` → `evidence-and-assumptions.md` · Liczby ekonomiczne → `economics.csv`

## 1. Werdykt

**Werdykt: budować warunkowo — wyłącznie jako ograniczony test opcji. W zakładanej formie (setki symulatorów, AdSense jako podstawa przychodu, ruch liczony na asystentach AI): nie budować.**

- **Test opcji:** jeden symulator **RENO-02** na minimalnym silniku osi czasu, na nowej domenie wariantu B.
- **Limit testu:** gotówka do ok. **9 tys. USD** i czas właściciela do ok. **300 h** na G0 i budowę, bez utrzymania po publikacji. Do publikacji RENO-02 (ok. 4. miesiąc) potrzeba bazowo ok. **5,9 tys. USD** i **215 h** budowy (+15–25 h G0); do decyzji 6-miesięcznej gotówka dochodzi do ok. 8 tys. USD. Konserwatywnie ok. **13 tys. USD** i **290 h** (z G0 ok. 305–315 h): oba limity są przekroczone przed publikacją, więc test zostaje przerwany (§8 pkt 4), chyba że właściciel jawnie obetnie koszty. Optymistycznie ok. 3,0 tys. USD i 140 h. Gotówka obejmuje prawo/CMP, eksperta dla RENO-02 (20–30 h) i koszty stałe za okres budowy.
- **Start testu wyłącznie po zaliczeniu mierzalnej bramki G0** (§6).
- **Pewność:** średnia dla „nie budować wersji szerokiej w modelu AdSense-first”; niska dla „test wąskiej wersji ma dodatnią wartość oczekiwaną” (brak danych o popycie w Google, brak testów asystentów, strony konkurentów nieotwierane).
- **Dlaczego nie „budować”:** w ilustracji 36-miesięcznej pełnej budowy (harmonogram ograniczony czasem właściciela) scenariusz bazowy kończy się skumulowaną stratą gotówkową ok. **−97 tys. USD** (z wyceną czasu właściciela ok. **−156 tys. USD**) bez zwrotu, a konserwatywny stratą ok. −86 tys. USD. Tylko optymistyczny zwraca gotówkę (ok. mies. 29), a z wyceną czasu właściciela nie zwraca się w 36 mies. Pełna budowa byłaby więc zakładem na scenariusz optymistyczny albo na zmianę modelu monetyzacji.
- **Dlaczego nie „nie budować” bez zastrzeżeń:** koszt testu opcji jest ograniczony z góry, a kluczowe niewiadome (§4b) da się zmierzyć tanio dopiero w G0 i w teście.

**Pozycjonowanie:** „Neutralne symulatory dużych decyzji kapitałowych gospodarstwa domowego w USA — dom, jego systemy, ubezpieczenie, kapitał w domu i auto — które w jednym rachunku łączą zależności pomijane przez pojedyncze kalkulatory i typowe odpowiedzi asystentów (ubezpieczenie, finansowanie, termin sprzedaży, podatki) i pokazują, przy jakich założeniach wynik się odwraca.” To, że typowe odpowiedzi asystentów pomijają te zależności, jest hipotezą (Z-12) do sprawdzenia w panelu asystentów (G0, krok 5); funkcje kalkulatorów konkurencji znamy tylko ze streszczeń wyszukiwarki.

**Domena:** wariant B — jedna domena, kategorie w podkatalogach, możliwe późniejsze wydzielenie 301. Osobna domena tylko przy spełnieniu warunków (1 lub 2) oraz 3 oraz 4: inna publiczność lub monetyzacja; inny profil ryzyka; zwalidowany popyt; potencjał marki (`architecture-and-validation.md` §1.2).

## 2. Najważniejsze dowody

1. **Ruch z asystentów AI jest mały i skoncentrowany:** 0,1–1% ruchu witryn (Conductor: 1,08%, 10 branż, USA, V–IX 2025, próba z bazy klientów Conductor) [E-AI-02, E-VER-C5]. ChatGPT daje 63–95% referencji AI zależnie od trackera (BrightEdge VIII 2026: 95,1%; SE Ranking 2026: 74,78%); Perplexity 1–7%, Copilot 1–3,5% (jedyny pomiar: SE Ranking 3,51%), Claude 0,8–2,6% [E-AI-03, E-REV-01]. Link zewnętrzny ma tylko 6,8% odpowiedzi ChatGPT (USA, desktop, V 2026) [E-VER-C3].
2. **ChatGPT i Google AI Mode same generują kalkulatory:** OpenAI „Intelligent UI” od 7–8.10.2026 (wg OpenAI jeszcze niedopracowane) [E-VER-C2]; Google według relacji SEJ — w AI Mode globalnie po angielsku od 19.08.2026, wdrażane w AIO [E-VER-C1]. To funkcje, nie skala użycia; dla Perplexity, Copilota i Claude nie weryfikowano.
3. **Google oddaje mniej kliknięć:** przy AI Overviews CTR jest niższy o 35–61% (korelacje Ahrefs i Seer; Pew: 8% vs 15% kliknięć; Seer: częściowe odbicie w 2026) [E-AI-06..08]. W eksperymencie randomizowanym (wersja robocza; n ≈ 1 100, USA, próba niereprezentatywna; 7 dni wymuszonego trybu AI Mode) kliknięcia w linki zewnętrzne spadły o 18,8 pp [E-VER-C6, E-AI-09]. Zapytania 7+ słów wywołują AIO w ok. 46–55% przypadków, jednowyrazowe w ok. 10% [E-AI-11, E-REV-02].
4. **Monetyzacja:** AdSense płaci za wyświetlenia, a głębokie narzędzia zarabiają zwykle poza display (źródła w §4a pkt 2–3). Display działa u Omni Calculator (~3,7–3,8 tys. kalkulatorów, ok. 14–16,5 mln wizyt/mies. wg Semrush; nieaudytowane) [E-POR-02, E-REV-04].
5. **Konkurencja.** W 24 z 25 audytów nie znaleziono bezpośredniego konkurenta w badanym zakresie (7 zapytań WebSearch na produkt, u 10 finalistów +8 zapytań próby obalenia; anglojęzyczny web USA; 2026-10-25; wyłącznie streszczenia wyszukiwarki, strony nieotwierane; pewność niska–średnia); wyjątek RET-03 (konkurenci bezpośredni RothHelper i QuantCalc ACA Bridge Optimizer; pewność średnia). Fragmenty decyzji wszędzie pokrywają konkurenci częściowi i substytuty. Seedy: B — konkurenci częściowi; F/ENER-03 — Home Energy Planner sporny; H — BiggerPockets Sell vs Keep bezpośredni dla rdzenia hold/sell (pewność średnia), OverlineIQ sporny.
6. **Popyt: tylko dane pośrednie.** Hipoteza: decyzje przesuwają się w stronę „zostać i remontować” (mediana posiadania domu 12 lat; sprzedaż istniejących domów 4,06 mln, najmniej od 1995) [E-DEM-04, E-DEM-05]. Skala zdarzeń, nie popyt online: 7,75 mln sztuk dostaw AC i pomp ciepła w 2025 (w tym nowe budownictwo) [E-DEM-08]; 29,6% aut oddanych w rozliczeniu przy zakupie nowego miało ujemny kapitał (Edmunds Q2 2026) [E-REV-07]; 29,1% za Q3 2026 to jedno niepotwierdzone źródło [E-DEM-14]. PV domowe słabnie po wygaśnięciu 25D [E-DEM-10], a generatory standby wróciły w Q2 2026 do wzrostu [E-DEM-12, E-REV-03].
7. **Utrzymanie ma granice:** w 12 mies. zmieniły się 25D [E-REG-01], NFIP (wygasał co najmniej dwukrotnie; autoryzowany do 11.12.2026) [E-REG3-06, E-REV-05], zniżki FORTIFIED [E-REG3-08], ACA PTC [E-REG2-13] i RAP [E-REG2-07]; wiele parametrów nie ma stabilnych API (Z-14), a finanse to YMYL [E-ADS-08].

## 3. Główne ryzyka (od największego)

1. **Kanał AI nie dostarczy wolumenu:** bazowo z ok. 171 tys. sesji zarejestrowanych potrzebnych na 1000 USD/mies. tylko ok. 1,6 tys. pochodzi z asystentów (ok. 156 tys. to sesje ludzi z wyszukiwarek i innych źródeł, ok. 14 tys. boty). Kanał zależy od jednej firmy (ChatGPT daje 63–95% referencji AI; −52% referencji z ChatGPT w VII–VIII 2025, przyczyna wg Profound: zmiana wag cytowań, niepotwierdzona) [E-AI-04], a pomiar jest zawodny (utrata UTM w X 2026) [E-VER-C12].
2. **Substytucja przez generatywne UI (hipoteza):** interaktywność prawdopodobnie przestaje być przewagą; jakości i skali użycia nie testowano (Z-12).
3. **Niski przychód na sesję:** bazowo ok. 5,9 USD na 1000 sesji zarejestrowanych (6,4 USD na 1000 sesji ludzi); zwrot nowego narzędzia wymaga ok. 39 tys. sesji ludzi/mies. (§5).
4. **Ryzyko algorytmiczne i polityk:** scaled content abuse [E-ADS-06], sygnały obejmujące całą witrynę [E-POR2-08], odrzucenie AdSense za „low value content” [E-ADS-09]; jedno konto reklamowe to jeden punkt awarii [E-ADS-05].
5. **Koszt eksperta:** 17–27 h na nowy symulator i 3–12 h rocznie na utrzymanie (Z-16); pięć pilotów to 86–135 h (szacunki agentów fali 2b).
6. **Konflikt celów:** widoczność w ChatGPT, AI Mode i AIO koreluje ze wzmiankami poza witryną (dane dostawców, pewność niska; dla Claude i Copilota brak danych) [E-POR2-12], a model nie przewiduje budowy marki poza witryną.
7. **Błędny odczyt wczesnych danych:** 30 dni bez ruchu nie dowodzi braku rynku. Model zakłada RPM w styczniu ok. 75%, a w grudniu ok. 136% średniej rocznej (założenie Z-07; raporty branżowe: spadek styczniowy 35–75% [E-ADS-20]), więc progi porównujemy po korekcie sezonowej.

## 4. Rekomendacja zakresu

Pięć produktów pilotażowych w kolejności budowy (nazwy robocze z `product-opportunities.csv`; karty: `top-10-products.md`):

1. **RENO-02 Aging Roof: Replace, Repair, Fortify or Wait** — najwyższa ocena po kalibracji (3,75); wynik zależy od polisy (ACV/RCV, udział własny wiatr/grad), horyzontu sprzedaży i PV. W badanym zakresie (§2 pkt 5: 7 + 8 zapytań, wyłącznie streszczenia wyszukiwarki, strony nieotwierane; pewność niska–średnia) nie znaleziono narzędzia, które łączy te zależności; najbliższe kalkulatory Roof ROI (Weathershield, CalculateMyRoof, ShinglesCalculator) trzeba ręcznie sprawdzić w G0 (krok 4). Test opcji nr 1 i warunek startu projektu; ekspert 20–30 h.
2. **RENO-03 AC or Furnace Just Died: Repair vs Like-for-Like vs Heat Pump vs Dual-Fuel** — pilna decyzja z 4–6 wariantami na tym samym silniku; dopiero po wyniku RENO-02; ekspert 16–27 h.
3. **HOME-04 Remodel vs. Move (Rate Lock-In Aware)** — pasuje do hipotezy „zostać i remontować”; pilot warunkowy (luka obniżona w kalibracji 3→2); ekspert 16–25 h.
4. **HOME-02 Sell vs. Rent Out When Moving (Exclusion Clock & Low-Rate Value)** — zegar wyłączenia §121 daje konkretny wynik (datę); pilot warunkowy; TrueHomeCosts, Bellhaven i TeamzLab mogą pokrywać część luki; ekspert 10–17 h (13–22 h z opcjami).
5. **AUTO-01 Underwater Car Loan Exit Planner (Keep, Trade Now, Wait, or Pay the Gap)** — test drugiej puli popytu (auta); pilot warunkowy; ekspert 24–36 h (nie jest tani).

Produkty 2–5 wymagają przed budową własnego pomiaru popytu i SERP (jak G0, kroki 2–3), ręcznej weryfikacji konkurencji (reguła ≥ 3 kluczowych zależności) i reguły dodawania narzędzi (§5: bazowo ok. 250 USD/mies. mediany przychodu, czyli ok. 39 tys. sesji ludzi/mies. na narzędzie; maks. 1 nowe narzędzie miesięcznie). „Pilot” w CSV to kandydat po bramkach, nie decyzja o budowie.

Długa lista: 96 wierszy, 92 odrębne pomysły (RENO-01, INS-06, CARE-07 i BIZ-06 to gałęzie, moduły lub warianty innych); statusy odrębnych: pilot 5, zbadać 27, później 35, odrzucić 25. Ranking: 25 audytowanych pozycji, 24 odrębne propozycje (RENO-01 to gałąź RENO-02); następny kandydat do audytu: AUTO-04.

**Poza zakresem domeny:** samodzielne planery podatku dochodowego (moduły podatkowe w decyzjach, np. §121 w HOME-02, są w zakresie, z przeglądem CPA/EA); zdrowie (ewentualnie test na healthscorer.com); emerytura, opieka i starzenie, praca/relokacja/benefity, finansowanie studiów; mała firma i e-commerce — ewentualny test w istniejącym serwisie e-commerce właściciela, osobna domena dopiero po spełnieniu warunków 3 i 4.

## 4a. Trzy obalone założenia

Dowody obalają albo silnie podważają te założenia wyjściowe (analiza źródeł wtórnych, nie własne testy):

1. **„Asystenci AI dadzą istotny ruch”.** Ruch z AI to 0,1–1% ruchu witryn [E-AI-02, E-VER-C5]; Omni Calculator dostaje z ChatGPT, Claude i Gemini ok. 0,04–0,05% ruchu (ok. 6 tys. wizyt/mies., szacunek Semrush) [E-AI-14, E-VER-C4]; link zewnętrzny ma 6,8% odpowiedzi ChatGPT [E-VER-C3]; ChatGPT i Google AI Mode same generują kalkulatory [E-VER-C1, E-VER-C2].
2. **„Dłuższa praca z symulatorem daje więcej przychodu z AdSense”.** AdSense rozlicza wyświetlenia i zabrania odświeżania reklam bez działania użytkownika oraz reklam obok elementów interaktywnych [E-VER-C7, E-ADS-03]. Benchmarków odsłon na sesję dla stron-narzędzi nie znaleziono; przy założonych 1,1–1,6 odsłony na sesję (Z-02, analogia do landing pages [E-ADS-26]) dłuższa sesja nie daje więcej wyświetleń.
3. **„Głębokie narzędzia utrzymają się z display, a setki narzędzi dadzą proporcjonalnie więcej ruchu”.** Głębokie narzędzia żyją z subskrypcji (ProjectionLab: deklarowane ~1 mln USD ARR, VI 2025; Boldin, DealCheck), osadzania u firm (Rewiring America) albo z partnerów i leadów (NerdWallet wg 10-K FY2025; SmartAsset wg deklaracji z 2021) [E-POR2-02..07]. Ruch rozkłada się nierówno (w modelu: rozkład potęgowy); nowe narzędzie musi mieć ok. 39 tys. sesji ludzi/mies., by zwrócić koszt w 24 mies. (baza), a najlepsze w ilustracji ma ok. 15 tys. sesji po 12 mies. Masowe strony grożą kwalifikacją jako scaled content abuse [E-ADS-06].

## 4b. Trzy największe niewiadome

1. **Popyt w Google na decyzje RENO-02** (wolumeny, skład SERP z AIO/AI Mode). Z AI przychodzi w bazie 1% sesji ludzi, więc ruch musi dać Google; bezpośrednich dowodów popytu online brak. Pomiar: G0 kroki 2–3 (K-04, K-05).
2. **Realny page RPM i odsłony na sesję stron-narzędzi z formularzem.** Rozrzut tych założeń zmienia ruch potrzebny na 1000 USD/mies. z ok. 48 tys. do ok. 980 tys. sesji zarejestrowanych. Pomiar: G0 krok 1b kierunkowo, potem test RENO-02 od 2 000 odsłon (Z-01, Z-02, K-06).
3. **Czy asystenci linkują do zewnętrznych narzędzi, czy generują je sami** — od tego zależy, czy kanał AI to dodatek, czy substytut. Pomiar: G0 krok 5 (Z-11, Z-12, K-02).

## 5. Ekonomika bez fałszywej precyzji

Wszystkie wartości to założenia (`economics.csv`; Z-09, Z-15, Z-16): przychodowe oparte na niezweryfikowanych zakresach vendorskich, kosztowe i czasowe to szacunki własne. Trajektoria to ilustracja, nie prognoza. „Sesje zarejestrowane” obejmują boty (progi ruchu w tabeli); „sesje ludzi” są po filtrze botów (progi decyzyjne).

| Wskaźnik | Kons. | Baz. | Opt. |
|---|---|---|---|
| Przychód na 1000 sesji zarejestrowanych, średnia roczna (na 1000 sesji ludzi) | 1,0 USD (1,2) | 5,9 USD (6,4) | 21 USD (21,6) |
| Sesje zarejestrowane/mies. dla 1 / 3 / 10 tys. USD | 980 tys. / 2,9 mln / 9,8 mln | 171 tys. / 513 tys. / 1,71 mln | 48 tys. / 143 tys. / 477 tys. |
| Koszty stałe/mies. z utrzymaniem eksperckim: 5 / 15 / 25 narzędzi (USD) | 1 710 / 4 210 / 6 710 | 640 / 1 510 / 2 390 | 290 / 600 / 910 |
| Próg rentowności gotówkowej (sesje zarejestrowane/mies.): 5 / 15 narzędzi | 1,68 mln / 4,12 mln | 109 tys. / 259 tys. | 14 tys. / 29 tys. |
| Próg, 5 narzędzi: z amortyzacją uruchomienia w 24 mies. / z wyceną czasu właściciela | 3,14 mln / 2,51 mln | 254 tys. / 191 tys. | 36 tys. / 27 tys. |
| Zysk operacyjny gotówkowy, 25 narzędzi, przy przychodzie 1 / 3 tys. USD (USD/mies.) | −5 710 / −3 710 | −1 390 / +610 | +90 / +2 090 |
| To samo przy 1 tys. USD, po wycenie czasu właściciela | −7 560 | −2 510 | −540 |
| Test opcji (silnik + RENO-02): gotówka do publikacji / czas / miesiąc publikacji; koszty stałe potem | ok. 13 tys. USD / 290 h / mies. 8; 710 USD/mies. | 5,9 tys. USD / 215 h / mies. 4; 290 USD/mies. | 3,0 tys. USD / 140 h / mies. 2; 160 USD/mies. |
| Silnik + 5 symulatorów: gotówka (prawo/CMP + eksperci) / czas | 36 tys. USD / 502 h | 20,4 tys. USD / 395 h | 11,2 tys. USD / 288 h |
| Nowe narzędzie: ekspert / czas właściciela | 27 h, 6 750 USD / 53 h | 22 h, 3 850 USD / 45 h | 17 h, 2 125 USD / 37 h |
| Sesje zarejestrowane/mies. na narzędzie do zwrotu jego gotówki w 24 mies. | 520 tys. | 42 tys. | 5,7 tys. |
| Reguła dodawania (koszt narzędzia / 24 + utrzymanie): mediana przychodu / sesje ludzi na narzędzie (mies.) | ok. 530 USD / 442 tys. | ok. 250 USD / 39 tys. | ok. 120 USD / 5,5 tys. |
| Mies. 24: narzędzia / przychód / wynik gotówkowy (USD/mies.) | 5 / 3 / −1 710 | 15 / 220 / −1 290 | 30 / 4 940 / +3 870 |
| Skumulowany wynik gotówkowy po 36 mies. (z wyceną czasu) | −86 tys. USD (−139 tys.) | −97 tys. USD (−156 tys.) | +27 tys. USD (−31 tys.) |
| Maks. zaangażowanie gotówki | 86 tys. USD | 97 tys. USD | 44 tys. USD |
| Miesiąc zwrotu: gotówka / z wyceną czasu | brak / brak | brak / brak | 29 / brak |

Czas budowy liczono przy 40 / 60 / 80 h/mies. właściciela (w §6: ok. 15 h/tydz.). Ilustracja startuje w listopadzie i zakłada 5 / 15 / 30 narzędzi; konserwatywna (tylko 5 narzędzi) traci więc mniej niż bazowa. W bazie najlepsze narzędzie ma ok. 15 tys. sesji po 12 mies., więc reguła dodawania w praktyce blokuje rozbudowę — zgodnie z werdyktem.

- **Założenia kluczowe:** page RPM USA 2,4 / 8 / 18 USD (brak danych pierwotnych dla stron-narzędzi; 2,4 USD to pojedyncza mediana z jednego benchmarku, 75 stawek, nieprzypisana do URL, o nieznanym typie RPM, kraju i niszy — pewność niska [E-ADS-11]); odsłony na sesję 1,1 / 1,3 / 1,6 (Z-02); udział AI w sesjach ludzi 0,3% / 1% / 5% (benchmarki 0,1–1%; 5% to hipoteza); obserwacja właściciela 10–30% tylko jako wrażliwość. Przy page RPM 2,4 USD wszędzie: 1,0 / 1,8 / 2,8 USD na 1000 sesji zarejestrowanych. CPC Search nie przeliczamy na przychód serwisu [E-ADS-15].
- **Omni Calculator:** ok. 15–30 USD na 1000 wizyt (szacunek na szacunkach: ok. 4,2 mln USD/rok wg Growjo – poniżej 5 mln wg ZoomInfo, nieaudytowane; szacunek do 6 mln/rok pominięto jako niezweryfikowany; / 14–23 mln wizyt/mies.) [E-POR-02, E-POR2-05]; ruch globalny, dojrzała marka. Rozbieżność z bazą (ok. 2,5–5×) to argument za pomiarem w G0 (krok 1b), nie za podnoszeniem bazy.
- **Dodatek poza bazą (hipoteza):** lead-gen/afiliacja przy niezweryfikowanej konwersji 0,2–1% sesji ludzi i wypłacie 10–50 USD daje 20–500 USD na 1000 sesji ludzi, a próg rentowności 5 narzędzi ok. 95 tys. / 5,3 tys. / 0,6 tys. sesji zarejestrowanych. To ilustracja z własnych założeń, poza werdyktem, bramkami i regułą dodawania; wymaga zgód TCPA (leady ubezpieczeniowe — osobnej opinii prawnej).

## 5a. Strategie alternatywne

| Strategia | Koszt testu | Czas do sygnału | Przychód (jednostka) | Zgodność z ograniczeniem właściciela |
|---|---|---|---|---|
| Test na healthscorer.com (HLTH-02 lub symulator zdrowotny) | ~0 USD + 30–60 h | 1–3 mies. | AdSense na istniejącym koncie i ruchu | pełna (AdSense), ale inna tematyka i YMYL zdrowotny |
| B2B embed / white-label RENO-02, RENO-03 (dekarze, HVAC, agenci ubezpieczeniowi, credit unions; model Rewiring America [E-POR2-04]) | rozmowy z 5 firmami: 5–10 h | 2–6 tyg. | abonament na klienta (hipoteza: 50–100 USD/mies.; niezweryfikowane) | niezgodne z „AdSense jako baza” — osobna decyzja |
| Lead-gen/afiliacja jako dodatek | integracja + zgody TCPA | 3–6 mies. | 20–500 USD/1000 sesji ludzi (hipoteza z własnych założeń) | tylko dodatek; nie ratuje modelu w analizie podstawowej |
| Płatny test ruchu (Google Ads 300–500 USD) na MVP RENO-02 | 300–500 USD + MVP | 2 tyg. | pomiar ukończenia i CTR (RPM w tym budżecie niemierzalny) | zgodne jako pomiar, wymaga zgody właściciela |
| Subskrypcja / raport płatny (model ProjectionLab: deklarowane ~1 mln USD ARR, VI 2025 [E-POR2-02]) | landing + waitlista | 1–2 mies. | przedpłaty / zapisy | niezgodne z bazą; osobna decyzja |

## 6. Pierwszy eksperyment: bramka G0 (dni 0–14; ok. 0 USD; ok. 15–25 h właściciela)

- **1a. Kanał AI (kierunkowo, inna domena; K-01):** GA4 i logi healthscorer.com za 90 dni: sesje ludzi od asystentów, osobno dla każdej platformy, po odfiltrowaniu botów (`ChatGPT-User`, `OAI-SearchBot`, `Claude-User` itd.); Bing „AI Performance”.
- **1b. Kalibracja monetyzacji (kierunkowo; K-06):** page RPM (USA i ogółem), odsłony na sesję i udział odsłon z reklamą na stronach z formularzem w healthscorer.com (Z-01…Z-05).
- **2. Popyt w Google dla RENO-02 (K-04):** Keyword Planner (bez kampanii) i Google Trends dla 10–20 fraz w 3–5 klastrach (np. wiek dachu a ubezpieczenie, ACV vs RCV) oraz 12-miesięczny profil sezonowy. **Próg (propozycja decyzyjna, nie norma rynkowa): łącznie ≥ 10 tys. wyszukiwań/mies. w USA dla mierzonych fraz.** Wyprowadzenie (założenia własne): z długim ogonem klaster ma ok. 2× wolumenu mierzonych fraz, a przechwycenie po dojrzeniu 10–15% ruchu klastra daje ok. 2–3 tys. sesji ludzi/mies., czyli okolice progu „Kontynuować”. Warunek konieczny, nie wystarczający.
- **3. SERP i AI w Google (K-05):** dla 10 fraz: czy AIO/AI Mode generuje własny kalkulator lub tabelę wariantów; ile wyników top 10 to fora lub małe domeny. **Próg (propozycja): dla ≥ 3 fraz w top 10 są ≥ 2 wyniki z forów lub małych domen, a AI Mode/AIO nie generuje pełnego porównania wariantów w więcej niż połowie fraz.**
- **4. Ręczna weryfikacja konkurencji RENO-02 (K-03):** otworzyć strony wszystkich kandydatów z „Listy do ręcznej weryfikacji (G0 krok 4)” w karcie RENO-02 (`top-10-products.md`; m.in. kalkulatory Roof ROI, InsuranceCostCity, RoofingCalculatorUSA, Paperform Roof Replacement Financing Calculator, RoofTap) i przetestować formularze. **Produkt odpada, jeśli jedno narzędzie pokrywa ≥ 3 kluczowe zależności** (ACV/RCV lub harmonogram wypłat za dach; udział własny wiatr/grad; horyzont sprzedaży; demontaż i ponowny montaż PV; finansowanie).
- **5. Panel asystentów (pomiar bazowy, nie warunek; K-02):** 5 produktów × (2 prompty bez prośby o narzędzie + 2 z prośbą o kalkulator) × 5 asystentów × 2 powtórzenia = 200 uruchomień (ok. 10–15 h); odsetek linków osobno dla obu kategorii promptów i dla każdej platformy. Pule promptów pozostałych finalistów — dopiero przed decyzją o ich budowie.

**Reguła bramki:** test opcji budujemy tylko wtedy, gdy **jednocześnie spełnione są kroki 2, 3 i 4**. Kroki 1a, 1b i 5 tylko kalibrują oczekiwania: ≥ 1% sesji ludzi z AI i ≥ 2 tys. takich sesji/mies. w 1a oznacza, że kanał AI to realny dodatek (wskaźnik pośredni); page RPM USA < 2,4 USD w 1b oznacza, że liczymy dalej scenariusz konserwatywny. Deklaracja właściciela („akceptuję Google organic”) **nie jest** warunkiem bramki.

**Po bramce:** przy ok. 15 h/tydz. budowa (bazowo 215 h) trwa ok. 14 tygodni, więc **publikacja RENO-02 wypada ok. dnia 105–120** (przy 40 / 80 h/mies. ok. mies. 8 / 2). Zegar produktu liczymy od indeksacji w Google i Bing; **reguła awaryjna:** jeśli 60 dni po publikacji strony nadal nie ma w indeksie, liczymy od publikacji. Decyzja 90-dniowa wypada ok. mies. 7–8 od startu, 6-miesięczna ok. mies. 10–11; ruch i RPM porównujemy po korekcie sezonowej. **Kontynuować** (propozycja): po 90 dniach ≥ 500 wyświetleń GSC/mies., CTR ≥ 1,5%, ukończenie ≥ 35%; po 6 mies. ≥ 5 USD na 1000 sesji ludzi, ≥ 3 tys. sesji ludzi/mies. z trendem ≥ +15% m/m przez 3 mies. i spełniona reguła dodawania. Reszta reguł: `architecture-and-validation.md` §4.

**Najtańsza alternatywa (opcjonalna, za zgodą właściciela):** MVP RENO-02 bez pełnego silnika + 300–500 USD Google Ads przez 2 tygodnie mierzy ukończenie (`tool_completed`/`tool_started`) i CTR, ale nie RPM (odczyt wymaga ≥ 2 000 odsłon, czyli ok. 1,3–5,3 tys. USD płatnego ruchu, i zatwierdzonej witryny w AdSense); do tego rozmowy z 5 potencjalnymi klientami B2B.

## 7. Granice pewności

- **Strony nieotwierane:** WebFetch, curl i przeglądarka były zablokowane; funkcje konkurentów znamy ze streszczeń wyszukiwarki, a funkcje za loginem lub niewidoczne są „niezweryfikowane”, nie „brak” (K-03).
- **Brak danych SEO:** bez Keyword Plannera, Semrush, Ahrefs i Trends nie zebrano wolumenów; podaż treści to sygnał pośredni, nie pomiar popytu, więc kryterium „popyt” ma pewność niską (K-04, K-05). Liczby Semrush i Similarweb o ruchu domen pochodzą ze streszczeń wyników wyszukiwania (publiczne strony przeglądu domen); z samych narzędzi nie korzystano.
- **Brak testów asystentów:** wyników nie symulowano; jest plan testu (K-02). Reguł Google nie przenosimy na innych asystentów.
- **Limit wyszukiwań:** 200 wywołań na turę wspólnie dla agentów; w fali 1 agenci rodzin wykonali 0–5 udanych zapytań (łącznie 20 na 35 rodzin; agenci G2 i G5 żadnego), agenci pomysłów startowych 4–5 (łącznie 24); oceny rodzin mają pewność niską–średnią.
- **Monetyzacja i koszty:** page RPM i odsłony na sesję zmierzy kierunkowo G0 krok 1b, potem test RENO-02; politykę AdSense wobec stron-narzędzi trzeba potwierdzić (K-06); godziny ekspertów zweryfikują oferty (K-07).
- **Kanał AI właściciela:** obserwacja 10–30% ruchu z AI jest niezweryfikowana (K-01); utrata UTM zaniża atrybucję [E-VER-C12].

## 8. Warunek przerwania projektu

Przerwać projekt (nie tylko produkt), jeśli zajdzie którekolwiek z poniższych: (1) bramka G0 nie przechodzi — ręczna weryfikacja znajduje narzędzie pokrywające ≥ 3 kluczowe zależności RENO-02 albo pomiar popytu i SERP w Google nie spełnia progów; (2) 90 dni od indeksacji RENO-02 (albo od publikacji, jeśli 60 dni po publikacji strony nadal nie ma w indeksie): < 100 wyświetleń GSC/mies. i 0 cytowań w panelu asystentów oraz w Bing AI Performance; (3) 6 mies. od indeksacji RENO-02: zmierzony przychód < 2 USD na 1000 sesji ludzi albo < 1 tys. sesji ludzi/mies. bez wzrostu przez 3 kolejne miesiące (po korekcie sezonowej); (4) skumulowana strata gotówkowa przekracza ok. 9 tys. USD albo czas właściciela na G0 i budowę testu (silnik + RENO-02, bez utrzymania po publikacji) przekracza ok. 300 h, zanim spełnione zostaną kryteria kontynuacji. Progi to propozycje decyzyjne, nie normy rynkowe. Po przerwaniu ewentualną kontynuację rozważać tylko w innym modelu (B2B embed/white-label, lead-gen, subskrypcja), osobną decyzją.
