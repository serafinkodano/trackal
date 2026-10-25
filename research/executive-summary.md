# Streszczenie wykonawcze — serwis symulatorów decyzji (USA)

Data: 2026-10-25 · Badanie wieloagentowe (74 agentów w falach 1–2b, recenzja adwersaryjna w fali 3) · Odwołania `E-…`, `Z-…`, `K-…` → `evidence-and-assumptions.md` · Liczby ekonomiczne → `economics.csv`

## 1. Werdykt

**Werdykt: budować warunkowo — wyłącznie jako ograniczony test opcji. W zakładanej formie (setki symulatorów, AdSense jako podstawa przychodu, ruch liczony na asystentach AI): nie budować.**

- **Test opcji:** jeden symulator **RENO-02** na minimalnym silniku osi czasu, na nowej domenie wariantu B.
- **Limit testu:** gotówka do ok. **8 tys. USD** i czas właściciela do ok. **300 h** na G0 i budowę, bez utrzymania po publikacji (bazowo ok. 3,7 tys. USD i ok. 200 h budowy + 15–25 h G0; konserwatywnie 7,6 tys. USD i 273 h; optymistycznie 2,0 tys. USD i 127 h). Gotówka obejmuje prawo/CMP, eksperta dla RENO-02 i 3 miesiące kosztów stałych (`economics.csv`, sekcja launch).
- **Start testu wyłącznie po zaliczeniu mierzalnej bramki G0** (§6).
- **Pewność:** średnia dla „nie budować wersji szerokiej w modelu AdSense-first”; niska dla „test wąskiej wersji ma dodatnią wartość oczekiwaną” (brak danych o popycie w Google, brak testów asystentów, strony konkurentów nieotwierane).
- **Dlaczego nie „budować”:** w scenariuszu bazowym ilustracja 36-miesięczna kończy się skumulowaną stratą gotówkową ok. **−52 tys. USD** (z wyceną czasu właściciela ok. **−110 tys. USD**) i nie ma zwrotu w 36 mies. Zwrot pojawia się tylko w scenariuszu optymistycznym (gotówka: ok. mies. 21; z czasem właściciela: ok. mies. 34). Pełna budowa byłaby więc zakładem na scenariusz optymistyczny albo na zmianę modelu monetyzacji.
- **Dlaczego nie „nie budować” bez zastrzeżeń:** koszt testu opcji jest mały i ograniczony z góry, a kluczowe niewiadome (popyt w Google, realny page RPM stron-narzędzi, zachowanie asystentów) da się zmierzyć tanio dopiero w G0 i w teście.

**Pozycjonowanie:** „Neutralne symulatory dużych decyzji kapitałowych gospodarstwa domowego w USA — dom, jego systemy, ubezpieczenie, kapitał w domu i auto — które w jednym rachunku łączą zależności pomijane przez pojedyncze kalkulatory i typowe odpowiedzi asystentów (ubezpieczenie, finansowanie, termin sprzedaży, podatki) i pokazują, przy jakich założeniach wynik się odwraca.”

**Domena:** wariant B — jedna domena o spójnej funkcji decyzyjnej (dom, jego systemy, ubezpieczenie, kapitał w domu, auto), kategorie w podkatalogach, możliwe późniejsze wydzielenie 301; osobna domena tylko przy spełnieniu warunków (1 lub 2) oraz 3 oraz 4 (inna publiczność lub monetyzacja; inny profil ryzyka; zwalidowany popyt; potencjał marki — `architecture-and-validation.md` §1).

## 2. Najważniejsze dowody

