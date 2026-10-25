"""Generate finalist cards (markdown) from longlist + audit + wave2b refute/demand outputs.

Fala 3 (po recenzji): wspólne poprawki tekstu agentów (fix), etykiety dowodów popytu w dwóch osiach
(siła źródła / co źródło mierzy), formuła konkurencji z kanonu K10, statusy z product-opportunities.csv.
Moduł jest też importowany przez build_top10.py (funkcje fix, one, criteria_rows).

Runda 2 kontroli spójności: pełne teksty (bez ucinania) w kartach i tabelach kryteriów, kompletne listy konkurentów,
lista do ręcznej weryfikacji RENO-02 (G0 krok 4), nagłówki kart z pozycją w rankingu, godziny eksperta pilotów (kanon K4),
twierdzenia o asystentach jako hipotezy, polityki reklamowe jako niezweryfikowane, klasyfikacja przykładów pytań.
"""
import csv, json, os, re, sys

CSV_PRODUCTS = '/home/user/trackal/research/product-opportunities.csv'

W = [('demand', 'Dowody popytu', 20), ('gap', 'Luka zintegrowanego produktu', 20), ('ai_distribution', 'Potencjał dystrybucji AI', 15),
     ('ad_potential', 'Potencjał reklamowy', 15), ('feasibility', 'Wykonalność i koszt utrzymania', 10),
     ('reliability', 'Wiarygodność obliczeń i ryzyko', 10), ('shared_engine', 'Współdzielenie silników', 10)]
LV = {'low': 'niska', 'medium': 'średnia', 'high': 'wysoka'}
# Kategorie konkurentów wg kanonu K10: bezpośredni / częściowy / substytut / sporny (do ręcznej weryfikacji).
TYP = {'direct': 'bezpośredni', 'partial': 'częściowy', 'substitute': 'substytut',
       'probably_direct_unverified': 'sporny (możliwy bezpośredni; do ręcznej weryfikacji)'}
KIND = {'direct': 'bezpośrednie', 'indirect': 'pośrednie', 'estimate': 'estymacja', 'hypothesis': 'hipoteza'}

# Polityki reklamowe dla kategorii (recenzja spójności, rules#14): „brak ograniczeń kategorii wrażliwych” nie było sprawdzane.
ADPOL = ('ograniczeń polityk reklamowych AdSense i Google Ads dla tych kategorii (m.in. usługi finansowe: kredyty, HELOC, PACE, pożyczki) '
         'nie sprawdzano — niezweryfikowane (do sprawdzenia razem z polityką wobec stron-narzędzi, K-06)')
ADPOL_SHORT = 'ograniczeń polityk reklamowych dla tych kategorii nie sprawdzano (niezweryfikowane; zob. kolumnę „Luki”)'
ADPOL_SHORT_S = ADPOL_SHORT[0].upper() + ADPOL_SHORT[1:]

# Kryteria, dla których pewność jest z góry ograniczona do „niska” (kanon K10 i reguły briefu):
# popyt — brak wolumenów; reklama — page RPM niezmierzony; dystrybucja AI — asystentów nie testowano.
LOW_CAP = {
    'demand': ('Wolumenów wyszukiwań i promptów nie zmierzono (K-04). Podaż treści i kalkulatorów to sygnał pośredni, a liczba zdarzeń '
               '(transakcji, wymian, polis, zapisów) to górna granica populacji; żadne z nich nie jest pomiarem popytu online.'),
    'ad_potential': ('Page RPM stron-narzędzi niezmierzony (Z-01); łączenie kategorii reklamowych nie sumuje stawek (każde wyświetlenie to osobna aukcja); '
                     + ADPOL + '.'),
    'ai_distribution': ('Asystentów nie testowano; streszczenia narzędzia WebSearch to obserwacja pośrednia (proxy), nie test asystenta. '
                        'Wydanie funkcji generowania kalkulatorów potwierdzono tylko dla ChatGPT (Intelligent UI) i Google AI Mode [E-VER-C1, E-VER-C2]; '
                        'dla Perplexity, Copilota i Claude go nie weryfikowano.'),
}
# Prefiks uzasadnienia kryterium „dystrybucja AI”: przewidywania audytora o zachowaniu asystentów to hipotezy (reguły briefu).
AI_PREFIX = 'Ocena audytora (hipoteza; asystentów nie testowano): '

VER = 'wydanie potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]'
IUI = 'ChatGPT Intelligent UI (od 7–8.10.2026; potwierdzone w weryfikacji [E-VER-C2])'
AIM = 'Google AI Mode z generatywnym UI (od 19.08.2026 wg relacji SEJ [E-VER-C1])'

