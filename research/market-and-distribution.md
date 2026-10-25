# Rynek, popyt w USA i dystrybucja przez asystentów AI

Data badania: 2026-10-25. Identyfikatory `E-…` odsyłają do rejestru dowodów w `evidence-and-assumptions.md` (tam URL-e, daty dostępu i poziom pewności).

## 0. Zakres i ograniczenia metody

| Narzędzie | Stan w tej sesji | Skutek |
|---|---|---|
| Wyszukiwarka (WebSearch, tryb standard/extended) | działa; **limit 200 zapytań na turę**, wspólny dla wszystkich agentów | badanie prowadzono falami z twardymi limitami na agenta; część agentów pierwszej fali wykonała tylko 4–10 zapytań (zaznaczono w ich wynikach) |
| Odczyt stron (WebFetch, curl, przeglądarka) | **zablokowany przez politykę sieci środowiska** (DNS / 403) | żadna strona konkurenta nie została otwarta; funkcje konkurentów oceniono na podstawie streszczeń wyników wyszukiwania („search-summary”). Formularzy i przykładowych wyników nie testowano |
| Dane SEO (wolumeny, CPC, ruch domen) | brak dostępu (brak kont Ahrefs/Semrush/Keyword Planner) | **nie podaję żadnych wolumenów słów kluczowych**; tam, gdzie cytuję ruch domen, są to szacunki Semrush/Similarweb widoczne w wynikach wyszukiwania |
| Testy asystentów (ChatGPT, Perplexity, Gemini, Copilot, Claude w wersjach konsumenckich) | brak dostępu | wyników testów **nie symulowano**; przygotowano plan testu i pule promptów (`top-10-products.md`, `architecture-and-validation.md`) |
| Analityka healthscorer.com | nieprzekazana | nie wyciągam wniosków o RPM ani o udziale ruchu AI na tej domenie |

Badanie wykonało 17 agentów w fali 1 (fundamenty, rodziny, pomysły startowe), 10 agentów uzupełniających, 2 weryfikatorów adwersaryjnych i 25 audytorów konkurencji (fala 2) oraz agentów pogłębionej weryfikacji finalistów. Łącznie kilkaset zapytań; wszystkie dowody o konkurencji mają status „search-summary”.

---

## 1. ETAP A — weryfikacja podstawowej tezy biznesowej

### A1. Czy portfel zaawansowanych narzędzi na jednej domenie ma sens pod monetyzację reklamową?

**Odpowiedź: ma sens tylko warunkowo i słabszy, niż zakłada hipoteza.** Dowody:

1. **Mechanika AdSense działa przeciw formatowi „jeden interaktywny ekran”.** Od 2024 r. AdSense rozlicza wydawców za wyświetlenie (wydawca otrzymuje 80% po opłacie strony kupującej, efektywnie ok. 68%) [E-VER-C7, E-ADS-01]. Polityka umieszczania reklam zabrania odświeżania reklam bez działania użytkownika [E-VER-C7, E-ADS-04]. Długi czas spędzony na symulatorze nie zamienia się więc w kolejne wyświetlenia. Strony narzędziowe przypominają landing pages (ok. 1–1,5 odsłony na sesję), a nie blogi (3–10) [E-ADS-26].
2. **Polityki wydawców ograniczają liczbę bezpiecznych slotów.** Reklamy nie mogą sąsiadować z elementami interaktywnymi ani ich zasłaniać [E-ADS-03]. Na ekranach bez treści wydawcy reklamy są zakazane [E-ADS-02]. Symulator to w dużej części pola, suwaki i przyciski, więc sloty zostają głównie nad nagłówkiem, pod wynikami i w bocznej kolumnie na desktopie.
3. **Model display działa w danych głównie przy ogromnej skali i szerokim, płytkim katalogu.** Omni Calculator: ok. 3,7–3,8 tys. kalkulatorów, 18–23 mln wizyt/mies., ok. 70 pracowników, przychód szacowany przez strony trzecie na ok. 4–5 mln USD/rok, monetyzacja głównie AdSense [E-POR-01..03, E-POR2-05]. To szacunki, nie dane finansowe.
4. **Głębokie, zintegrowane narzędzia decyzyjne nie żyją z display.** ProjectionLab — subskrypcja, deklarowane ~1 mln USD ARR przy 3 FTE [E-POR2-02]. Boldin i DealCheck — freemium/subskrypcja [E-POR2-03]. FI Calc — darowizny [E-POR2-01]. Rewiring America — non-profit, dystrybucja B2B przez embed/API [E-POR2-04].
5. **Najwięksi wydawcy narzędzi finansowych to biznesy lead-gen/afiliacyjne.** NerdWallet: ok. 836,6 mln USD przychodu w FY2025, raportowany według produktów partnerów (największy segment: Insurance, 280,8 mln USD) [E-POR2-06]. SmartAsset: rdzeniem jest sprzedaż leadów doradcom [E-POR2-07]. Kalkulatory są tam lejkiem do ofert, nie produktem reklamowym.
6. **Wysoki CPC reklamodawców nie przekłada się na RPM display.** Finance & Insurance: ok. 3,46 USD CPC w Search wobec ok. 0,86 USD w Display Network [E-ADS-15].