1. **Ruch z asystentów AI jest mały i skoncentrowany:** 0,1–1% ruchu witryn (Conductor: 1,08%, 10 branż, USA, V–IX 2025, próba z bazy klientów Conductor) [E-AI-02, E-VER-C5]. ChatGPT daje 63–95% referencji AI zależnie od trackera (BrightEdge VIII 2026: 95,1%; SE Ranking 2026: 74,78%); Perplexity 1–7%, Copilot 1–3,5%, Claude 0,8–2,6% [E-AI-03, E-REV-01]. Link do zewnętrznego źródła ma tylko 6,8% odpowiedzi ChatGPT (USA, desktop, V 2026) [E-VER-C3], a Omni Calculator dostaje z ChatGPT, Claude i Gemini ok. 0,05% ruchu (szacunek Semrush) [E-VER-C4].
2. **Asystenci sami generują kalkulatory:** OpenAI udostępnia „Intelligent UI” od 7–8.10.2026 i zaznacza, że funkcja nie jest jeszcze dopracowana [E-VER-C2]; Google według relacji SEJ uruchomił generatywne narzędzia w AI Mode globalnie po angielsku 19.08.2026 i wdraża je w AIO (brak wpisu Google z VIII 2026) [E-VER-C1]. Źródła dokumentują funkcje, nie skalę ich użycia.
3. **Google oddaje mniej kliknięć:** przy AI Overviews CTR jest niższy o 35–61% (korelacje Ahrefs i Seer; Pew: 8% vs 15% kliknięć; Seer: częściowe odbicie w 2026) [E-AI-06..08]. W eksperymencie randomizowanym AI Mode obniżył kliknięcia zewnętrzne o 18,8 pp [E-VER-C6]. Zapytania 7+ słów wywołują AIO w ok. 46–55% przypadków, jednowyrazowe w ok. 10% [E-AI-11, E-REV-02].
4. **AdSense płaci za wyświetlenia** i zabrania odświeżania reklam bez działania użytkownika [E-VER-C7] oraz umieszczania reklam obok elementów interaktywnych [E-ADS-03]. Benchmarków odsłon na sesję dla stron-narzędzi nie znaleziono; przez analogię do landing pages (1–1,5) przyjęto założenie 1,1 / 1,3 / 1,6 (Z-02), do weryfikacji w GA4 [E-ADS-26].
5. **Głębokie narzędzia zarabiają zwykle poza display.** Tak działają ProjectionLab (subskrypcja; deklarowane ~1 mln USD ARR, VI 2025), Boldin i DealCheck (freemium) oraz Rewiring America (osadzany kalkulator dla firm) [E-POR2-02..04]; NerdWallet i SmartAsset raportują przychody głównie z partnerów i leadów [E-POR2-06/07]. Display działa u Omni Calculator (~3,7–3,8 tys. kalkulatorów, ok. 14–16,5 mln wizyt/mies. wg Semrush, starsze deklaracje 17–23 mln; zespół 33–70 osób; szacunki nieaudytowane) [E-POR-02, E-POR2-05, E-REV-04].
6. **Konkurencja.** W 24 z 25 audytów nie znaleziono bezpośredniego konkurenta w badanym zakresie (7 zapytań WebSearch na produkt, u 10 finalistów +8 zapytań próby obalenia; anglojęzyczny web USA; 2026-10-25; wyłącznie streszczenia wyszukiwarki, strony nieotwierane; pewność niska–średnia); wyjątek RET-03 (konkurenci bezpośredni RothHelper i QuantCalc ACA Bridge Optimizer; pewność średnia). We wszystkich audytach fragmenty decyzji pokrywają konkurenci częściowi i substytuty. Seedy: B — rdzeń pokrywają konkurenci częściowi (calcbee Insurance Deductible Optimizer i in.); F/ENER-03 — Home Energy Planner sporny (bezpośredni vs częściowy), do ręcznej weryfikacji; H — BiggerPockets Sell vs Keep bezpośredni dla rdzenia hold/sell (pewność średnia), OverlineIQ sporny (`competitor-audit.csv`).
7. **Popyt: tylko dane pośrednie.** Hipoteza: decyzje przesuwają się w stronę „zostać i remontować” (mediana posiadania domu 12 lat; sprzedaż istniejących domów 4,06 mln, najmniej od 1995) [E-DEM-04, E-DEM-05]. Skala zdarzeń, nie popyt online: 7,75 mln sztuk dostaw AC i pomp ciepła w 2025 (sztuki, w tym nowe budownictwo; nie gospodarstwa ani decyzje) [E-DEM-08]; 29,1% aut oddanych w rozliczeniu przy zakupie nowego miało ujemny kapitał (Edmunds Q3 2026 wg agenta; potwierdzono Q2 2026: 29,6%) [E-DEM-14, E-REV-07]. Domowe PV słabnie po wygaśnięciu 25D (Q2 2026: −12% r/r) [E-DEM-10]; w zasilaniu awaryjnym spadają generatory przenośne i magazyny, ale generatory standby wróciły w Q2 2026 do wzrostu [E-DEM-12, E-REV-03].
8. **Utrzymanie ma granice:** w 12 mies. zmieniły się 25D [E-REG-01], NFIP (wygasał co najmniej dwukrotnie; autoryzowany do 11.12.2026) [E-REG3-06, E-REV-05], zniżki FORTIFIED [E-REG3-08], ACA PTC [E-REG2-13] i RAP [E-REG2-07]; wiele parametrów nie ma stabilnych API (Z-14), a finanse to YMYL [E-ADS-08].