# Poprawki tekstów agentów (kolejność ma znaczenie: najpierw dłuższe, konkretne wzorce).
SUBS = [
    # --- runda 2 kontroli spójności: wzorce, które muszą zadziałać przed ogólnymi ---
    # JOB-02: data „7.10.2026” rozcinana przez ogólny wzorzec „Kontekst zadania: …”.
    (r"Kontekst zadania: ChatGPT Intelligent UI od 7\.10\.2026, Google AI Mode od 19\.08\.2026\.",
     "ChatGPT Intelligent UI od 7–8.10.2026 i Google AI Mode od 19.08.2026: " + VER + "."),
    # rules#8: funkcje potwierdzone tylko dla ChatGPT i Google AI Mode, nie dla „asystentów” w ogóle.
    (r"Od 10\.2026 asystenci mają generatywne UI kalkulatorów\.",
     "ChatGPT (Intelligent UI, od 7–8.10.2026) i Google AI Mode (od 19.08.2026) generują kalkulatory w odpowiedzi [E-VER-C1, E-VER-C2]; "
     "dla Perplexity, Copilota i Claude tego nie zweryfikowano."),
    (r"leżą w zasięgu asystentów, które od 2026 renderują kalkulatory w odpowiedziach;",
     "prawdopodobnie leżą w zasięgu asystentów: ChatGPT (Intelligent UI, od 7–8.10.2026) i Google AI Mode (od 19.08.2026) "
     "generują kalkulatory w odpowiedzi [E-VER-C1, E-VER-C2], a dla Perplexity, Copilota i Claude tego nie zweryfikowano;"),
    (r"a od X 2026 renderuje też kalkulatory \(ChatGPT Intelligent UI, Google AI Mode\)",
     "a ChatGPT (Intelligent UI) i Google AI Mode renderują też kalkulatory [E-VER-C1, E-VER-C2]"),
    (r"ChatGPT Intelligent UI i Google AI Mode generują kalkulatory\.",
     "ChatGPT Intelligent UI i Google AI Mode generują kalkulatory (" + VER + ")."),
    (r"ChatGPT Intelligent UI i Google AI Mode renderują kalkulatory w odpowiedzi\.",
     "ChatGPT Intelligent UI i Google AI Mode renderują kalkulatory w odpowiedzi (" + VER + "; jakości w tej niszy nie testowano)."),
    # rules#5: obserwacja generatora streszczeń WebSearch to nie odpowiedź asystenta; zachowanie asystentów = hipoteza.
    (r"Asystent wyszukiwania sam podał kompletny werdykt na przykładowy prompt\.",
     "Streszczenie narzędzia WebSearch (nie asystent konsumencki) samo podało werdykt na przykładowe zapytanie."),
    (r"Asystenci i AI-podsumowania wyszukiwarki odpowiadają na przykładowy prompt sami, wystarczająco dla większości użytkowników\.",
     "AI-podsumowania wyszukiwarki (narzędzie WebSearch) same odpowiedziały na przykładowy prompt; że asystenci zrobią to wystarczająco dla większości użytkowników, to hipoteza."),
    (r"potrafi wyrenderować formularz z 5–8 polami i policzyć wypłatę ACV, ratę HELOC i prosty break-even 'wymiana vs kredyt dla kupującego'\.",
     "według zapowiedzi OpenAI może renderować formularze i kalkulatory [E-VER-C2]; czy w tej niszy poprawnie policzy wypłatę ACV, ratę HELOC "
     "i prosty break-even 'wymiana vs kredyt dla kupującego', to hipoteza do sprawdzenia w G0, krok 5."),
    (r"Dla promptów z sekcji 'calculator request' trzeba spodziewać się, że asystent zbuduje narzędzie ad hoc\.",
     "Dla promptów z sekcji 'calculator request' prawdopodobne jest (hipoteza), że asystent zbuduje narzędzie ad hoc."),
    (r"których AI nie robi, jeśli użytkownik o nie nie poprosi", "których AI prawdopodobnie nie zrobi (hipoteza), jeśli użytkownik o nie nie poprosi"),
    (r"AI wymyśla parametry, które mogą zmieniać się między sesjami", "AI może wymyślać parametry, które zmieniają się między sesjami (hipoteza)"),
    (r"zapytania jakościowe \('should I…'\) zostaną w dużej mierze zaspokojone w AI bez kliknięcia\.",
     "zapytania jakościowe ('should I…') prawdopodobnie zostaną w dużej mierze zaspokojone w AI bez kliknięcia (hipoteza)."),
    (r"przykłady liczbowe, które AI chętnie przytacza z linkiem\.", "przykłady liczbowe, które AI może przytaczać z linkiem (hipoteza)."),
    (r"potrafią wyrenderować prosty interaktywny kalkulator wprost w odpowiedzi\.",
     "mogą renderować prosty interaktywny kalkulator wprost w odpowiedzi (jakości w tej niszy nie testowano)."),
    (r"Asystent przyjmie jedną średnią COP\.", "Asystent prawdopodobnie przyjmie jedną średnią COP (hipoteza)."),
    (r"\(1\) Co AI zrobi samo:", "(1) Co AI prawdopodobnie zrobi samo (hipoteza):"),
    (r"Z Intelligent UI albo AI Mode wyrenderuje prosty kalkulator dwóch wariantów (\([^)]*\)) z suwakami wzrostu cen i czynszu\. "
     r"To pokrywa większość popytu typu 'quick answer' i bezpośrednio kanibalizuje model AdSense oparty na odsłonach\.",
     r"Z Intelligent UI albo AI Mode prawdopodobnie wyrenderuje prosty kalkulator dwóch wariantów \1 z suwakami wzrostu cen i czynszu (hipoteza). "
     r"Może to pokryć znaczną część popytu typu 'quick answer' i kanibalizować model AdSense oparty na odsłonach (hipoteza; udziału popytu „quick answer” nie zmierzono)."),
    (r"To mocny dowód, że automatyczne odpowiedzi popełniają tu istotny błąd\.",
     "To sygnał (z generatora streszczeń WebSearch, nie z testu asystenta), że automatyczne odpowiedzi mogą tu popełniać istotny błąd."),
    (r"\(3\) Dystrybucja: AI Mode i Perplexity cytują dziś głównie strony lead-gen firm zarządzających najmem\.",
     "(3) Dystrybucja: według agenta AI Mode i Perplexity cytują dziś głównie strony lead-gen firm zarządzających najmem (niezweryfikowane; cytowań nie testowano)."),
    (r"\(a\) Audyt pokazał, że silnik wyszukiwania sam generuje ramę decyzji:",
     "(a) W audycie generator streszczeń narzędzia WebSearch (nie asystent konsumencki) sam podał ramę decyzji:"),
    (r"\(b\) Podpytania to prosta arytmetyka, którą LLM liczy poprawnie:",
     "(b) Podpytania to prosta arytmetyka. Modele zwykle dobrze liczą dobrze postawione zadania [E-CAP-05], ale przy sprzecznych danych podają wynik, "
     "zamiast zgłosić problem [E-CAP-05], a pełne zeznania podatkowe liczą poprawnie w mniej niż 1/3 przypadków [E-CAP-04]; dla tej niszy to hipoteza. Przykłady podpytań:"),
    (r"potrafią wyrenderować ad-hoc kalkulator z suwakami bezpośrednio w odpowiedzi\.",
     "mogą renderować ad-hoc kalkulator z suwakami bezpośrednio w odpowiedzi (jakości w tej niszy nie testowano)."),
    (r"Dowody z tej sesji \(search-summary\): \(1\) Sam silnik wyszukiwania",
     "Obserwacje pośrednie z tej sesji (search-summary; generator streszczeń WebSearch, nie test asystenta): (1) Sam silnik wyszukiwania"),
    (r"Wśród wyników nie było oficjalnego komunikatu OpenAI, a część źródeł jest niskiej jakości\. Szczegóły trzeba potwierdzić\.",
     "Agent nie znalazł oficjalnego komunikatu OpenAI, a część jego źródeł była niskiej jakości; w weryfikacji fali 3 wydanie potwierdzono w źródle pierwotnym [E-VER-C2]."),
    (r"Status i zasięg w USA w X 2026 wymagają sprawdzenia\.",
     "Status i zasięg w USA w X 2026 wymagają sprawdzenia (w weryfikacji fali 3: generatywne narzędzia w AI Mode globalnie po angielsku od 19.08.2026 wg relacji SEJ [E-VER-C1])."),
    (r"Mimo to prosty kalkulator break-even godzin lub runway oszczędności można dziś wygenerować ad hoc w odpowiedzi, z suwakami\.",
     "Prosty kalkulator break-even godzin lub runway oszczędności prawdopodobnie można dziś wygenerować ad hoc w odpowiedzi, z suwakami (hipoteza; nie testowano)."),
    (r"Gdzie asystent wygrywa:", "Gdzie asystent prawdopodobnie wygrywa (hipoteza):"),
    (r"Co asystent zrobi dobrze bez nas:", "Co asystent prawdopodobnie zrobi dobrze bez nas (hipoteza):"),
    (r"jest więc towarem i zaspokaja większość pytań bez kliknięcia\.",
     "jest więc towarem i prawdopodobnie zaspokaja większość pytań bez kliknięcia (hipoteza; udziału nie zmierzono)."),
    (r"Do tego asystenci powtarzają konsensus wydawców", "Do tego asystenci prawdopodobnie powtarzają konsensus wydawców (hipoteza)"),
    (r"Co AI zrobi dobrze:", "Co AI prawdopodobnie zrobi dobrze (hipoteza):"),
    (r"Asystent zwykle porównuje raty, a nie koszt ekonomiczny: myli spłatę kapitału z kosztem i pomija koszt alternatywny equity\.",
     "Według agenta asystent zwykle porównuje raty, a nie koszt ekonomiczny: myli spłatę kapitału z kosztem i pomija koszt alternatywny equity (hipoteza; nie testowano)."),
    (r"Generatywne UI zwykle buduje jeden kalkulator na jeden wariant", "Generatywne UI prawdopodobnie buduje jeden kalkulator na jeden wariant (hipoteza)"),
    (r"Asystent policzy, ale założenia \(podatek, deprecjacja, LTV/APR\) będą zgadywane lub pominięte\.",
     "Asystent prawdopodobnie policzy, ale założenia (podatek, deprecjacja, LTV/APR) mogą być zgadywane lub pominięte (hipoteza)."),
    (r"Model AdSense wymaga długiej sesji \(interakcja z suwakami\) i odwiedzin powrotnych \(np\. 'sprawdź ponownie za 3 mies\.'\)\.",
     "W modelu AdSense przychód zależy od liczby odsłon z wyświetloną reklamą, a nie od długości sesji: AdSense rozlicza wyświetlenia, a polityki nie pozwalają "
     "odświeżać reklam bez działania użytkownika ani stawiać ich obok elementów interaktywnych [E-VER-C7, E-ADS-03]; pomóc mogą odwiedziny powrotne (np. 'sprawdź ponownie za 3 mies.')."),
    (r"Gdzie AI najczęściej się pomyli lub coś pominie:", "Gdzie AI prawdopodobnie się pomyli lub coś pominie (hipoteza; nie testowano):"),
    (r"choć Fed podniósł stopy we wrześniu 2026", "choć według streszczenia wyszukiwarki (primerates.com; niezweryfikowane) Fed podniósł stopy we wrześniu 2026"),
    (r"Fed podniósł stopy 16\.09\.2026, prime wynosi 7,00%\.",
     "Według streszczenia wyszukiwarki (primerates.com; niezweryfikowane) Fed podniósł stopy 16.09.2026, a prime wynosi 7,00%."),
    (r"Ryzyko dystrybucyjne jest wysokie: AI Overviews i AI Mode przejmą kliknięcia",
     "Ryzyko dystrybucyjne jest wysokie: AI Overviews i AI Mode prawdopodobnie przejmą kliknięcia (hipoteza)"),
    # rules#1 (pełne teksty kart ujawniły kolejne „brak …” o funkcjach na nieotwartych stronach): „nie widać w streszczeniu”, niezweryfikowane.
    (r"Brak kalkulatora oczekiwanego kosztu czekania \(grad × szkoda vs wymiana\)\.",
     "W streszczeniach nie widać kalkulatora oczekiwanego kosztu czekania (grad × szkoda vs wymiana; niezweryfikowane)."),
    (r"To brak kluczowych zależności, nie kosmetycznego pola\.",
     "W streszczeniach znalezionych narzędzi nie widać właśnie kluczowych zależności, a nie kosmetycznych pól (niezweryfikowane)."),
    (r"brak płatnej aplikacji łączącej termin, finansowanie i składkę",
     "'no single paid homeowner app' łączącej termin, finansowanie i składkę (stwierdzenia streszczeń; niezweryfikowane)"),
    (r"To ogólny kalkulator inwestora najmu: brak w nim step-up, wielu spadkobierców, wykupu i 121\.",
     "To ogólny kalkulator inwestora najmu; w streszczeniu nie widać w nim step-up, wielu spadkobierców, wykupu ani 121 (niezweryfikowane)."),
    (r"Kilka wyszukiwań wprost potwierdziło brak:",
     "Kilka streszczeń wyszukiwarki wprost stwierdziło brak (negatywne stwierdzenia ze streszczeń to słaby dowód; niezweryfikowane):"),
    (r"Dwa streszczenia wprost stwierdzają brak gotowych narzędzi:",
     "Dwa streszczenia wprost stwierdzają brak gotowych narzędzi (słaby dowód negatywny; niezweryfikowane):"),
    (r"Brak porównania wariantów\.", "W streszczeniu nie widać porównania wariantów (niezweryfikowane)."),
    (r"Brak personal loan, etapowania i sekwencji\.", "W streszczeniu nie widać personal loan, etapowania ani sekwencji (niezweryfikowane)."),
    (r"Brak interaktywnego modelu\.", "W streszczeniu nie widać interaktywnego modelu (niezweryfikowane)."),
    (r"Brak salda kredytu, więc nie ma negative equity\.",
     "W streszczeniu nie widać salda kredytu, więc prawdopodobnie nie liczy ujemnego kapitału (niezweryfikowane)."),
    # Kategorie konkurentów tylko: bezpośredni / częściowy / substytut / sporny (K10; bez kategorii pośrednich między „bezpośredni” a „częściowy”).
    (r"przeklasyfikować na probably_direct\.", "przeklasyfikować na „sporny (do ręcznej weryfikacji)” albo „bezpośredni”."),
    (r"klasyfikacja może wzrosnąć do probably_direct\.", "klasyfikacja może się zmienić na „sporny (do ręcznej weryfikacji)” albo „bezpośredni”."),
    (r"staje się bliski bezpośredniemu,", "staje się kandydatem na konkurenta bezpośredniego,"),
    # rules#14: ograniczeń polityk reklamowych dla kategorii nie sprawdzano.
    (r"\s*[–-]\s*wysokowartościowe wertykale bez ograniczeń kategorii wrażliwych\.", " – wysokowartościowe wertykale; " + ADPOL_SHORT + "."),
    (r"\s*[–-]\s*wysokowartościowe branże bez ograniczeń kategorii wrażliwych\.", " – wysokowartościowe branże; " + ADPOL_SHORT + "."),
    (r"\s*[–-]\s*najwyżej płatne wertykały, bez ograniczeń kategorii wrażliwych\.", " – najwyżej płatne wertykały; " + ADPOL_SHORT + "."),
    (r", bez ograniczeń kategorii wrażliwych\.", "; " + ADPOL_SHORT + "."),
    (r"Bez ograniczeń kategorii wrażliwych typowych dla zdrowia\.", ADPOL_SHORT_S + "."),
    (r"; brak ograniczeń kategorii wrażliwych dla AdSense w typowym rozumieniu\.", "; " + ADPOL_SHORT + "."),
    (r"Brak ograniczeń kategorii wrażliwych \(urządzenia medyczne są tylko kontekstem\)\.", ADPOL_SHORT_S + "."),
    (r"To nie kategoria wrażliwa w rozumieniu ograniczeń AdSense\.", ADPOL_SHORT_S + "."),
    (r"Treść nie jest kategorią wrażliwą dla wydawcy\.", ADPOL_SHORT_S + "."),
    (r"Brak kategorii wrażliw(?:ych|ej)\.", ADPOL_SHORT_S + "."),
    (r"Brak ograniczeń kategorii wrażliwych\.", ADPOL_SHORT_S + "."),
    (r"Kategoria nie jest wrażliwa\.", ADPOL_SHORT_S + "."),
    (r"; brak ograniczeń kategorii wrażliwych\.", "; " + ADPOL_SHORT + "."),
    # rules#2 / rules#13: liczba zdarzeń i podaż treści to nie popyt online.
    (r"Potwierdzają to treści ośrodków, prasa \(IBJ\) i świeże artykuły z 2026 r\.",
     "Opisują ją treści ośrodków, prasa (IBJ) i świeże artykuły z 2026 r. (podaż treści, sygnał pośredni, nie pomiar popytu)."),
    (r"i widoczna w pytaniach online; wiele firm buduje pod nią treści i narzędzia\.",
     "i widoczna w pytaniach online (anegdotycznie); wiele firm buduje pod nią treści i narzędzia (podaż treści, sygnał pośredni, nie pomiar popytu)."),
    (r"Widać silne inwestycje treściowe i narzędziowe dużych graczy i firm lead-gen\.",
     "Widać silne inwestycje treściowe i narzędziowe dużych graczy i firm lead-gen (podaż treści, sygnał pośredni, nie pomiar popytu)."),
    (r"co sprzyja szukaniu narzędzi\.", "co może sprzyjać szukaniu narzędzi (hipoteza)."),
    (r"Decyzja jest częsta w USA: ok\. 1,5 mln HELOC rocznie i ok\. 700 tys\. originations home equity kwartalnie\.",
     "Decyzja jest częsta w USA: ok. 1,5 mln HELOC rocznie i ok. 700 tys. originations home equity kwartalnie (liczba zdarzeń, nie popyt online)."),
    (r"Pokazuje realny popyt, ale w podsumowaniu", "To pojedyncze pytanie na forum (anegdotycznie, bez wolumenu; nie pomiar popytu), a w podsumowaniu"),
    (r"szacunkowo ok\. 2,4 mln zwrotów po leasingu w 2026", "szacunkowo ok. 2,4 mln zwrotów po leasingu w 2026 (liczba zdarzeń, nie popyt online)"),
    # --- Intelligent UI / AI Mode: fakt wydania potwierdzony (K10), nie „wg briefu” ---
    (r"ChatGPT Intelligent UI \(wg briefu od 2026-10-07, w tej sesji niezweryfikowane\)",
     "ChatGPT Intelligent UI (od 7–8.10.2026: plany płatne 7.10, Free/Go 8.10; potwierdzone w weryfikacji [E-VER-C2]; jakości w tej niszy nie testowano)"),
    (r"Google AI Mode z generatywnym UI \(wg briefu od 2026-08-19\)", AIM),
    (r"Według briefu \(dat nie weryfikowałem w tym badaniu\) ChatGPT Intelligent UI \(od 7\.10\.2026\) i generatywny UI w Google AI Mode \(od 19\.08\.2026\)",
     IUI + " i generatywny UI w Google AI Mode (od 19.08.2026 wg relacji SEJ [E-VER-C1])"),
    (r"Według briefu ChatGPT Intelligent UI \(od 7\.10\.2026\) i Google AI Mode z generatywnym UI \(od 19\.08\.2026\)", IUI + " i " + AIM),
    (r"Fakty o ChatGPT Intelligent UI \(7\.10\.2026\) i Google AI Mode generative UI \(19\.08\.2026\) pochodzą z briefu i nie były weryfikowane w tej sesji\.",
     "Daty ChatGPT Intelligent UI (7–8.10.2026) i generatywnego UI w Google AI Mode (19.08.2026) potwierdzono w weryfikacji [E-VER-C1, E-VER-C2]; zachowania asystentów w tej niszy nie testowano."),
    (r"funkcje ChatGPT 'Intelligent UI' \(od października 2026, kalkulatory renderowane w odpowiedzi\) i generatywnego UI w Google AI Mode przyjmuję za briefem\. W tym badaniu ich nie weryfikowałem i nie testowałem promptów\.",
     "funkcje ChatGPT 'Intelligent UI' (od 7–8.10.2026, kalkulatory renderowane w odpowiedzi) i generatywnego UI w Google AI Mode potwierdzono w weryfikacji [E-VER-C1, E-VER-C2]; promptów w tej niszy nie testowano."),
    (r"ChatGPT 'Intelligent UI' \(X 2026, według briefu; nie weryfikowałem w tej rundzie\)",
     "ChatGPT 'Intelligent UI' (od 7–8.10.2026; potwierdzone w weryfikacji [E-VER-C2])"),
    (r"ChatGPT z Intelligent UI \(wg briefu od 7\.10\.2026 renderuje kalkulatory w odpowiedzi\) i Google AI Mode z generative UI \(wg briefu od 19\.08\.2026\) wygenerują takie narzędzie ad hoc\. Daty tych funkcji pochodzą z briefu i nie były weryfikowane w tym przebiegu\.",
     "ChatGPT z Intelligent UI (od 7–8.10.2026 renderuje kalkulatory w odpowiedzi; potwierdzone w weryfikacji [E-VER-C2]) i Google AI Mode z generative UI (od 19.08.2026 wg relacji SEJ [E-VER-C1]) prawdopodobnie wygenerują takie narzędzie ad hoc (hipoteza; nie testowano)."),
    (r"potrafią wyrenderować formularz lub kalkulator \(wg briefu\)", "potrafią wyrenderować formularz lub kalkulator (" + VER + ")"),
    (r"Brief: ChatGPT Intelligent UI \(od 7\.10\.2026\) i Google AI Mode \(od 19\.08\.2026\)\.",
     "ChatGPT Intelligent UI (od 7–8.10.2026) i Google AI Mode (od 19.08.2026): " + VER + "."),
    (r"Brief: (ChatGPT Intelligent UI i Google AI Mode [^.]*)\.", r"\1 (" + VER + ")."),
    (r"Kontekst zadania \(ChatGPT Intelligent UI, Google AI Mode generujący narzędzia\)",
     "Wydanie ChatGPT Intelligent UI i narzędzi generatywnych w Google AI Mode (potwierdzone w weryfikacji [E-VER-C1, E-VER-C2])"),
    (r"kontekst zadania o Intelligent UI \(7\.10\.2026\) i AI Mode \(19\.08\.2026\)",
     "wydanie Intelligent UI (7–8.10.2026) i narzędzi AI Mode (19.08.2026) potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]"),
    (r"Funkcje Intelligent UI i AI Mode z kontekstu zadania", "Wydanie Intelligent UI i narzędzi AI Mode potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]"),
    (r"Opis możliwości ChatGPT i AI Mode z kontekstu zadania\.",
     "Wydanie Intelligent UI i narzędzi AI Mode potwierdzone w weryfikacji [E-VER-C1, E-VER-C2]; zachowania w tej niszy nie testowano."),
    (r"[Kk]ontekst zadania: (ChatGPT Intelligent UI[^.]*)\.", r"\1 (" + VER + ")."),
    (r"Według kontekstu zadania (ChatGPT Intelligent UI[^.]*)\.", r"\1 (" + VER + ")."),
    (r"; kontekst (ChatGPT Intelligent UI \(7\.10\.2026\) i Google AI Mode \(19\.08\.2026\))\.", r"; \1: " + VER + "."),
    (r"[Kk]ontekst: (ChatGPT Intelligent UI i Google AI Mode [^;.]*)", r"\1 (" + VER + ")"),
    (r"\s+według kontekstu zadania\.", ": " + VER + "."),
    (r"\((?:wg|według) kontekstu zadania\)", "(" + VER + ")"),
    (r"\(kontekst zadania\)", "(" + VER + ")"),
    # --- obserwacja generatora streszczeń WebSearch to nie test asystenta ---
    (r"Dowód z tej sesji:", "Obserwacja pośrednia (hipoteza; to nie test asystenta, tylko generator streszczeń narzędzia WebSearch):"),
    (r"pięć niezależnych podsumowań wyszukiwarki", "pięć podsumowań wyszukiwarki (z tego samego narzędzia)"),
    # --- RENO-02: brak funkcji na nieotwartych stronach = „niezweryfikowane” (recenzja spójności, rules#1) ---
    (r"Jedyne znalezione narzędzie konsumenckie łączące wiek dachu z ubezpieczeniem\.",
     "Łączy wiek dachu z szacunkiem oszczędności na składce (wg streszczenia; niezweryfikowane); fala 2b znalazła też InsuranceCostCity i RoofingCalculatorUSA."),
    (r"Luka: brak konsumenckiego modelu", "W badanym zakresie nie znaleziono konsumenckiego modelu"),
    (r"Brak szablonu NPV dla terminu wymiany dachu\.", "W streszczeniach nie widać szablonu NPV dla terminu wymiany dachu (niezweryfikowane)."),
    (r"Brak aplikacji łączącej pozostałą żywotność dachu ze składką\.",
     "W streszczeniach nie widać modelu łączącego pozostałą żywotność dachu ze składką w czasie (fragmenty pokrywają RoofTap, InsuranceCostCity i RoofingCalculatorUSA — do ręcznej weryfikacji)."),
    (r"Brak kalkulatora kredytu dla kupującego vs wymiana", "W streszczeniach nie widać kalkulatora kredytu dla kupującego vs wymiana (niezweryfikowane)"),
    # --- podaż treści ≠ popyt (rules#3) ---
    (r"Wskazuje to na stały ruch wyszukiwań, wartościowy dla lead-gen",
     "To podaż treści i kalkulatorów — sygnał pośredni (wydawcy uważają temat za opłacalny dla lead-genu), nie pomiar popytu ani ruchu"),
    (r"Sugeruje stały popyt w wyszukiwarce\.", "To podaż treści (sygnał pośredni), nie pomiar popytu."),
    (r"wskazuje na stały popyt informacyjny w momencie decyzji", "to podaż treści w momencie decyzji (sygnał pośredni, nie pomiar popytu)"),
    (r"temat ma stały popyt informacy\w*", "to podaż treści (sygnał pośredni, nie pomiar popytu)"),
    (r"Wysoki popyt tematyczny \(pośrednio z liczby narzędzi\)", "Duża podaż narzędzi (sygnał pośredni, nie pomiar popytu)"),
    # --- formuła konkurencji (K10) ---
    (r"Nie znaleziono bezpośredniego konkurenta(?! w badanym zakresie)", "Nie znaleziono bezpośredniego konkurenta w badanym zakresie"),
    # --- podaż treści ≠ popyt (K10) ---
    (r"co wskazuje na widoczny popyt pytań online", "to podaż treści (sygnał pośredni), nie pomiar popytu"),
    (r"co wskazuje na widoczny popyt na pytania", "to podaż treści (sygnał pośredni), nie pomiar popytu"),
    (r"wskazuje na realny popyt na pytania", "to podaż treści (sygnał pośredni), nie pomiar popytu"),
    (r"widoczny popyt na pytania online \(fora, poradniki wykonawców, wysyp kalkulatorów 2026, lead-gen\)",
     "pojedyncze pytania na forach (anegdotycznie) oraz podaż poradników wykonawców, kalkulatorów 2026 i lead-genu (sygnał pośredni, nie pomiar popytu)"),
    (r"Widoczny popyt na pytania: ", "Widoczna podaż treści (sygnał pośredni, nie pomiar popytu): "),
    (r"widoczny popyt pytaniowy \(", "widoczna podaż treści, czyli sygnał pośredni, a nie pomiar popytu ("),
    (r"ma widoczny popyt treściowy", "ma widoczną podaż treści (sygnał pośredni)"),
    (r"widoczny popyt na treści i kalkulatory", "widoczna podaż treści i kalkulatorów (sygnał pośredni)"),
    (r"Widoczny jest popyt na pytania \(", "Widoczne są pytania i podaż treści (sygnał pośredni; "),
    (r"Widać silny popyt na fragmenty", "Widać dużą podaż treści o fragmentach (sygnał pośredni, nie pomiar popytu)"),
    (r"dużo treści targetuje pokrewne frazy\.", "dużo treści targetuje pokrewne frazy (podaż treści, nie pomiar popytu)."),
    (r"co sugeruje widoczny popyt wyszukiw\w*", "co jest podażą treści (sygnał pośredni), nie pomiarem popytu"),
    (r"solidny popyt", "popyt niezmierzony (hipoteza)"),
    # --- wyniki narzędzia WebSearch to nie SERP Google (K-05) ---
    (r"SERP jest zdominowany przez", "w wynikach WebSearch dominują (SERP Google niezweryfikowany, K-05)"),
    (r"SERP zdominowany przez", "wyniki WebSearch zdominowane (SERP Google niezweryfikowany, K-05) przez"),
    (r"SERP jest zatłoczony", "wyniki WebSearch są zatłoczone (SERP Google niezweryfikowany, K-05)"),
    (r"\bw SERP\b", "w wynikach WebSearch (SERP Google niezweryfikowany, K-05)"),
    # --- reklama: wyniki organiczne to nie gęstość reklamodawców ---
    (r"\s*[–-] gęstość reklamodawców\.", " (wyniki organiczne; gęstość reklamodawców w aukcjach to hipoteza)."),
    # --- Edmunds: zawsze z kwartałem i statusem weryfikacji (K10) ---
    (r"Edmunds za Q3 2026:",
     "Edmunds za Q3 2026 (wg agenta, jedno źródło; w weryfikacji fali 3 potwierdzono ostatnio Q2 2026: 29,6% i 6 884 USD [E-REV-07]):"),
]
SUBS = [(re.compile(p), r) for p, r in SUBS]