Wniosek: portfel symulatorów **może** generować przychód z display, ale (a) przychód na sesję będzie niski (model bazowy: ok. 7 USD na 1000 sesji, zob. `economics.csv`), (b) istniejące dowody o głębokich narzędziach wskazują na inne modele monetyzacji. Ograniczenie właściciela („reklama bazą, reszta dodatkiem”) jest najsłabszym elementem modelu. Nie zmieniam go w analizie podstawowej, ale pokazuję jego koszt.

### A2. Czy asystenci AI kierują użytkowników do takich narzędzi, zamiast wykonywać zadania sami?

**Odpowiedź: nie znaleziono dowodów, że kierują w istotnej skali. Kierunek rozwoju produktów asystentów jest odwrotny.**

| Ustalenie | Dowód |
|---|---|
| Ruch z asystentów AI to rząd 0,1–1% ruchu typowej witryny | Ahrefs: 0,17% (II 2025), ok. 0,25% (VII 2025), 0,28% w trackerze z III 2026 (74 752 strony); Conductor: 1,08% dla domen enterprise [E-AI-02, E-VER-C5] |
| W kanale AI dominuje jeden dystrybutor | ChatGPT: 81–95% referencji z chatbotów zależnie od miesiąca i dostawcy danych [E-AI-03] |
| Tylko mała część odpowiedzi ChatGPT zawiera link | 6,8% odpowiedzi (USA, desktop, V 2026); finanse 8,0%, podróże 22,6% (Similarweb) [E-VER-C3] |
| Największy katalog kalkulatorów dostaje z AI pomijalny ruch | omnicalculator.com: ChatGPT ok. 0,03%, Claude 0,01%, Gemini 0,006% ruchu (szacunek Semrush, połowa 2026), czyli rzędu 4–5 tys. wizyt z ChatGPT miesięcznie przy ~14 mln wizyt [E-AI-14, E-VER-C4] |
| Brak jakiegokolwiek badania, które wyodrębnia kalkulatory/symulatory wśród cytowanych lub klikanych URL-i | przeszukano badania Semrush, Ahrefs, Profound, Evertune, Wix, Similarweb; cytowania trafiają głównie do listicles, stron produktowych, Reddita, YouTube, Wikipedii [E-AI-12, E-AI-13, E-CAP2-04] |
| **Asystenci sami generują interaktywne narzędzia** | 7.10.2026 OpenAI udostępniło wszystkim użytkownikom ChatGPT, także darmowym, „Intelligent UI”: kalkulatory, formularze i wykresy w odpowiedzi ([openai.com](https://openai.com/index/gpt-6-for-everyone/)) [E-VER-C2]. Google: generatywne UI w AI Mode (XI 2025 dla płatnych, od 19.08.2026 globalnie po angielsku, stopniowo w AI Overviews) [E-VER-C1] |
| Interakcja z narzędziami przenosi się do wnętrza czatu | MCP Apps (26.01.2026) — interaktywne UI narzędzi renderowane w Claude, ChatGPT i innych klientach [E-VER-C10]; aplikacje w ChatGPT mogą dziś monetyzować tylko towary fizyczne przez zewnętrzny checkout [E-VER-C10] |
| Platformy AI monetyzują intencję komercyjną u siebie | reklamy w ChatGPT od 9.02.2026 (USA, Free/Go), z wyłączeniem tematów wrażliwych, w tym zdrowia [E-VER-C9]; reklamy w Google AI Mode od 2025 [E-AI-29] |
| Kontrargument: ruch z AI jest zwykle bardziej zaangażowany | niższy bounce, więcej odsłon; dane o konwersji sprzeczne (Adobe +31%, badanie 973 sklepów −13% vs organic) [E-AI-30] |

Ruch z asystentów **rośnie**, np. +117% r/r w referencjach globalnie i skoki po zmianach UI ChatGPT [E-AI-01]. Jest jednak niestabilny: −52% w VII–VIII 2025 po zmianie wag cytowań i skok +158% tydzień do tygodnia w V 2026 po zmianie formatu linków [E-AI-04]. Obserwacja właściciela, że healthscorer.com „ma ruch z AI”, może być prawdziwa. Wymaga jednak weryfikacji w logach: pobrania przez boty `ChatGPT-User`/`Claude-User` to nie wizyty ludzi [E-AI-22], a część ruchu ludzi z aplikacji ChatGPT ląduje w „Direct” [E-AI-20, E-VER-C12].

### A3. Lejek: obecność marki → cytowanie → link → wizyta → wizyta z przychodem

| Etap | Definicja operacyjna | Jak mierzyć | Typowe „przecieki” (dowody) |
|---|---|---|---|
| 1. Obecność marki | nazwa serwisu/narzędzia pojawia się w treści odpowiedzi | panel promptów uruchamianych wielokrotnie w UI; narzędzia typu Profound/Peec/Ahrefs Brand Radar (próbkowanie) | listy rekomendacji powtarzają się identycznie w <1 na 100 uruchomień [E-AI-23]; wyniki API ≠ UI (np. źródła w 84% vs 26% promptów) [E-AI-23] |
| 2. Cytowanie źródła | URL serwisu na liście źródeł | Bing Webmaster Tools „AI Performance” (Copilot/Bing, bez kliknięć) [E-AI-21]; GSC raport „Generative AI” (tylko wyświetlenia AIO/AI Mode łącznie) [E-AI-21]; panel promptów | ChatGPT cytuje ok. 50% pobranych URL-i; 44% cytowań pochodzi z pierwszych 30% tekstu [E-AI-12, E-AI-14] |
| 3. Klikalny link | link widoczny i klikalny w UI | panel promptów (zrzut + zapis) | 6,8% odpowiedzi ChatGPT z linkiem (finanse 8%) [E-VER-C3]; w Google AIO link w podsumowaniu klikany w ok. 1% wizyt [E-AI-06] |
| 4. Wizyta człowieka | sesja z referrerem chatgpt.com / perplexity.ai / gemini.google.com / copilot.microsoft.com / claude.ai lub `utm_source=chatgpt.com` | GA4 (kanał „AI Assistant” od V 2026, zależny od referrera) [E-AI-21]; logi serwera z UA i IP; zapis parametru UTM po stronie serwera | aplikacje mobilne gubią referrer → „Direct” [E-AI-20]; błąd UTM w ChatGPT 8–15.10.2026 przesunął ok. 31 tys. wizyt dziennie do Direct na ~500 stronach [E-VER-C12]; boty `ChatGPT-User`/`Claude-User` to pobrania, nie wizyty [E-AI-22] |
| 5. Wizyta z przychodem | sesja człowieka z co najmniej jednym widocznym wyświetleniem reklamy | AdSense: raport według stron/kanałów URL; łączenie z GA4 po stronie i dacie | adblock 19–33% w USA [E-ADS-17]; GPC/RDP w części stanów → reklamy niespersonalizowane [E-ADS-19]; agenci AI klasyfikowani jako GIVT/SIVT (zero przychodu lub ryzyko IVT) [E-ADS-23] |

Praktyczny wniosek: KPI kanału AI to **odsetek promptów testowych z klikalnym linkiem do serwisu** i **przychód z sesji z referrerem AI**, a nie „widoczność marki”.

### A4. Trwałe powody do użycia zewnętrznego narzędzia

| Powód | Trwałość (ocena) | Uzasadnienie |
|---|---|---|
| Interaktywność (suwaki, przeliczenia) | **niska** | od X 2026 ChatGPT, a od VIII 2026 Google AI Mode same generują interaktywne kalkulatory [E-VER-C1, E-VER-C2] |
| Wizualizacja, porównanie wariantów w tabeli | **niska** | j.w.; generatywne UI renderuje wykresy i tabele |
| Świeże i lokalne dane, których asystent nie ma pod ręką (taryfy eksportowe, zniżki stanowe FORTIFIED, ścieżki składek NFIP, lokalne koszty) | **średnia** | asystent może je wyszukać, ale ich zebranie i złożenie w model jest kosztowne i podatne na błąd. Ta przewaga to jednak także koszt utrzymania [E-REG3-*] |
| Spójna, wersjonowana metodologia, audytowalność, eksport z zapisem założeń | **średnia–wysoka** | LLM-y mylą się w regułach podatkowych (TaxCalcBench: <1/3 poprawnych pełnych zeznań; nowsze modele lepsze na dobrze postawionych zadaniach, ale podają wynik przy sprzecznych danych zamiast zgłosić problem) [E-CAP-04, E-CAP-05] |
| Wielookresowa symulacja z sekwencją zdarzeń i progiem przełączenia | **średnia** | asystent zbuduje tabelę 3–4 scenariuszy, ale rzadziej spójny model przepływów z wrażliwością; przewaga maleje z każdą generacją modeli (hipoteza) |
| Prywatność (bez podawania danych finansowych czatowi) | **niska** | 40% Amerykanów deklaruje, że nie poda danych finansowych AI (Qlik), ale 77% użytkowników pytających chatbota o finanse podało dane osobowe (NerdWallet) [E-CAP2-16, E-CAP2-17] |
| Zaufanie do neutralnego źródła (vs lead-gen instalatora lub pożyczkodawcy) | **średnia** | w wielu niszach najbliższe narzędzia to kalkulatory sprzedawców; neutralność jest wyróżnikiem, ale trudnym do zakomunikowania w odpowiedzi AI (hipoteza) |

### A5. Zadania, które szybko stracą sens jako osobne strony

- jednowzorowe kalkulatory (rata, break-even udziału własnego, ROAS, rent vs buy w prostej wersji);
- porównania, w których użytkownik ma wszystkie dane w dokumentach (oferta, polisa, umowa leasingu) — asystent przeczyta plik i policzy;
- ogólne wyjaśnienia reguł („czy wymienić dach przed PV?”) — heurystyki są powszechne i asystent je poda [E-DEM-23];
- generyczne „X vs Y TCO” (EV vs gas, HDHP vs PPO) — zatłoczone i łatwe do wygenerowania.

Relatywnie odporniejsze: decyzje wieloletnie z sekwencją zdarzeń, w których **wynik zależy od niepewnego parametru i warto pokazać próg przełączenia**. Przykład: dach × ubezpieczenie × horyzont sprzedaży. Takie decyzje wymagają też danych regulacyjnych o niskiej dostępności. Ich odporność jest jednak względna, nie absolutna.

### A6. Jedna domena czy kilka (skrót; pełna analiza w `architecture-and-validation.md`, sekcja 1)

- **Produktowo:** wspólne silniki (oś czasu przepływów, finansowanie, wartość domu, ubezpieczenie) przemawiają za jedną domeną o spójnej funkcji „decyzje kapitałowe gospodarstwa domowego”.
- **Operacyjnie:** jedna domena = jeden pipeline, jeden CMP, jedno konto reklamowe, ale też jeden punkt awarii (IVT, kara algorytmiczna) [E-ADS-05, E-ADS-07].
- **SEO:** Google dokumentuje „topic authority” tylko dla newsów [E-POR2-09]. Kary za szerokość nie udokumentowano, ale sygnały site-wide istnieją, a słaba część katalogu może obniżyć ocenę całej witryny [E-POR2-08].
- **AI:** brak dowodów, że szerokość domeny wpływa na cytowania w ChatGPT/Perplexity. Widoczność w AI koreluje raczej z obecnością marki poza witryną (YouTube, Reddit, Wikipedia) [E-POR2-12] i z dopasowaniem strony do wąskiego pod-zapytania [E-AI-12].

---

## 2. Popyt w USA: co mówią dane (bez wolumenów słów kluczowych)

Poniższe liczby mierzą **roczne zdarzenia, zasoby lub kwoty**, a nie miesięczny popyt w wyszukiwarce ani gotowość do kliknięcia. Wolumenów zapytań do LLM nie da się zaobserwować w tym badaniu.

| Obszar | Wskaźnik (co mierzy) | Wartość | Źródło |
|---|---|---|---|
| Samochody | nowe auta (prognoza 2026) | 16,1 mln | Cox [E-DEM-13] |
| Samochody | wymiany z ujemnym kapitałem przy zakupie nowego auta | 29,1% wymian z kredytem, średnio −7 107 USD (Q3 2026) | Edmunds [E-DEM-14] |
| Home equity | nowe kredyty home equity 2025 | 1,4–2,6 mln zależnie od dostawcy | TransUnion, Cotality, Equifax [E-DEM-02] |
| Kredyty gotówkowe | nowe niezabezpieczone kredyty (Q4 2025) | 7,6 mln w kwartale | TransUnion [E-DEM-03] |
| Sprzedaż domów | transakcje 2025 | 4,06 mln (najniżej od 1995) | NAR [E-DEM-04] |
| Sprzedaż domów | mediana czasu posiadania | 12 lat (2025) | Redfin [E-DEM-05] |
| Refinansowanie | wolumen USD 2026→2027 | 713 → 571 mld USD (−17%), tylko 23% kredytobiorców ma oprocentowanie >6% | MBA [E-DEM-01] |
| Remonty | wydatki właścicieli | ok. 522–526 mld USD/rok | Harvard JCHS LIRA [E-DEM-06] |
| Dachy | wymiany dachów | ok. 5 mln/rok — **szacunek modelowy o niskiej pewności** | blogi branżowe [E-DEM-07] |
| HVAC | dostawy AC + pomp ciepła | 7,75 mln szt. w 2025 (−20%) | AHRI [E-DEM-08] |
| Ubezpieczenia domu | szkody zgłaszane rocznie | 5,3–5,6% ubezpieczonych domów (źródło wtórne) | Triple-I/ISO via blog [E-DEM-09] |
| PV | instalacje domowe | Q2 2026: −12% r/r; prognoza 2026: −18% do −23% | Wood Mackenzie/SEIA [E-DEM-10] |
| Zasilanie | przerwy na odbiorcę | 11 h w 2024 (80% zdarzenia ekstremalne) | EIA [E-DEM-11] |
| Praca | dobrowolne odejścia (zdarzenia) | 38,0 mln w 2025 | BLS JOLTS [E-DEM-15] |
| Relokacja | przeprowadzki międzystanowe | 2,1% populacji (2024) | Census ACS [E-DEM-16] |
| Emerytura | osoby kończące 65 lat | ok. 4,1 mln/rok do 2027 | Retirement Income Institute [E-DEM-17] |
| Wynajem | nieruchomości 1–4 lokale u osób fizycznych | 15,9 mln (2021) | RHFS [E-DEM-18] |
| Opieka | opiekunowie rodzinni (zasób) | 63 mln (2025) | AARP/NAC [E-DEM-19] |
| Opieka | mediana kosztu assisted living | 74 400 USD/rok (dane 2025) | CareScout [E-DEM-19] |
| Starzenie | osoby 50+ chcące zostać w domu | 75% | AARP [E-DEM-20] |
| E-commerce | aktywni sprzedawcy Amazon (USA) | ok. 500 tys. (ścisła definicja, szacunek) | Marketplace Pulse via AMZ Prep [E-DEM-21] |

**Wniosek (hipoteza):** w latach 2025–2026 ciężar decyzji gospodarstw przesuwa się z „przeprowadzić się / refinansować” na „zostać, remontować, uruchomić kapitał z domu, spłacić dług, poradzić sobie z ubezpieczeniem”. Energia (PV, generatory) słabnie po wygaśnięciu 25D i przy braku dużych awarii [E-DEM-10, E-DEM-12]. Samochody mają największy, stabilny przepływ decyzji.

**Dowody na częstotliwość pytań online są słabe.** Nie znaleziono żadnych opublikowanych wolumenów wyszukiwań ani danych Google Trends 2025–2026 dla badanych tematów [E-DEM-22..24]. Dostępne są tylko sygnały pośrednie: liczba stron odpowiadających na pytanie (np. „should I replace my roof before solar”), liczba istniejących kalkulatorów, wątki forów. **Liczba konkurencyjnych stron nie jest miarą popytu.**

---

## 3. Dystrybucja przez asystentów: platforma po platformie

Zasad Google nie przenoszę automatycznie na pozostałe systemy.

| Platforma | Skąd bierze źródła | Co jest potrzebne, by być pobranym | Udział w referencjach AI | Uwagi |
|---|---|---|---|---|
| ChatGPT (search) | własny indeks OpenAI (doniesienia o „Labrador”, niepotwierdzone przez OpenAI) + Bing; Deep Research korzystał z Binga [E-AI-24] | dopuszczenie `OAI-SearchBot` (robots.txt; zmiana działa po ok. 24 h); treść jako widoczny HTML [E-AI-22, E-POR2-14] | 81–95% [E-AI-03] | ok. 3 linki na odpowiedź [E-CAP2-02]; tylko ok. 45% zbieżności z top 10 Google [E-AI-15]; Intelligent UI od X 2026 [E-VER-C2] |
| Perplexity | własny indeks („setki miliardów stron”) [E-AI-25] | `PerplexityBot`; świeżość treści (82% cytowań z treści <30 dni wg źródła wtórnego) [E-CAP2-02] | ~1% | ok. 19 linków na odpowiedź; >91% zbieżności domen z top 10 Google [E-AI-15]; reklamy wstrzymane, Comet Plus dla wydawców [E-AI-29] |
| Google AI Overviews / AI Mode | indeks Google | klasyczne SEO; `nosnippet` wyłącza użycie w AIO/AI Mode [E-AI-22] | Gemini 2–13% referencji AI (zmienne) [E-AI-03] | AIO obniża CTR o 35–61% [E-AI-06..08]; AI Mode −18,8 pp CTR zewnętrznego w RCT [E-VER-C6]; generatywne UI [E-VER-C1] |
| Copilot | Bing | Bing Webmaster Tools, IndexNow (niezweryfikowane w tym badaniu) | ~1% | jedyny raport cytowań od dostawcy (Bing AI Performance) [E-AI-21] |
| Claude | Brave Search + drugi dostawca (wg listy podprocesorów) [E-AI-25] | `Claude-SearchBot`, `Claude-User` | ~1% | — |

**Implikacje techniczne:** treść symulatora (założenia, wynik przykładowego scenariusza, wnioski) musi być w widocznym HTML renderowanym po stronie serwera. Systemy AI czytają widoczny HTML, a JSON-LD ignorują lub traktują marginalnie [E-POR2-14]. `llms.txt` nie wykazał mierzalnego efektu [E-POR2-13]. Uwaga: od 15.09.2026 nowe domeny w Cloudflare dostają domyślną blokadę botów „Training/Agent” na stronach z reklamami [E-VER-C11]; trzeba to świadomie skonfigurować.

---

## 4. ETAP B — ocena rodzin produktów

Oceny 1–5 (wyżej = lepiej, łatwiej albo mniejsze ryzyko) pochodzą od agentów rodzin. Skorygowałem je tam, gdzie późniejsze dowody (fala uzupełniająca, audyt konkurencji) zmieniły obraz. **Pewność ocen jest niska–średnia:** część agentów miała tylko 4–11 zapytań (limit wyszukiwań). Oceny porządkują hipotezy, nie mierzą potencjału.

Kolumny: Pop = popyt i jego dowody; Kom = komercyjny charakter; Luka = luka zintegrowanego produktu; AI = przydatność dla dystrybucji AI; Wsp = wspólne modelowanie; Dane = niski koszt danych i aktualizacji; Błąd = niskie ryzyko błędów; Kat = potencjał katalogu; Rekl = dopasowanie do reklamy; Eksp = niski koszt kontroli eksperckiej.

| Rodzina | Pop | Kom | Luka | AI | Wsp | Dane | Błąd | Kat | Rekl | Eksp | Śr. | Werdykt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Samochody: keep/replace, finansowanie, leasing, ujemny kapitał | 5 | 5 | 3 | 3 | 5 | 2 | 4 | 5 | 5 | 4 | 4,1 | **rozwijać** — duży, stabilny przepływ decyzji, niski koszt ekspercki; ryzyko: proste przypadki asystent liczy sam, brak tanich danych o wartości aut |
| Remonty i kolejność inwestycji (dach, HVAC, okna) | 4 | 5 | 4 | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 3,7 | **rozwijać** — najlepsza luka integracyjna w domu; ryzyko: zmienność zachęt, brak darmowych lokalnych kosztów |
| Zakup / posiadanie / sprzedaż domu (buy-before-sell, sprzedać vs wynająć) | 4 | 5 | 3 | 3 | 5 | 4 | 2 | 4 | 4 | 3 | 3,7 | **rozwijać selektywnie** — silny lead-gen (HomeLight, Knock, Orchard) jako częściowa konkurencja |
| Finansowanie i dług (home equity, pilna gotówka) | 4 | 5 | 3 | 3 | 5 | 3 | 2 | 4 | 4 | 3 | 3,6 | **rozwijać** klaster „dostęp do kapitału z domu”; reszta zatłoczona |
| Katastrofy i ubezpieczenie domu (FORTIFIED, wiatr/grad, powódź) | 3 | 5 | 4 | 3 | 4 | 2 | 3 | 4 | 5 | 3 | 3,6 | **rozwijać w połączeniu z dachem**; powódź/NFIP później (niestabilne reguły) |
| Zapas i finansowanie zapasów (e-commerce) | 3 | 4 | 4 | 3 | 5 | 4 | 3 | 4 | 3 | 4 | 3,7 | **pilotaż poboczny** (founder-market fit); mała, B2B-owa populacja, płatne narzędzia (Cogsy, 8fig) |
| Freelancer / 1099: forma, emerytura, zdrowie | 4 | 5 | 3 | 4 | 5 | 3 | 2 | 4 | 5 | 2 | 3,7 | **później** — gęsta konkurencja częściowa, wysokie ryzyko podatkowe |
| Wczesna emerytura i klif ACA/MAGI | 3 | 4 | 4 | 4 | 5 | 3 | 2 | 4 | 4 | 3 | 3,6 | **zbadać** — realna zmiana 2026 (powrót klifu 400% FPL) [E-REG2-13]; wysoki koszt ekspercki |
| Zasilanie awaryjne | 3 | 4 | 4→2 | 3 | 4 | 4 | 3 | 3 | 4 | 4 | 3,4 | **ograniczyć** — po fali uzupełniającej luka obniżona: możliwy konkurent bezpośredni (Home Energy Planner — klasyfikacja sporna między agentami, do ręcznej weryfikacji) (`top-10-products.md` §0, seed F) |
| Nieruchomości na wynajem | 4 | 4 | 3→2 | 3 | 5 | 4 | 2 | 4 | 4 | 3 | 3,5 | **ograniczyć** do wąskich momentów; BiggerPockets „Sell vs Keep” i OverlineIQ to konkurenci bezpośredni (`top-10-products.md` §0, seed H) |
| PV i magazyny | 3→2 | 5 | 3 | 3 | 5 | 3 | 2 | 4 | 4 | 3 | 3,4 | **tylko jako gałąź** innych symulatorów; rynek kurczy się po 25D [E-DEM-10] |
| Ogrzewanie/chłodzenie, ciepła woda | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 3,5 | **rozwijać przez moment awarii** (repair vs replace vs heat pump) |
| Sprzęt: buy vs lease vs loan (firmy) | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 4 | 4 | 3 | 3,5 | później |
| Zabiegi medyczne: termin i finansowanie | 3 | 4 | 4 | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 3,5 | **zbadać** — bliskość healthscorer.com; uwaga: reklamy w ChatGPT pomijają zdrowie (neutralne dla nas) [E-VER-C9] |
| Spadki (dom, inherited IRA) | 3 | 4 | 3 | 4 | 4 | 4 | 2 | 4 | 4 | 3 | 3,5 | **zbadać** (dom dziedziczony z rodzeństwem) |
| Plan zdrowotny (pracodawca/ACA/HSA) | 5 | 3 | 2 | 3 | 5 | 3 | 2 | 4 | 4 | 3 | 3,4 | **tylko warianty złożone**; prosty HDHP vs PPO zatłoczony |
| Reklama, zwroty, unit economics (e-commerce) | 3 | 3 | 2 | 2 | 4 | 5 | 4 | 3 | 3 | 5 | 3,4 | moduł, nie rodzina |
| Emerytura i wypłaty | 4 | 5 | 2 | 3 | 5 | 2 | 2 | 4 | 4 | 2 | 3,3 | **nie wchodzić** szeroko (Boldin, ProjectionLab, MaxiFi, Pralana, Open Social Security); tylko wąskie decyzje z datą |
| Adaptacja domu i finansowanie opieki | 4 | 5 | 3 | 3 | 4 | 3 | 2 | 3 | 4 | 2 | 3,3 | **zbadać ostrożnie** — >10 częściowych kalkulatorów; wysoki koszt ekspercki, leady senior living pod lupą Senatu [E-ADS-34] |
| Fulfillment e-commerce (FBA vs 3PL) | 3 | 4 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 3,3 | pilotaż poboczny |
| Płynność firmy (cykl konwersji gotówki) | 2 | 3 | 3 | 2 | 5 | 5 | 3 | 3 | 3 | 4 | 3,3 | moduł |
| Edukacja i kredyty studenckie po 2026 | 4 | 4 | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 3 | 3,3 | **nie wchodzić** w spłaty (oficjalny Loan Simulator); ewentualnie porównanie ofert uczelni |
| EV vs ICE, ładowanie, ubezpieczenie | 3 | 4 | 2 | 2 | 4 | 3 | 3 | 3 | 4 | 4 | 3,2 | moduł rodziny samochodowej, nie produkt |
| Praca, relokacja, benefity | 3 | 3 | 3 | 2 | 4 | 3 | 3 | 4 | 3 | 3 | 3,1 | tylko wąsko (data odejścia × vesting × clawback) |
| Finansowanie małej firmy (SBA/MCA/LOC) | 4 | 5 | 2 | 2 | 4 | 3 | 2 | 3 | 4 | 2 | 3,1 | nie wchodzić |
| Ubezpieczenie zwierząt | 4 | 4 | 2 | 2 | 2 | 3 | 4 | 2 | 4 | 4 | 3,1 | później |
| Relokacja międzystanowa (podatki, koszty życia) | 4 | 4 | 2 | 3 | 4 | 1 | 3 | 3 | 4 | 3 | 3,1 | później |
| Opieka długoterminowa (LTC) | 3 | 4 | 3 | 3 | 3 | 3 | 2 | 3 | 4 | 2 | 3,0 | później |
| Opieka nad dziećmi vs praca | 4 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 4 | 3,0 | później (słaba reklama) |
| Ubezpieczenia ogólnie (udziały własne, rezerwy) | 3 | 4 | 3→1 | 2 | 4 | 2 | 2 | 3 | 4 | 2 | 2,7 | **odrzucić jako rodzinę**; zostają moduły („zgłosić szkodę?”, udział procentowy vs rezerwa) (`top-10-products.md` §0, seed B) |
| Import, cła, landed cost | 4 | 4 | 3 | 3 | 4 | 1 | 2 | 3 | 3 | 2 | 2,9 | tylko timing, nie stawki celne |
| Rozwód (dom) | 3 | 4 | 3 | 3 | 3 | 3 | 1 | 3 | 3 | 2 | 2,8 | później |
| Zatrudnienie W-2 vs 1099 | 3 | 4 | 2 | 2 | 3 | 2 | 2 | 3 | 4 | 2 | 2,7 | nie wchodzić |
| Taryfy energii | 3 | 3 | 2 | 2 | 5 | 1 | 2 | 3 | 3 | 2 | 2,6 | warstwa danych, nie rodzina |
| Klify świadczeń dla gospodarstw o niskich dochodach | 3 | 1 | 2 | 2 | 3 | 1 | 1 | 2 | 1 | 1 | 1,7 | **odrzucić** (brak monetyzacji, wysokie ryzyko) |

Średnia jest nieważona; ranking finalistów (`top-10-products.md`) używa wag z zadania.

### Obszary nieoczywiste dodane w badaniu

- **Starzejący się dach + ubezpieczenie (RCV/ACV, procentowe udziały wiatr/grad) + FORTIFIED + horyzont sprzedaży.** Zamiennik pomysłu A, łączy rodziny remontów, ubezpieczeń i sprzedaży domu. Zniżki FORTIFIED: Alabama ma mandat, Luizjana benchmarki od 1.01.2027, Kentucky obowiązkowe zniżki od 2026 [E-REG3-08].
- **Wczesna emerytura i klif ACA/MAGI.** Wzmocnione dopłaty ACA wygasły 31.12.2025, a przedłużenie przeszło w Izbie, ale nie w Senacie [E-REG2-13]. Bronze i catastrophic kwalifikują się do HSA od 2026 [E-REG2-10].
- **Zabiegi medyczne: termin w roku planu i finansowanie.** Domena bliska healthscorer.com.
- **Dom po rodzicu (spadek z rodzeństwem, dom przy przejściu rodzica do opieki).**
- **Decyzje e-commerce o zapasie i finansowaniu** (founder-market fit właściciela).
- **„Sump pump” i zalanie piwnicy przy przerwie zasilania** — wąski, konkretny problem po odrzuceniu ogólnego „bateria vs generator”.

---

## 5. Wnioski dla strategii dystrybucji

1. **Nie budować modelu na ruchu z asystentów AI.** Traktować go jako kanał mierzalny i wtórny wobec Google organic. Google też eroduje: AIO, AI Mode, generatywne UI [E-AI-06..09, E-VER-C1].
2. **Kanał AI nagradza markę i obecność poza witryną** (YouTube, Reddit, Wikipedia, wzmianki) [E-POR2-12, E-AI-19]. To stoi w sprzeczności z założeniem „bez społeczności i bez udostępniania linków”. Kanał AI bez marki jest wąski.
3. **Jeśli kanał AI ma działać, to w niszach, gdzie asystent potrzebuje danych lub metody, których nie ma**, i w zapytaniach z linkami (finanse: 8% odpowiedzi z linkiem). Hipoteza do testu, nie fakt.
4. **Pierwszym eksperymentem jest pomiar, nie budowa:** weryfikacja ruchu AI w logach healthscorer.com i panel promptów w 5 asystentach dla 10 finalistów (plan w `architecture-and-validation.md`).