## 3. Główne ryzyka (od największego)

1. **Kanał AI nie dostarczy wolumenu:** bazowo z ok. 171 tys. sesji potrzebnych na 1000 USD/mies. tylko ok. 1,6 tys. pochodzi z asystentów. Kanał zależy od decyzji jednej firmy (−52% referencji z ChatGPT w VII–VIII 2025) [E-AI-04], a pomiar jest zawodny (utrata UTM w X 2026) [E-VER-C12].
2. **Substytucja przez generatywne UI (hipoteza):** interaktywność prawdopodobnie przestaje być przewagą; jakości i skali użycia nie testowano (Z-12).
3. **Niski przychód na sesję:** bazowo ok. 5,9 USD na 1000 sesji. Nowe narzędzie zwraca gotówkę budowy w 24 mies. przy ok. 22 tys. sesji/mies., a w ilustracji najlepsze narzędzie ma ok. 15 tys. po 12 mies.
4. **Ryzyko algorytmiczne i polityk:** grożą kwalifikacja jako scaled content abuse [E-ADS-06], sygnały obejmujące całą witrynę [E-POR2-08] i odrzucenie AdSense za „low value content” [E-ADS-09]; jedno konto reklamowe to jeden punkt awarii [E-ADS-05].
5. **Koszt eksperta:** nowy symulator wymaga 11–18 h eksperta (Z-16), czyli 1 375–4 500 USD, a każda kategoria YMYL dokłada roczne przeglądy.
6. **Konflikt celów:** widoczność w ChatGPT, AI Mode i AIO koreluje ze wzmiankami poza witryną (dane dostawców, pewność niska; dla Claude i Copilota brak danych) [E-POR2-12, E-AI-19], a model nie przewiduje budowy marki poza witryną.
7. **Błędny odczyt wczesnych danych:** 30 dni bez ruchu nie dowodzi braku rynku, a RPM w styczniu to ok. 75% średniej, w grudniu ok. 136%.

## 4. Rekomendacja zakresu

Pięć produktów pilotażowych w kolejności budowy (`top-10-products.md`, `architecture-and-validation.md` §3):

1. **RENO-02 Aging Roof: Replace, Repair, Fortify or Wait** — dlaczego: ma najwyższą ocenę po kalibracji (3,75), a wynik zależy od polisy (ACV/RCV, udział wiatr/grad), horyzontu sprzedaży i PV, czego nie łączy żadne znalezione narzędzie. Warunek: bramka G0; test opcji nr 1 i warunek startu całego projektu.
2. **RENO-03 AC or Furnace Just Died** — dlaczego: to pilna decyzja z 4–6 wariantami na tym samym silniku. Warunek: dopiero po wyniku RENO-02 i ręcznej weryfikacji konkurencji.
3. **HOME-04 Renovate vs Move (rate lock-in)** — dlaczego: pasuje do hipotezy „zostać i remontować” i liczy koszt utraty niskiej stopy. Warunek: pilot warunkowy (luka obniżona w kalibracji 3→2).
4. **HOME-02 Moving: Sell, Rent Out or Keep (§121 clock)** — dlaczego: zegar §121 daje konkretny, cytowalny wynik (datę). Warunek: pilot warunkowy; TrueHomeCosts, Bellhaven i TeamzLab mogą pokrywać część luki (fala 2b); przegląd CPA/EA.
5. **AUTO-01 Underwater Car Loan: Keep, Trade, Refinance or Sell** — dlaczego: testuje drugą pulę popytu (auta). Warunek: pilot warunkowy; ekspert 11–17 h (nie jest tani).

Produkty 2–5 wymagają własnej ręcznej weryfikacji konkurencji i reguły dodawania narzędzi (mediana miesięcznego przychodu narzędzi z ruchem ≥ gotówkowy koszt nowego narzędzia / 24, bazowo ok. 100 USD/mies.; maks. 1 nowe narzędzie miesięcznie do progu rentowności gotówkowej). „Pilot” w `product-opportunities.csv` to kandydat po bramkach, nie decyzja o budowie. Długa lista: 96 wierszy, 95 odrębnych pomysłów (pilot 5, zbadać 28, później 37, odrzucić 25); w rankingu 24 odrębne propozycje (RENO-01 to gałąź RENO-02).