def fix(s):
    s = ' '.join(str(s).split())
    for p, r in SUBS:
        s = p.sub(r, s)
    return s


def one(s, n=None):
    """Tekst agenta po poprawkach słownictwa (fix). Runda 2 kontroli spójności: karty i tabele kryteriów
    pokazują pełne brzmienie (n=None); limit n zostaje tylko jako opcja i wtedy dopisuje „…”."""
    s = fix(s)
    if n is None or len(s) <= n:
        return s
    return s[:n].rsplit(' ', 1)[0] + ' …'


def cell(s, n=None):
    return one(s, n).replace('|', '/')


def misses(s, n=None):
    """Kolumna „W search-summary nie widać / niezweryfikowane”: funkcji niewidocznych w streszczeniu nie nazywamy „brakiem”."""
    s = fix(s)
    s = re.sub(r'\bBrak\b(?! (?:testu|danych|audytowalnych))', 'Nie widać', s)
    s = re.sub(r'\bbrak\b(?! (?:testu|danych|audytowalnych))', 'nie widać', s)
    out = cell(s, n)
    if 'niezweryfik' not in out.lower():
        out += ' (niezweryfikowane)'
    return out


def load(p):
    return json.load(open(p)) if os.path.exists(p) else None


def products_csv():
    return {r['ID']: r for r in csv.DictReader(open(CSV_PRODUCTS))}


def status_text(row):
    st = row['status']
    return st + (f" — {row['uwaga_statusu']}" if row.get('uwaga_statusu') else '')


def criteria_rows(a, c, n_r=None, n_e=None, n_g=None):
    """Wiersze tabeli 7 kryteriów (ocena, uzasadnienie, dowody, luki, pewność) z audytu i kalibracji.
    Runda 2 kontroli spójności: domyślnie pełne brzmienie komórek (bez ucinania)."""
    rows = []
    for k, label, w in W:
        s = a['scores'][k]
        adj = c.get('adj', {}).get(k)
        sc = f"{s['score']}" + (f" → **{adj}**" if adj is not None else '')
        conf = LV[s['confidence']]
        gaps = s['gaps_pl']
        rationale = str(s['rationale_pl'])
        if k == 'ai_distribution':
            rationale = AI_PREFIX + rationale
        if k in LOW_CAP:
            if conf != 'niska':
                conf = f"niska (audytor: {conf})"
            gaps = LOW_CAP[k] + ' ' + str(gaps)
        n_gap = None if n_g is None else (n_g + 140 if k in LOW_CAP else n_g)
        rows.append(f"| {label} ({w}%) | {sc} | {cell(rationale, n_r)} | {cell(s['evidence_pl'], n_e)} | {cell(gaps, n_gap)} | {conf} |")
    return rows