**Poza zakresem domeny:** samodzielne planery podatku dochodowego (moduły podatkowe wbudowane w decyzje, np. §121 w HOME-02, step-up w LIFE-01, są w zakresie, z przeglądem CPA/EA); zdrowie (ewentualny test na healthscorer.com, nie na nowej domenie); emerytura, opieka, kredyty studenckie i e-commerce.

## 5. Ekonomika bez fałszywej precyzji

Wszystkie wartości to założenia (`economics.csv`): przychodowe oparte na niezweryfikowanych zakresach vendorskich, kosztowe i czasowe to szacunki własne (Z-09, Z-15, Z-16). Trajektoria to ilustracja, nie prognoza.

| Wskaźnik | Kons. | Baz. | Opt. |
|---|---|---|---|
| Przychód reklamowy na 1000 sesji (średnia roczna) | 1,0 USD | 5,9 USD | 21 USD |
| Sesje/mies. dla 1 / 3 / 10 tys. USD | 980 tys. / 2,9 mln / 9,8 mln | 171 tys. / 513 tys. / 1,71 mln | 48 tys. / 143 tys. / 477 tys. |
| Koszty stałe/mies.: 5 / 15 narzędzi | 880 / 1 710 USD | 350 / 640 USD | 180 / 290 USD |
| Próg rentowności gotówkowej (sesje/mies.): 5 / 15 narzędzi | 860 tys. / 1,68 mln | 59 tys. / 109 tys. | 9 tys. / 14 tys. |
| Próg, 5 narzędzi: z amortyzacją uruchomienia w 24 mies. / z wyceną czasu właściciela | 1,84 mln / 1,69 mln | 151 tys. / 141 tys. | 23 tys. / 22 tys. |
| Test opcji: gotówka / czas / czas budowy | 7,6 tys. USD / 273 h / ok. 7 mies. | 3,7 tys. USD / 200 h / 3–3,5 mies. | 2,0 tys. USD / 127 h / ok. 1,6 mies. |
| Silnik + 5 symulatorów: gotówka / czas | 24 tys. USD / 485 h | 12,9 tys. USD / 380 h | 7,1 tys. USD / 275 h |
| Nowe narzędzie: ekspert / czas właściciela | 4 500 USD / 53 h | 2 450 USD / 45 h | 1 375 USD / 37 h |
| Sesje/mies. na narzędzie do zwrotu jego gotówki w 24 mies. | 265 tys. | 22 tys. | 3,2 tys. |
| Mies. 12: narzędzia / przychód / wynik gotówkowy (USD/mies.) | 4 / 2 / −790 | 12 / 130 / −2 870 | 23 / 4 390 / +1 270 |
| Skumulowany wynik gotówkowy po 36 mies. | −52 tys. USD | −52 tys. USD | +71 tys. USD |
| Maks. zaangażowanie gotówki | 52 tys. USD | 52 tys. USD | 19 tys. USD |
| Miesiąc zwrotu: gotówka / z wyceną czasu | brak / brak | brak / brak | 21 / 34 |

Czas budowy liczono przy dostępności właściciela 40 / 60 / 80 h/mies. Bazowo skumulowany wynik gotówkowy: −34 tys. USD po 12 mies., −47 tys. po 24 mies.; z wyceną czasu −110 tys. po 36 mies. Wynik miesięczny obejmuje ekspertów nowych narzędzi (stąd gorszy mies. 12 w bazie niż konserwatywnie).

- **Założenia kluczowe:** page RPM USA 2,4 / 8 / 18 USD (brak danych pierwotnych dla stron-narzędzi; mediana vendorska ok. 2,4 USD [E-ADS-11]); odsłony na sesję 1,1 / 1,3 / 1,6 jako założenie [E-ADS-26, Z-02]; udział AI w sesjach ludzi 0,3% / 1% / 5% (benchmarki 0,1–1%); obserwacja właściciela 10–30% tylko jako wrażliwość. CPC Search nie przeliczamy na przychód serwisu [E-ADS-15].
- **Wrażliwość:** przy page RPM 2,4 USD we wszystkich scenariuszach przychód wynosi 1,0 / 1,8 / 2,8 USD na 1000 sesji.
- **Sesje AI to ułamek:** bazowo przy 1000 USD/mies. ok. 1,6 tys. ze 171 tys. sesji pochodzi z asystentów AI, ok. 156 tys. z wyszukiwarek i innych źródeł, ok. 14 tys. to boty.
- **Kontekst Omni Calculator:** ok. 15–30 USD na 1000 wizyt (szacunek na szacunkach: ok. 4,2–5 mln USD/rok wg Growjo, nieaudytowane, / 14–23 mln wizyt/mies.; ruch globalny, wiele odsłon, dojrzała marka). Rozbieżność z bazą (5,9 USD) to argument za pomiarem w G0 (krok 1b), nie za podnoszeniem bazy.
- **Dodatek poza bazą (hipoteza):** lead-gen/afiliacja przy niezweryfikowanym założeniu konwersji 0,2–1% i wypłacie 10–50 USD daje 20–500 USD na 1000 sesji; próg rentowności 5 narzędzi z lead-genem: 42 tys. / 2,7 tys. / 0,4 tys. sesji. To wynik własnych założeń, nie dowód zachowania rynku (wymaga też zgód TCPA). Niezależnie od modelu NerdWallet i SmartAsset raportują przychody głównie z partnerów i leadów [E-POR2-06/07].