# Dwie osie etykiet dowodów popytu z fali 2b (recenzja fali 3, uwaga 4): siła źródła i co źródło mierzy.
# Klucz: indeks w demand_evidence. Wartość: (siła, co mierzy, powód obniżenia siły lub '').
P, Z, M, T, A = ('pytania zadawane online (anegdotycznie, bez wolumenu)', 'zdarzenia, wyzwalacze lub populacja (nie popyt online)',
                 'parametr modelu lub reguła (nie popyt)', 'podaż treści (nie popyt)', 'deklaracje w ankiecie (nie popyt online)')
B, PO, E, H = 'bezpośrednie', 'pośrednie', 'estymacja', 'hipoteza'
AXES = {
    'RENO-02': [(E, Z, ''), (PO, M, 'źródło wtórne o raporcie Verisk'), (PO, M, 'źródło wtórne o danych Verisk'), (PO, T, ''), (PO, M, ''), (PO, T, '')],
    'RENO-03': [(PO, Z, 'dane AHRI ze źródła wtórnego'), (E, Z, ''), (PO, Z, ''), (PO, M, ''), (B, P, ''), (B, P, '')],
    'RENO-04': [(PO, Z, ''), (E, Z, ''), (PO, M, ''), (PO, Z, ''), (PO, M, ''), (PO, M, '')],
    # HOME-02[0]: agent zastrzega, że przypisanie liczb do wątku jest niepewne → pośrednie (legenda §1.2; citations#13).
    'HOME-02': [(PO, P, 'niepewne przypisanie liczb do wątku'), (B, P, ''), (PO, P, ''), (PO, Z, ''), (PO, M, ''), (PO, Z, '')],
    'LIFE-01': [(B, Z, ''), (PO, T, ''), (PO, Z, 'źródło wtórne'), (PO, A, 'komunikat PR, próba prawdopodobnie samoselekcyjna'), (E, A, ''), (PO, T, '')],
    'HOME-04': [(PO, Z, ''), (PO, Z, ''), (PO, Z, ''), (PO, A, ''), (PO, A, ''), (PO, A, '')],
    'INS-03': [(PO, Z, ''), (PO, Z, ''), (E, Z, ''), (PO, Z, ''), (PO, Z, ''), (PO, M, '')],
    'CARE-01': [(PO, A, ''), (H, Z, ''), (PO, M, ''), (E, M, ''), (PO, Z, ''), (PO, Z, '')],
    'AUTO-01': [(PO, Z, ''), (PO, Z, ''), (PO, Z + '; ' + T, ''), (PO, T, ''), (PO, M, ''), (PO, Z, '')],
    'FIN-01': [(B, Z, ''), (B, Z, ''), (B, Z, ''), (PO, Z, 'przypisanie do URL niepewne'), (PO, Z, 'przypisanie do URL niepewne'), (E, Z, '')],
}


def demand_label(fid, i, e):
    ax = AXES.get(fid, [])
    if i < len(ax):
        sila, mierzy, why = ax[i]
    else:
        sila, mierzy, why = KIND[e['kind']], 'nieprzypisane', ''
    if why and KIND[e['kind']] != sila:
        sila = f"{sila} (obniżone z „{KIND[e['kind']]}”: {why})"
    return f"[siła źródła: {sila} · mierzy: {mierzy}]"


# Przykłady pytań z fali 2b (forum_question_examples) według tego, czym naprawdę są (recenzja spójności, rules#13).
# F = pytanie użytkownika na forum lub w serwisie Q&A społeczności; R = pytanie czytelnika w rubryce wydawcy (dobór redakcji);
# W = nagłówek strony wydawcy, wykonawcy lub kredytodawcy w formie pytania albo artykuł (podaż treści, sygnał pośredni).
FORUM_KIND = {
    'RENO-02': 'WWWWWWWW', 'RENO-03': 'FFFFF', 'RENO-04': 'FFF', 'HOME-02': 'FFFFFFF', 'LIFE-01': 'FWWWWWW',
    'HOME-04': 'FFRRR', 'INS-03': 'FFFFFW', 'CARE-01': 'R', 'AUTO-01': 'FF', 'FIN-01': 'WWW',
}
FORUM_TAG = {'F': 'pytanie użytkownika (forum lub Q&A społeczności)', 'R': 'pytanie czytelnika w rubryce wydawcy',
             'W': 'nagłówek strony wydawcy lub firmy w formie pytania (podaż treści)'}


def forum_counts(fid, n):
    kinds = FORUM_KIND.get(fid, '')
    assert len(kinds) == n, (fid, len(kinds), n)
    return kinds.count('F'), kinds.count('R'), kinds.count('W')


# Lista do ręcznej weryfikacji RENO-02 (G0 krok 4; kanon K5; recenzja spójności completeness#2).
# Pięć kluczowych zależności z reguły odpadnięcia (≥ 3 w jednym narzędziu): ACV/RCV lub harmonogram wypłat za dach; udział własny
# wiatr/grad; horyzont sprzedaży; demontaż i ponowny montaż PV; finansowanie. Przypisania wyłącznie na podstawie streszczeń
# wyszukiwarki z audytu fali 2, próby obalenia fali 2b i (grupa D) wierszy fali 1 w competitor-audit.csv — niezweryfikowane.
# Pola: (priorytet, pełna nazwa, adresy, może pokrywać z 5, inne elementy spoza 5, co sprawdzić ręcznie).
VERIFY_RENO02 = [
    ('A. Narzędzia częściowe z próby obalenia (fala 2b)', [
        ('1', 'Kalkulatory Roof ROI: Weathershield Roofers – Roofing ROI Calculator 2026; CalculateMyRoof – Roof ROI Calculator; ShinglesCalculator – Roof ROI Calculator (Resale Value & Energy Savings)',
         ['https://weathershieldroofers.com/roofing-roi-calculator/', 'https://calculatemyroof.com/calculator/roof-roi-calculator/', 'https://shinglescalculator.com/calculators/roof-roi-calculator/'],
         'horyzont sprzedaży — możliwe (wartość domu i oszczędności w horyzoncie 5–20 lat; czy data sprzedaży jest zmienną, niejasne)',
         'wiek dachu → składka; zwrot z oszczędności na ubezpieczeniu',
         'pole „years until sale”; warianty (wymiana teraz, naprawa i czekanie, sprzedaż as-is z kredytem); ACV/RCV i udział wiatr/grad; finansowanie i PV'),
        ('1', 'RoofingCalculatorUSA – Roof Insurance Deductible Calculator 2026 oraz New Roof Insurance Premium Savings Calculator',
         ['https://roofingcalculatorusa.com/calculators/roof-insurance-deductible'],
         'udział własny w szkodach dachowych — możliwe (czy procentowy wiatr/grad, niejasne)',
         'spadek składki po nowym dachu i lata do zwrotu (osobny kalkulator)',
         'czy kalkulatory mają wspólne dane wejściowe; wariant „wait” lub horyzont sprzedaży; czy udział własny trafia do oczekiwanego kosztu'),
        ('1', 'Roof Decision Guide – Roof Decision Tools and Calculators (hub)', ['https://roofdecisionguide.com/tools/'],
         'nieznane — hub z wieloma narzędziami; sprawdzić wszystkie 5',
         'kalkulator naprawa vs wymiana (wiek, stan, uszkodzenia)',
         'lista narzędzi w hubie; czy ubezpieczenie, sprzedaż, PV i finansowanie dzielą dane wejściowe'),
        ('2', 'InsuranceCostCity – Roof Age & Insurance Cost Calculator', ['https://www.insurancecostcity.com/tools/roof-age-calculator'],
         'nie widać żadnej wprost (w streszczeniu tylko tytuł)', 'wiek dachu → składka',
         'rekomendacja wymiany lub okres zwrotu; ACV i nieodnowienie polisy; region (grad/wiatr)'),
        ('2', 'Kalkulatory szkód gradowych: ShinglesCalculator – Hail Damage Calculator; RoofingCalculatorHQ – Hail Damage Assessment Calculator',
         ['https://shinglescalculator.com/calculators/hail-damage-calculator/', 'https://www.roofingcalculatorhq.com/calculators/hail-damage-assessment-calculator/'],
         'nie widać żadnej wprost (ocena szkody gradowej, która już wystąpiła)', 'procent uszkodzeń wg wielkości gradu, wieku i materiału; próg naprawa vs wymiana',
         'czy liczą roczne prawdopodobieństwo gradu albo ACV vs RCV przy przyszłej szkodzie'),
        ('2', 'BuildFolio – Should I Repair or Replace My Roof? Free Tool', ['https://build-folio.com/repair-or-replace-roof/'],
         'nie widać żadnej w streszczeniu', 'rekomendacja naprawa/wymiana i koszt na podstawie zdjęć satelitarnych',
         'pytania o ubezpieczyciela (ACV/RCV, dopłaty) i plan sprzedaży; wynik w czasie; czy to tylko lead-gen'),
        ('3', 'Hammerio – Replace vs Repair Calculator 2026: 5-Year TCO & 50% Rule', ['https://hammerio.com/tools/replace-vs-repair-decision-calculator-2026/'],
         'nie widać żadnej w streszczeniu (prawdopodobnie narzędzie ogólne, nie dachowe)', '5-letni TCO, reguła 50%',
         'tryb dla dachu; horyzont dłuższy niż 5 lat; ubezpieczenie i sprzedaż'),
        ('3', 'Paperform – Roof Replacement Financing Calculator (template)', ['https://paperform.co/templates/roof-replacement-financing-calculator/'],
         'finansowanie — możliwe (raty i plan płatności)', '—', 'czy szablon ma pola ubezpieczenia albo sprzedaży'),
    ]),
    ('B. Narzędzia częściowe z audytu fali 2', [
        ('1', 'RoofTap – Free Roof Cost Estimate / homeowner roof report', ['https://www.rooftap.app/homeowner/roof-report'],
         'finansowanie — niejasne', 'wiek i stan dachu, 3-letnia prognoza wymiany, szacunek oszczędności na składce',
         'warianty (naprawa, czekanie, sprzedaż as-is z kredytem); ACV i oczekiwana strata; horyzont sprzedaży (agent audytu: największe ryzyko błędnej klasyfikacji)'),
        ('2', 'SubcontractorHub – Roof Repair vs. Replacement Calculator', ['https://www.subcontractorhub.com/tools/roof-repair-vs-replacement-calculator'],
         'nie widać żadnej w streszczeniu', 'koszt roczny naprawy vs wymiany, reguła 50%, pozostała żywotność (wariant „naprawa i czekanie”)',
         'pola polisy, horyzontu sprzedaży i finansowania'),
        ('2', 'RoofQuote (roofquotes.app) – AI estimates for contractors', ['https://roofquotes.app/'],
         'nie widać żadnej w streszczeniu', 'obniżki składki dla FORTIFIED Roof/Silver/Gold, 5-letnia projekcja, granty stanowe (narzędzie dla dekarzy)',
         'dostęp konsumencki; ACV/RCV; horyzont sprzedaży'),
        ('3', 'Roof Decision Guide – Repair vs Replace Calculator', ['https://roofdecisionguide.com/repair-vs-replace/calculator/'],
         'nie widać żadnej w streszczeniu', 'wynik 0–100 i widełki kosztu naprawy i wymiany', 'sprawdzić razem z hubem Roof Decision Guide (grupa A)'),
        ('3', 'Kalkulatory kosztu wymiany dachu: TheRooferFinder, RoofPitch, CostFlow AI, RoofQuotes.com, Calculator.net, Roof-Smith',
         ['https://www.therooferfinder.com/roof-cost-calculator', 'https://roofpitch.net/roof-replacement-cost-calculator/', 'https://costflowai.com/calculators/roofing/',
          'https://roofquotes.com/roofing-calculator', 'https://www.calculator.net/roofing-calculator.html', 'https://www.roof-smith.com/calculator'],
         'nie widać żadnej (jednorazowy koszt wymiany)', 'koszt wymiany wg powierzchni, materiału, nachylenia i lokalizacji', 'wystarczy przegląd pobieżny'),
        ('3', 'ServiceAgent.ai – Roof Repair Cost Estimator', ['https://serviceagent.ai/tools/roof-repair-cost-calculator/'],
         'nie widać żadnej (koszt naprawy)', 'koszt naprawy; w FAQ: przy ponad ok. 30% uszkodzeń zwykle wymiana', 'wystarczy przegląd pobieżny'),
    ]),
    ('C. Substytuty (treści, dane, doradcy) z audytu fali 2 i próby obalenia fali 2b — sprawdzić tylko, czy nie mają wbudowanego kalkulatora', [
        ('3', 'ValuePenguin – Does Home Insurance Cover a New Roof? (fala 2)', ['https://www.valuepenguin.com/homeowners-insurance/roof-insurance'],
         'nie widać żadnej (treść)', 'dane: składka wg wieku dachu', 'metodologia tabeli'),
        ('3', 'Treści o ACV vs RCV i harmonogramach wypłat: Real Cost Report, Fit Roofing, Better Choice Insurance, Weathershield Roofers, Yahoo Finance, Bankrate, Policygenius (fala 2)',
         ['https://www.realcostreport.com/insurance/home-insurance/replacement-cost-vs-acv/'],
         'ACV/RCV — opisane w treści (wzory, przykłady), bez narzędzia', 'harmonogram wypłat wg wieku dachu (jedno źródło)', 'czy któraś strona ma kalkulator'),
        ('3', 'Poradniki „replace roof before selling”: Zillow, ibuyer.com, RoofVista, Best Roofing Now, Tour Wizard (fala 2)',
         ['https://www.zillow.com/learn/should-i-replace-my-roof-before-selling/'],
         'horyzont sprzedaży — opisany w treści (zwrot w cenie, kredyt przy zamknięciu), bez narzędzia', 'jeden serwis ma tabelę „net cost after ROI” (który — niejasne)',
         'który serwis ma tabelę i czy to kalkulator'),
        ('3', 'Treści o PV a wymianie dachu: ConsumerAffairs, Solar Panel Exit, The Roofing Brief, SquareDash, SolarFY, Forme Solar (fala 2)',
         ['https://www.consumeraffairs.com/solar-energy/should-you-replace-your-roof-before-going-solar.html'],
         'demontaż i ponowny montaż PV — opisany w treści (koszty), bez narzędzia', 'reguły pozostałej żywotności dachu przed PV', 'czy któraś strona ma kalkulator'),
        ('3', 'Planery budżetu i finansowanie dachu: RIBA Roofing planner, HomeRun PACE, PrimeRates (fala 2)', ['https://ribaconstruction.com/how-homeowners-budget-for-a-new-roof/'],
         'finansowanie — możliwe (planer oszczędzania, PACE, pożyczki)', '—', 'czy jest porównanie wariantów'),
        ('—', 'Asystenci AI: ChatGPT Intelligent UI, Google AI Mode z generowanymi narzędziami (fala 2)', [],
         'nie dotyczy kroku 4 (to nie strona)', '—', 'pomiar w G0, krok 5 (panel promptów)'),
        ('—', 'Agent ubezpieczeniowy, dekarz, agent nieruchomości (fala 2)', [], 'nie dotyczy (to nie narzędzie)', '—', '—'),
        ('3', 'CostPrism / RealCostIQ – roof repair vs replacement 2026 guides (fala 2b)', ['https://costprism.com/guides/roof-repair-vs-replacement/', 'https://realcostiq.com/guides/roof-repair-vs-replacement/'],
         'nie widać żadnej (treść: 20-letni scenariusz „wymiana teraz vs czekanie”)', '—', 'czy jest wbudowany kalkulator replace-now vs wait z ubezpieczeniem'),
        ('3', 'Oxmaint – Property CapEx Request Template (NPV repair vs replace) (fala 2b)', ['https://oxmaint.com/industries/property-management/property-capex-request-template-building-owners'],
         'nie widać żadnej (szablon B2B)', 'NPV: dalsze naprawy vs wymiana 1:1 vs wymiana z ulepszeniem', 'czy to plik z formułami'),
        ('3', 'Poradniki dla sprzedających: Opendoor, Best Utah Real Estate, ListWithClever, Fixr (fala 2b)',
         ['https://bestutahrealestate.com/news/roof-condition-and-home-sales-replace-repair-or-credit', 'https://www.opendoor.com/articles/does-a-new-roof-increase-home-value-roi-costs-and-what-sellers-need-to-know'],
         'horyzont sprzedaży — opisany w treści (kredyt przy zamknięciu vs wymiana), bez narzędzia', 'wymóg FHA: min. 2 lata pozostałej żywotności dachu',
         'czy Opendoor lub ListWithClever mają kalkulator net proceeds z opcją dachu'),
        ('3', 'Poradniki o kolejności dach + PV: EnergySage, Griffith Roofing, RoofVista, Roofmaxx, DOE (fala 2b)', ['https://www.energysage.com/solar/solar-panel-roof-replacement/'],
         'demontaż i ponowny montaż PV — opisany w treści, bez narzędzia', '—', 'czy EnergySage ma kalkulator „roof + solar” z horyzontem sprzedaży'),
        ('3', 'MyTidyBoss – Home Maintenance Cost Calculator (fala 2b)', ['https://mytidyboss.com/tools/maintenance-budget-calculator/'],
         'nie widać żadnej', 'budżet utrzymania domu (żywotność dachu 20–30 lat)', '—'),
        ('3', 'ValuePenguin – Can Renovating Your House Lower Your Insurance Costs? (fala 2b)', ['https://www.valuepenguin.com/home-renovation-insurance-savings'],
         'nie widać żadnej (źródło danych)', 'oszczędność na składce po wymianie dachu', '—'),
    ]),
    ('D. Uzupełnienie z fali 1 (narzędzia częściowe z competitor-audit.csv, które w opisie dotykają kluczowych zależności; opisy krótsze i mniej pewne)', [
        ('1', 'Shingles Calculator – Roof Depreciation, ACV & Replacement Planning', ['https://shinglescalculator.com/calculators/roof-depreciation-calculator/'],
         'ACV/RCV — możliwe; horyzont pozostania w domu — możliwy (przypisanie niepewne)', 'planowanie wymiany',
         'czy próg naprawa vs wymiana uwzględnia horyzont sprzedaży, udział własny wiatr/grad i finansowanie'),
        ('2', 'SubcontractorHub Roof Insurance Claim Calculator', ['https://www.subcontractorhub.com/tools/roof-insurance-claim-calculator'],
         'ACV/RCV lub udział własny — możliwe (w opisie tylko „szacunek roszczenia”)', '—', 'jakie pola polisy ma kalkulator'),
        ('2', 'RateMyPolicy Roof ACV vs RCV Calculator', ['https://ratemypolicy.com/roof-acv-vs-rcv-calculator'], 'ACV/RCV — możliwe', '—',
         'czy łączy ACV z wiekiem dachu, udziałem własnym i terminem wymiany'),
        ('2', 'Teamzlab RCV vs ACV coverage calculator', ['https://tool.teamzlab.com/insurance/homeowners-replacement-cost-vs-acv-calculator/'], 'ACV/RCV — możliwe', '—',
         'jak wyżej'),
        ('2', 'Replace Roof Before Selling? The Math', ['https://www.ownluxuryhomes.com/markets/national/roof-replacement-cost/when-to-replace-roof-before-selling'],
         'horyzont sprzedaży — możliwe (rachunek wymiany przed sprzedażą, wg tytułu)', 'adres należy do innego podmiotu niż nazwa', 'czy to kalkulator, czy artykuł'),
        ('2', 'Solar Roofing Calculator (roofcalc.org)', ['https://www.roofcalc.org/solar-roofing-calculator'],
         'PV — możliwe (łączny koszt dachu i PV; czy obejmuje demontaż i ponowny montaż, niejasne)', 'ulga 30% prawdopodobnie nieaktualna po 2025',
         'czy jest wariant terminu wymiany i horyzont sprzedaży'),
        ('3', 'Solar Before Selling Home Calculator (solarsizecalculator.com)', ['https://solarsizecalculator.com/solar-before-selling-home-calculator/'],
         'horyzont sprzedaży — możliwe, ale dla PV (rok sprzedaży, premia wartości domu), nie dla dachu', '—', 'czy uwzględnia stan dachu'),
        ('3', 'RoofingCalculator – roof replacement insurance guide', ['https://roofingcalculator.com/roof-replacement-insurance-guide'],
         'nie widać żadnej (treść)', 'oszczędności na składce po nowym dachu wg stanu', '—'),
    ]),
]