## 5a. Strategie alternatywne

| Strategia | Koszt testu | Czas do sygnału | Przychód (jednostka) | Zgodność z ograniczeniem właściciela |
|---|---|---|---|---|
| Test na healthscorer.com (HLTH-02 lub symulator zdrowotny) | ~0 USD + 30–60 h | 1–3 mies. | AdSense na istniejącym koncie i ruchu | pełna (AdSense), ale inna tematyka i YMYL zdrowotny |
| B2B embed / white-label RENO-02, RENO-03 (dekarze, HVAC, agenci ubezpieczeniowi, credit unions; model Rewiring America [E-POR2-04]) | rozmowy z 5 firmami: 5–10 h | 2–6 tyg. | abonament na klienta (hipoteza: 50–100 USD/mies.; niezweryfikowane) | niezgodne z „AdSense jako baza” — osobna decyzja |
| Lead-gen/afiliacja jako dodatek | integracja + zgody TCPA | 3–6 mies. | 20–500 USD/1000 sesji (hipoteza z własnych założeń) | tylko dodatek; nie ratuje modelu w analizie podstawowej |
| Płatny test ruchu (Google Ads 300–500 USD) na MVP RENO-02 | 300–500 USD + MVP | 2 tyg. | pomiar ukończenia i RPM (nie przychód docelowy) | zgodne jako pomiar, wymaga zgody właściciela |
| Subskrypcja / raport płatny (model ProjectionLab: deklarowane ~1 mln USD ARR, VI 2025 [E-POR2-02]) | landing + waitlista | 1–2 mies. | przedpłaty / zapisy | niezgodne z bazą; osobna decyzja |

## 6. Pierwszy eksperyment: bramka G0 (dni 0–14; ok. 0 USD; ok. 15–25 h właściciela)

- **1a. Kanał AI (kierunkowo, inna domena i tematyka):** GA4 i logi healthscorer.com za 90 dni: sesje ludzi z referrerem lub `utm_source` asystentów, osobno dla ChatGPT, Gemini/AI Mode, Perplexity, Copilota i Claude, po odfiltrowaniu botów (`ChatGPT-User`, `OAI-SearchBot`, `Claude-User` itd.); Bing Webmaster „AI Performance”.
- **1b. Kalibracja monetyzacji (kierunkowo):** z AdSense i GA4 healthscorer.com page RPM (USA i ogółem), odsłony na sesję i udział odsłon z reklamą na stronach z formularzem; wyniki do `economics.csv` (Z-01…Z-05, K-06).
- **2. Popyt w Google dla RENO-02 (K-04):** Keyword Planner i Google Trends dla 10–20 fraz w 3–5 klastrach (np. wiek dachu a ubezpieczenie, ACV vs RCV, wymiana przed sprzedażą). **Próg (propozycja decyzyjna, nie norma rynkowa): łącznie ≥ 5 tys. wyszukiwań/mies. w USA.**
- **3. SERP i AI w Google (K-05):** dla 10 fraz: czy AIO/AI Mode generuje własny kalkulator lub tabelę wariantów; ile wyników top 10 to fora lub małe domeny. **Próg (propozycja): dla ≥ 3 fraz są w top 10 ≥ 2 wyniki z forów lub małych domen, a AI Mode/AIO nie generuje pełnego porównania wariantów w więcej niż połowie fraz.**
- **4. Ręczna weryfikacja konkurencji RENO-02:** otworzyć strony kandydatów (`top-10-products.md`, `competitor-audit.csv`) i przetestować formularze. **Produkt odpada, jeśli jedno narzędzie pokrywa ≥ 3 kluczowe zależności** (ACV/RCV lub harmonogram wypłat; udział wiatr/grad; horyzont sprzedaży; demontaż i montaż PV; finansowanie).
- **5. Panel asystentów (pomiar bazowy, nie warunek):** 5 produktów × 4 prompty z prośbą o kalkulator × 5 asystentów × 2 powtórzenia (ok. 10–15 h), wyniki osobno dla każdej platformy.