def verify_list_reno02():
    n = {g: len(rows) for g, rows in VERIFY_RENO02}
    out = ['**Lista do ręcznej weryfikacji (G0 krok 4).** Wszyscy kandydaci z audytu fali 2 i próby obalenia fali 2b '
           f"({sum(n.values()) - len(VERIFY_RENO02[3][1])} pozycji: 8 częściowych z fali 2b, 6 częściowych z audytu fali 2, 13 substytutów), "
           f"a do tego {len(VERIFY_RENO02[3][1])} narzędzi częściowych z fali 1 jako uzupełnienie. "
           'Reguła bramki (propozycja decyzyjna): RENO-02 odpada, jeśli jedno narzędzie pokrywa ≥ 3 z 5 kluczowych zależności: '
           '(1) ACV/RCV lub harmonogram wypłat za dach, (2) udział własny wiatr/grad, (3) horyzont sprzedaży, (4) demontaż i ponowny montaż PV, (5) finansowanie. '
           'Kolumna „Może pokrywać” opiera się wyłącznie na streszczeniach wyszukiwarki (strony nieotwierane), więc jest **niezweryfikowana**: '
           '„nie widać” znaczy „w streszczeniu nie widać”, a nie „narzędzie tego nie ma”. Priorytet: 1 = sprawdzić najpierw '
           '(łączy kilka elementów albo zakres jest nieznany), 2 = jeden kluczowy element, 3 = narzędzie jednocelowe lub treść. '
           'Szczegóły kandydatów: tabela konkurencji wyżej i `competitor-audit.csv` (filtr `produkt_ID_final` = RENO-02).\n']
    for group, rows in VERIFY_RENO02:
        out.append(f"*{group}:*\n")
        out.append('| Prio. | Kandydat (pełna nazwa) | Może pokrywać z 5 kluczowych zależności (wg streszczeń; niezweryfikowane) | Inne elementy (spoza 5) | Co sprawdzić ręcznie |')
        out.append('|---|---|---|---|---|')
        for prio, name, urls, cover, other, check in rows:
            links = ' '.join(f"[{i}]({u})" for i, u in enumerate(urls, 1)) if urls else 'n/d'
            label = 'adresy: ' if len(urls) > 1 else 'adres: '
            out.append(f"| {prio} | {name.replace('|', '/')} ({label}{links}) | {cover} | {other} | {check} |")
        out.append('')
    out.append('Wniosek ze streszczeń (niezweryfikowany): w streszczeniach widać najwyżej jedną z pięciu kluczowych zależności na narzędzie; '
               'tylko opis Shingles Calculator – Roof Depreciation (fala 1) sugeruje dwie (ACV i horyzont pozostania w domu, przypisanie niepewne). '
               'Przy kilku narzędziach zakres jest niejasny (hub Roof Decision Guide, kalkulatory Roof ROI, RoofTap, Shingles Calculator – Roof Depreciation, '
               'SubcontractorHub Roof Insurance Claim Calculator), więc mogą pokrywać więcej. Rozstrzyga dopiero otwarcie stron i test formularzy (K-03). '
               'Brak takiego narzędzia w streszczeniach nie dowodzi, że go nie ma.\n')
    return out


# Klasyfikacje sporne i znalezieni konkurenci bezpośredni (kanon K10).
COMPETITOR_OVERRIDE = {
    'RET-03': ('Znaleziono konkurentów bezpośrednich: RothHelper i QuantCalc ACA Bridge Optimizer realizują rdzeń decyzji '
               '(audyt fali 2: 7 zapytań WebSearch; search-summary, strony nieotwierane; pewność: średnia)'),
    'RENT-01': ('Sporny, do ręcznej weryfikacji. BiggerPockets Sell vs Keep jest konkurentem bezpośrednim dla rdzenia hold/sell z seeda H '
                '(search-summary, pewność średnia), ale w jego opisie z fali 1 (proformy 5/10/20+ lat) nie widać pozostałych wariantów RENT-01: 1031, step-up, sprzedaży ratalnej (niezweryfikowane). '
                'OverlineIQ Keep vs. Sell a Rental: w fali 1 bezpośredni, w fali 2 częściowy. Audyt fali 2: 7 zapytań WebSearch, anglojęzyczny web USA, '
                '2026-10-25, wyłącznie streszczenia wyszukiwarki, strony nieotwierane'),
    'ENER-03': ('Sporny, do ręcznej weryfikacji: Home Energy Planner (Backup Power Calculator) — w fali 1 bezpośredni, w fali 2 częściowy. '
                'Audyt fali 2: 7 zapytań WebSearch, anglojęzyczny web USA, 2026-10-25, wyłącznie streszczenia wyszukiwarki, strony nieotwierane'),
}


def dec(x):
    return f"{x:.2f}".replace('.', ',')


def competitor_line(row):
    """Formuła z kanonu K10: „Nie znaleziono bezpośredniego konkurenta w badanym zakresie” + zakres + pewność."""
    if row['ID'] in COMPETITOR_OVERRIDE:
        return COMPETITOR_OVERRIDE[row['ID']]
    v = row['bezposredni_konkurent (top 25)']
    if not v.startswith('Nie znaleziono'):
        return v
    m = re.search(r'pewność ([^)]*)\)', v)
    conf = m.group(1) if m else 'niska–średnia'
    q = '7 zapytań WebSearch w audycie fali 2' + (' + 8 zapytań próby obalenia w fali 2b' if 'fala 2b' in v else '')
    return (f"Nie znaleziono bezpośredniego konkurenta w badanym zakresie ({q}; anglojęzyczny web USA; 2026-10-25; "
            f"wyłącznie streszczenia wyszukiwarki, strony nieotwierane; pewność: {conf})")


# Godziny eksperta dla pilotów przyjęte w raporcie (kanon K4: szacunki agentów fali 2b, łącznie 86–135 h dla 5 pilotów).
PILOT_EXPERT_HOURS = {
    'RENO-02': '20–30 h',
    'RENO-03': '16–27 h',
    'HOME-04': '16–25 h',
    'HOME-02': '10–17 h w wersji podstawowej (13–22 h z recenzentami opcjonalnymi)',
    'AUTO-01': '24–36 h (nie jest tani; w tym CPA ds. podatku od sprzedaży ok. 10–14 h na start i 3–4 h rocznie)',
}

AI_RISK_HEAD = ('**Ryzyko, że asystent rozwiąże sam (analiza agenta, nie wynik testu; asystentów nie testowano).** '
                'Zdania o tym, co asystent „zrobi”, „policzy” albo „wyrenderuje”, to hipotezy agenta do sprawdzenia w panelu promptów (G0, krok 5). '
                'Wydanie funkcji generowania kalkulatorów potwierdzono tylko dla ChatGPT (Intelligent UI) i Google AI Mode [E-VER-C1, E-VER-C2]; '
                'dla Perplexity, Copilota i Claude go nie weryfikowano. Tekst agenta:')


def main(top10, position=None):
    """Karty finalistów w kolejności `top10`. `position` (ID → pozycja w rankingu §2) daje nagłówki „### ID (poz. N) — nazwa”
    (recenzja spójności, decisions#11); numer w kolejności budowy zostaje tylko w polu „Status (CSV)”."""
    ll = {x['final_id']: x for x in json.load(open('raw/longlist.json'))}
    CAL = json.load(open('raw/calibration.json'))
    PR = products_csv()
    out = []
    for rank, fid in enumerate(top10, 1):
        x = ll[fid]; a = load(f'raw/audit_{fid}.json'); r = load(f'raw/refute_{fid}.json'); d = load(f'raw/demand_{fid}.json')
        c = CAL[fid]; row = PR[fid]
        name = row['nazwa_robocza_en']  # nazwa robocza jak w product-opportunities.csv (kanon K4)
        head = f"### {fid} (poz. {position[fid]}) — {name}" if position else f"### {rank}. {fid} — {name}"
        out.append(head + "\n")
        out.append(f"**Rodzina:** {x['family_pl']} · **Ocena ważona:** agent {dec(c['agent'])} → po kalibracji **{dec(c['cal'])}** / 5 · "
                   f"**Status (CSV):** {status_text(row)} · **Pewność oceny/statusu:** {row['poziom_pewnosci (oceny/statusu)']}\n")
        if c.get('note'):
            out.append(f"> {c['note']}\n")
        out.append(f"- **Użytkownik i moment potrzeby:** {one(x['user_and_moment'])}")
        out.append(f"- **Przykładowe pytanie:** *{one(x['sample_prompt_en'])}*")
        out.append(f"- **Problem decyzyjny:** {one(x['decision_problem'])}")
        out.append(f"- **Warianty:** {one(x['variants_compared'])}")
        out.append(f"- **Kluczowe zależności:** {one(x['key_dependencies'])}")
        out.append(f"- **Główne wyniki:** {one(x['main_outputs'])}")
        out.append(f"- **Powód wejścia na zewnętrzną stronę:** {one(x['reason_external_site'])}\n")
        n_a = len(a['competitors']) if a else 0
        n_r = len(r['candidates']) if r else 0
        out.append(f"**Konkurencja (audyt fali 2: {n_a} pozycji + próba obalenia w fali 2b: {n_r} kandydatów; wszystkie pozycje w pełnym brzmieniu; "
                   "strony nieotwierane, dowód: search-summary):**\n")
        out.append(f"**Konkurent bezpośredni:** {competitor_line(row)}.\n")
        out.append("| Narzędzie | Typ | Co pokrywa (wg search-summary) | W search-summary nie widać / niezweryfikowane |\n|---|---|---|---|")
        if a:
            for comp in a['competitors']:
                link = f"[{cell(comp['name'])}]({comp['url']})" if comp['url'].startswith('http') else f"{cell(comp['name'])} (adres: {comp['url']})"
                covers = cell(comp['covers_pl'])
                if re.search(r'Asystent|AI assistants|ChatGPT|AI Mode', comp['name']):
                    covers = 'Hipoteza audytora (asystentów nie testowano; streszczenia WebSearch to nie test asystenta): ' + covers
                out.append(f"| {link} (audyt fali 2) | {TYP[comp['type']]} | {covers} | {misses(comp['misses_or_unverified_pl'])} |")
        if r:
            for cand in r['candidates']:
                link = f"[{cell(cand['name'])}]({cand['url']})" if cand['url'].startswith('http') else f"{cell(cand['name'])} (adres: {cand['url']})"
                out.append(f"| {link} (fala 2b) | {TYP[cand['classification']]} | {cell(cand['evidence_pl'])} | do ręcznej weryfikacji: {cell(cand['what_to_check_manually_pl'])} |")
        out.append("")
        if fid == 'RENO-02':
            out += verify_list_reno02()
        if a:
            out.append(f"**Luka (audyt):** {one(a['gap_statement_pl'])}\n")
        if r:
            out.append(f"**Próba obalenia (fala 2b; agent znał wyniki audytu, więc to nie jest niezależne potwierdzenie):** "
                       f"{'ZNALEZIONO konkurenta bezpośredniego. ' if r['direct_competitor_found'] else ''}{one(r['conclusion_pl'])} "
                       f"*Zakres:* {one(r['search_scope_pl'])} *Pewność wg agenta:* {LV[r['confidence']]}.\n")
        out.append("**Ocena kryteriów** (1–5; wyżej = lepiej / łatwiej / mniejsze ryzyko; pewność popytu, reklamy i dystrybucji AI ograniczona do „niska”, zob. §1.2):\n")
        out.append("| Kryterium (waga) | Ocena | Uzasadnienie | Dowody | Luki | Pewność |\n|---|---|---|---|---|---|")
        if a:
            out += criteria_rows(a, c)
        out.append("")
        if d:
            all_items = d['demand_evidence']
            items = all_items[:6]
            n_p = sum(1 for i, _ in enumerate(items) if i < len(AXES.get(fid, [])) and AXES[fid][i][1] == P)
            fq = d['forum_question_examples']
            n_f, n_rq, n_w = forum_counts(fid, len(fq))
            out.append("**Popyt (fala 2b):**\n")
            out.append(f"- **Bezpośrednie dowody popytu online (wolumeny wyszukiwań lub promptów): 0.** "
                       f"Pokazano {len(items)} z {len(all_items)} sygnałów zebranych przez agenta (pełna lista: `data/agent-outputs/demand_{fid}.json`, pole `demand_evidence`); "
                       f"pytania zadawane online: {n_p} z {len(items)} pokazanych. "
                       f"Przykłady pytań ({len(fq)}, wszystkie poniżej): pytania użytkowników z forów i serwisów Q&A: {n_f}; pytania czytelników w rubrykach wydawców: {n_rq}; "
                       f"nagłówki stron wydawców lub firm w formie pytania: {n_w} (podaż treści, sygnał pośredni). Wszystkie są anegdotyczne, bez wolumenu. "
                       f"Pozostałe sygnały mierzą zdarzenia, parametry modelu, deklaracje w ankietach albo podaż treści — to nie jest pomiar popytu. Pomiar: krok 2 bramki G0 (K-04).")
            for i, e in enumerate(items):
                out.append(f"- {demand_label(fid, i, e)} {one(e['claim_pl'])} (opis agenta, co mierzy: {one(e['measures_pl'])}) — {e['url']}")
            if fq:
                kinds = FORUM_KIND[fid]
                out.append("- Przykłady pytań (parafrazy agenta; w nawiasie kwadratowym: czym jest źródło): " +
                           '; '.join(f"[{FORUM_TAG[k]}] *{one(q['paraphrase_en'])}* ({q['url']})" for k, q in zip(kinds, fq)))
            out.append(f"- Sezonowość / wyzwalacze: {one(d['seasonality_or_triggers_pl'])}\n")
            out.append("**Prompty testowe (do przyszłego testu; wyników NIE symulowano):**\n")
            out.append("*Bez prośby o narzędzie:*")
            out += [f"{i}. {p}" for i, p in enumerate(d['prompts_no_tool_request'], 1)]
            out.append("\n*Z prośbą o kalkulator:*")
            out += [f"{i}. {p}" for i, p in enumerate(d['prompts_calculator_request'], 1)]
            out.append("\n*Z prośbą o porównanie scenariuszy:*")
            out += [f"{i}. {p}" for i, p in enumerate(d['prompts_scenario_comparison'], 1)]
            out.append("")
            out.append(f"{AI_RISK_HEAD} {one(d['ai_self_solve_assessment_pl'])}\n")
            out.append(f"**Zależności, które asystent prawdopodobnie pominie (hipoteza do sprawdzenia w panelu promptów):** {one(d['missing_dependencies_ai_likely_ignores_pl'])}\n")
            out.append(f"**MVP:** {one(d['mvp_scope_pl'])}\n")
            out.append(f"**Świadomie odłożone:** {one(d['deferred_features_pl'])}\n")
            out.append(f"**Dane i testy obliczeń:** {one(d['data_sources_and_tests_pl'])}\n")
            out.append(f"**Kontrola ekspercka (szacunek agenta):** {one(d['expert_review_pl'])}\n")
            if fid in PILOT_EXPERT_HOURS:
                out.append(f"**Godziny eksperta przyjęte w raporcie dla tego pilota (szacunek agenta fali 2b; podstawa wejść eksperckich w `economics.csv`):** "
                           f"{PILOT_EXPERT_HOURS[fid]}. Łącznie dla 5 pilotów 86–135 h.\n")
        out.append(f"**Ryzyko merytoryczne:** {LV[x['content_risk']]} · **Trudność implementacji:** {LV[x['impl_difficulty']]} · **Utrzymanie:** {LV[x['maintenance_burden']]} · "
                   f"**Otoczenie reklamowe (hipoteza; RPM niezmierzony):** {one(x['ad_environment'])}\n")
        out.append('---\n')
    text = '\n'.join(out)
    open('raw/cards.md', 'w').write(text)
    print('cards', len(top10), len(text))
    return text


if __name__ == '__main__':
    main(sys.argv[1].split(','))