**Reguła bramki:** test opcji budujemy tylko wtedy, gdy **jednocześnie spełnione są kroki 2, 3 i 4**. Kroki 1a, 1b i 5 tylko kalibrują oczekiwania: jeśli 1a pokaże ≥ 1% sesji ludzi z AI i ≥ 2 tys. takich sesji/mies., kanał AI traktujemy jako realny dodatek (wskaźnik pośredni); jeśli 1b pokaże page RPM USA na stronach z formularzem < 2,4 USD, liczymy dalej scenariusz konserwatywny. Deklaracja właściciela („akceptuję Google organic”) **nie jest** warunkiem bramki.

**Po bramce:** przy ok. 15 h/tydz. RENO-02 powstaje w ok. 3–3,5 mies.; decyzje zapadają 90 dni i 6 mies. od indeksacji (ok. mies. 6–7 i 9–10 od startu) według reguł w `architecture-and-validation.md` §4 (propozycje decyzyjne, nie normy rynkowe).

**Najtańsza alternatywa (opcjonalna, za zgodą właściciela):** MVP RENO-02 bez pełnego silnika + 300–500 USD płatnego ruchu przez 2 tygodnie (pomiar ukończenia i RPM) oraz rozmowy z 5 potencjalnymi klientami B2B.

## 7. Granice pewności

- **Strony nieotwierane:** WebFetch, curl i przeglądarka były zablokowane, więc funkcje konkurentów to deklaracje ze streszczeń wyszukiwarki; funkcje za loginem lub niewidoczne są „niezweryfikowane”, nie „brak”. Pomiar: G0 krok 4 (K-03).
- **Brak danych SEO:** bez Keyword Plannera, Semrush, Ahrefs i Trends nie zebrano wolumenów; podaż treści to sygnał pośredni, więc kryterium „popyt” ma pewność niską. Pomiar: K-04, K-05 (G0 kroki 2–3).
- **Brak testów asystentów:** wyników nie symulowano; jest plan testu (G0 krok 5, K-02). Reguł Google nie przenosimy na innych asystentów.
- **Limit wyszukiwań:** 200 wywołań na turę wspólnie dla agentów, w fali 1 po 4–11 zapytań; mimo uzupełnień oceny rodzin mają pewność niską–średnią.
- **Monetyzacja:** page RPM i odsłony na sesję zmierzy kierunkowo G0 krok 1b, a dla branży dom/auto test RENO-02; politykę AdSense wobec stron-narzędzi trzeba potwierdzić (K-06).
- **Kanał AI właściciela:** obserwacja 10–30% ruchu z AI jest niezweryfikowana (K-01, krok 1a); utrata UTM zaniża atrybucję [E-VER-C12].

## 8. Warunek przerwania projektu

Przerwać projekt (nie tylko produkt), jeśli zajdzie którekolwiek z poniższych: (1) bramka G0 nie przechodzi — ręczna weryfikacja znajduje narzędzie pokrywające ≥ 3 kluczowe zależności RENO-02 albo pomiar popytu i SERP w Google nie spełnia progów; (2) 90 dni od indeksacji RENO-02: < 100 wyświetleń GSC/mies. i 0 cytowań w panelu asystentów oraz w Bing AI Performance; (3) 6 mies. od indeksacji RENO-02: zmierzony przychód < 2 USD na 1000 sesji ludzi albo < 1 tys. sesji ludzi/mies. bez wzrostu przez 3 kolejne miesiące; (4) skumulowana strata gotówkowa przekracza 8 tys. USD albo czas właściciela na G0 i budowę testu (silnik + RENO-02, bez utrzymania po publikacji) przekracza ok. 300 h, zanim spełnione zostaną kryteria kontynuacji. Progi to propozycje decyzyjne, nie normy rynkowe. Po przerwaniu ewentualną kontynuację rozważać tylko w innym modelu (B2B embed/white-label, lead-gen, subskrypcja), osobną decyzją.
