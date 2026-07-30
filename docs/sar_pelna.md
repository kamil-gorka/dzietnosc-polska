# Systemowa Analiza Rzeczywistości: kryzys demograficzny Polski

**Warstwa interpretacyjna projektu `dzietnosc-polska`.** Ten dokument zawiera pełną
analizę systemową — mechanizmy, sprzężenia zwrotne i punkty interwencji. Warstwa
danowa (pipeline, wizualizacje, walidacja) opisana jest w [`README.md`](../README.md)
i [`docs/analiza_projekcja.md`](analiza_projekcja.md); tutaj chodzi o *interpretację*
tego, co dane pokazują, a nie o same dane.

## Nota o metodzie i etykietach epistemicznych

Analiza rozdziela trzy poziomy pewności twierdzeń, oznaczane w tekście:

- **[FAKT EMPIRYCZNY]** — twierdzenie oparte na danych obserwacyjnych (pomiar, rejestr,
  oficjalna statystyka). Weryfikowalne przez odwołanie do źródła.
- **[SZACUNEK Z LITERATURY]** — wartość liczbowa pochodząca z cudzego modelu lub
  prognozy (np. projekcja GUS), nie z pomiaru. Obarczona niepewnością modelu.
- **[TWIERDZENIE STRUKTURALNE]** — wniosek o mechanizmie, wyprowadzony z logiki
  systemu. Nie jest ani pomiarem, ani cytatem — jest interpretacją, którą dane mogą
  ilustrować, ale nie dowodzić w sensie przyczynowym.

Rozdzielenie to jest celowym zabezpieczeniem przed najczęstszym błędem analizy
systemowej: myleniem *korelacji zaobserwowanej w danych* z *mechanizmem przyczynowym
wyprowadzonym z modelu*. Liczba może pokazać, że coś rośnie; nie może sama pokazać,
dlaczego.

Analiza przyjmuje jedno założenie ramowe: aktorzy polityczni traktowani są jako
**racjonalni optymalizatorzy w strukturze bodźców**, nie jako podmioty moralne. Pytanie
nie brzmi „dlaczego nie robią tego, co słuszne", lecz „jaka struktura wypłat czyni
zaniechanie racjonalnym wyborem".

---

## Krok 1: Architektura pierwotnych przyczyn (meta-sterowniki)

Zamiast opisywać objawy poszczególnych kryzysów (demografia, fiskus, zdrowie, edukacja,
rynek pracy), analiza szuka **wspólnych wektorów sterujących** — czynników, które
zasilają wszystkie te kryzysy jednocześnie. Zidentyfikowano trzy.

### Meta-sterownik I — Niewidzialność kosztu zaniechania w cyklu wyborczym

[TWIERDZENIE STRUKTURALNE] Najgłębszy sterownik. We wszystkich pięciu obszarach koszt
niepodjęcia działania jest: (a) **kontrfaktyczny** — nie widać, co by było, gdyby
działano; (b) **nieatrybuowalny** — nie da się przypisać konkretnemu decydentowi;
(c) **odroczony** — materializuje się poza kadencją; (d) **maskowany fałszywym
pozytywem** — bieżące wskaźniki wyglądają znośnie, dopóki próg nie zostanie
przekroczony. W efekcie racjonalny aktor w cyklu wyborczym systematycznie wybiera
odroczenie, bo koszt działania jest natychmiastowy i widoczny, a koszt zaniechania —
nie. To jest „kod źródłowy" wspólny wszystkim kryzysom.

### Meta-sterownik II — Rozjazd stałych czasowych

[TWIERDZENIE STRUKTURALNE] Procesy demograficzne mają stałe czasowe rzędu dekad
(kohorta wchodzi w wiek produkcyjny 18–25 lat po urodzeniu), podczas gdy cykl decyzyjny
ma stałą rzędu kadencji (4 lata). Ten rozjazd sprawia, że system nie może domknąć pętli
korekcyjnej w normalnym trybie — sygnał zwrotny wraca zbyt późno, by wpłynąć na
decydenta, który go wywołał.

### Meta-sterownik III — Koszt strukturalny rodzicielstwa jako zmienna ukryta

[TWIERDZENIE STRUKTURALNE] Decyzja prokreacyjna zależy nie od dochodu (na który polityka
umie działać transferem), lecz od **kosztu strukturalnego**: mieszkania, czasu, kosztu
alternatywnego kariery — zwłaszcza kobiety. Te koszty są słabo widoczne w debacie
publicznej i trudne do zaadresowania parametrem, więc polityka celuje w dochód
(widoczny, łatwy), a nie w koszt (ukryty, trudny) — i systematycznie chybia.

---

## Krok 2: Objawy jako symptomy wspólnej struktury

[TWIERDZENIE STRUKTURALNE] Pięć kryzysów wymienionych w zakresie analizy — demografia,
fiskus, zdrowie, edukacja, rynek pracy — nie jest pięcioma niezależnymi problemami,
lecz pięcioma **objawami tej samej struktury** generowanej przez meta-sterowniki
z Kroku 1. Wspólny wzorzec: w każdym z nich koszt inakcji jest niewidzialny w oknie
decyzyjnym (Meta-sterownik I), stała czasowa problemu przekracza kadencję
(Meta-sterownik II), a właściwa dźwignia jest ukryta lub trudna (Meta-sterownik III).

**Dwa kryzysy ukryte**, rzadko obecne w debacie, a wynikające z powyższych:

*Kryzys wiedzy instytucjonalnej* — odejście dużych kohort z rynku pracy (Krok 5:
podwojenie OADR) oznacza utratę nieskodyfikowanej wiedzy operacyjnej szybciej, niż
młodsze, mniejsze kohorty zdążą ją przejąć. To kryzys nie liczby pracowników, lecz
*ciągłości kompetencji*.

*Kryzys legitymizacji międzypokoleniowej* — rosnące obciążenie pracujących (Krok 5:
DR 70→105+) przenosi coraz większy transfer od malejącej kohorty młodych do rosnącej
kohorty starszych, co podważa umowę pokoleniową leżącą u podstaw systemu emerytalnego
i zdrowotnego.

---

## Krok 3: Mapowanie pętli sprzężeń zwrotnych

Pętle opisane są przez **mechanizm transferu** — co płynie między elementami systemu,
w którą stronę, z jakim znakiem.

### Pętla P1 — Kohortowa spirala reprodukcyjna [dodatnia, samowzmacniająca]

[TWIERDZENIE STRUKTURALNE] Mniejsza kohorta kobiet w wieku rozrodczym → mniej urodzeń
(nawet przy stałym współczynniku płodności) → mniejsza kohorta następna → jeszcze mniej
urodzeń za pokolenie. Transfer: przepływa **liczebność kohorty** z okresu *t* do *t+25*,
pomnożona przez płodność. Znak dodatni = samowzmacnianie w kierunku spadku.

[SZACUNEK Z LITERATURY] Dowód siły tej pętli: nawet scenariusz wysoki GUS (dzietność
1,79) kończy 2060 z populacją 34,8 mln — poniżej startowych 37,8 mln. Gdyby wystarczyło
podnieść płodność, wysoki scenariusz odbudowałby populację. Nie odbudowuje, bo kohorta
rodzicielska jest już zdeterminowana przez urodzenia sprzed 2020 r. To empiryczny ślad
„momentum ujemnego": interwencja na płodności działa dopiero za pokolenie.

Dlaczego to pętla, a nie łańcuch przyczynowy: łańcuch dałoby się przeciąć w jednym
punkcie; pętli nie, bo skutek (mała kohorta dzieci) staje się przyczyną (mała kohorta
rodziców) w następnym cyklu. To rozróżnienie determinuje, gdzie w ogóle da się
interweniować (Krok 4).

### Pętla P2 — Fiskalno-elektoralna pętla wygaszania [ujemna dla systemu, domykająca się politycznie]

[TWIERDZENIE STRUKTURALNE] Starzenie → rosnące obciążenie fiskalne → presja na budżet →
wybór między podniesieniem obciążeń pracujących a cięciem świadczeń → oba kosztują głosy
→ aktor wybiera odroczenie → obciążenie rośnie dalej. Transfer: **sygnał kosztu** przez
cykl wyborczy, z opóźnieniem lokującym koszt poza horyzontem decyzyjnym decydenta.

[SZACUNEK Z LITERATURY] Paliwo pętli: OADR (liczba osób 65+ na 100 osób w wieku 15–64)
podwaja się z 29,9 (2022) do 59,6 (2060) — z trzech pracujących na emeryta do dwóch.
Najmocniejszy dowód to **inwersja obciążenia**: scenariusz wysoki ma DR 110,2 wobec
100,3 w niskim. [TWIERDZENIE STRUKTURALNE] Oznacza to, że interwencja prorodzinna, która
„udaje się" demograficznie, *podnosi* krótkookresowe obciążenie pracujących — dokłada
dzieci do licznika, zanim wejdą do mianownika (za 20 lat). Pętla P2 wygasza więc własne
rozwiązanie: polityk skutecznie podnoszący dzietność zostałby ukarany wzrostem
obciążenia w swoim cyklu, a nagrodzony dopiero jego następca dwie kadencje później.

To czyni P2 atraktorem systemu: dryfuje ku odraczaniu nie z powodu złej woli, lecz
dlatego że struktura wypłat (koszt natychmiastowy, korzyść odroczona i nieatrybuowalna)
czyni odroczenie racjonalnym w każdym pojedynczym cyklu.

*Uwaga o znaku pętli:* P2 jest jednocześnie stabilizująca (dla kariery decydenta)
i destabilizująca (dla systemu). Znak zależy od wybranej zmiennej wyjściowej —
tutaj liczony względem stabilności systemu, nie stabilności pozycji aktora.

### Pętla P3 — Kompetencyjno-migracyjna pętla kompensacyjna [ujemna, tłumiąca, nietrwała]

[TWIERDZENIE STRUKTURALNE] Kurcząca się podaż pracy → luka kompetencyjna i płacowa →
import siły roboczej + presja na automatyzację → chwilowe domknięcie deficytu → sygnał
„problem rozwiązany" (fałszywy pozytyw) → osłabienie presji na interwencję strukturalną
→ pętla P1 działa dalej nietknięta. Transfer: **podaż pracy spoza systemu** (migranci)
i **substytucja kapitałowa** (automatyzacja), kompensujące objaw bez ruszania sterownika.

[SZACUNEK Z LITERATURY] Scenariusz główny osiąga 30,9 mln głównie dzięki dodatniemu
saldu migracji — ale jego DR i tak dochodzi do 104,8. Migracja tłumi spadek liczebności,
lecz nie odwraca obciążenia, bo migranci ekonomiczni sami się starzeją i podlegają tym
samym sterownikom kosztu rodzicielstwa. Pętla ujemna z wbudowanym wyciekiem: kompensuje
wolniej, niż narasta problem, i generuje fałszywy sygnał sukcesu.

### Pętla P4 — Sprzężenie międzysektorowe (edukacja → praca → fiskus → prokreacja) [dodatnia, wielosektorowa]

[TWIERDZENIE STRUKTURALNE] Pętla spinająca wszystkie kryzysy. Kryzys edukacji
(niedopasowanie kompetencji, erozja autorytetu nauczyciela) → gorsze dopasowanie
absolwentów do rynku pracy → niższa produktywność, luka kompetencyjna → słabsza baza
podatkowa wobec rosnących zobowiązań → wyższe realne obciążenie młodych pracujących →
wzrost kosztu alternatywnego rodzicielstwa → odłożenie/rezygnacja z dzieci → mniejsza
kohorta → mniejsza baza uczniów i podatników w następnym cyklu → dalsza erozja
finansowania edukacji. Transfer przechodzi przez cztery sektory i zamyka się na wejściu.

[SZACUNEK Z LITERATURY] Nieliniowość czasowa obciążenia (płasko 70→72 do 2035, potem
skokowo do 96,8 w 2050) pokazuje, że presja na młodych pracujących — kluczowe ogniwo P4
— nie narasta liniowo, lecz uderza po 2040. [TWIERDZENIE STRUKTURALNE] Pętla P4 ma
**ukryty próg**: dziś jej sygnał jest słaby (stąd niski priorytet polityczny edukacji),
a gdy stanie się silny, kohorta zdolna ją odwrócić już się skurczy.

---

## Krok 4: Punkty przyłożenia siły (leverage points)

Uporządkowane wg hierarchii Meadows — od najsłabszych (parametry) do najsilniejszych
(reguły, przepływ informacji). Siła rośnie odwrotnie do politycznej wykonalności.

### LP1 — Transfery pieniężne na dzieci [parametr, słaby]

[TWIERDZENIE STRUKTURALNE] Zmienia jeden składnik decyzji prokreacyjnej (dochód), nie
ruszając struktury kosztu (mieszkanie, czas, koszt alternatywny). Atakuje P1 tylko przez
płodność. Dowód słabości: nawet scenariusz wysoki nie odwraca populacji — samo
podniesienie płodności nie pokonuje momentum P1. Punkt malejących zwrotów, na którym
system już operuje.

### LP2 — Struktura kosztu mieszkaniowego i czasu rodzicielstwa [struktura przepływu, średni]

[TWIERDZENIE STRUKTURALNE] Uderza w koszt, nie w dochód — zmienia równanie decyzyjne po
stronie, której transfer nie dotyka. Obniżenie strukturalnego kosztu dziecka (podaż
mieszkań, opieka, elastyczność pracy) zmienia płodność bez zależności od corocznego
transferu. Atakuje wejście do P1 i pośrednio P4. Wciąż jednak nie rusza mianownika P1 —
działa na płodność, nie na liczebność kohorty.

### LP3 — Reguła horyzontu decyzyjnego klasy politycznej [reguła systemu, silny]

[TWIERDZENIE STRUKTURALNE] Atakuje bezpośrednio P2 — pętlę-atraktor. Jądrem P2 jest
niedopasowanie horyzontu: koszt interwencji mieści się w kadencji, korzyść nie. Punkt
przyłożenia to każda reguła przenosząca przyszły koszt zaniechania do teraźniejszości
decydenta: niezależne ciała fiskalne z wieloletnim mandatem, reguły wydatkowe wiążące
dzisiejsze decyzje z projekcją długu, obowiązek raportowania kosztu zaniechania
w horyzoncie 30-letnim. Nie zmienia demografii bezpośrednio — zmienia **funkcję wypłat
aktora**. Dlatego nieproporcjonalnie silny: mała zmiana reguły przełącza zachowanie
wszystkich aktorów w pętli.

Dowód, że to najwyższy realny punkt: inwersja obciążenia (Krok 5) pokazuje, że dopóki
horyzont = kadencja, żaden racjonalny aktor nie wybierze interwencji prorodzinnej, bo
płaci obciążeniem od razu.

### LP4 — Uczynienie kosztu zaniechania natychmiast obserwowalnym [przepływ informacji, najsilniejszy]

[TWIERDZENIE STRUKTURALNE] Atakuje wspólny sterownik wszystkich pętli — niewidzialność
kosztu zaniechania (Meta-sterownik I). Wszystkie cztery pętle zamykają się tylko dlatego,
że koszt inakcji jest kontrfaktyczny, nieatrybuowalny i maskowany fałszywym pozytywem.
Punkt przyłożenia to każdy mechanizm przekształcający ten koszt w sygnał **natychmiastowy
i atrybuowalny**: publiczny licznik długu demograficznego, przypisanie przyszłych ubytków
świadczeń do dzisiejszych zaniechań, włączenie projekcji obciążenia do cyklu budżetowego.
Zmienia nie parametr i nie regułę, lecz **strukturę informacji, na podstawie której
system w ogóle rozpoznaje problem**.

[FAKT EMPIRYCZNY] Dowód działania mechanizmu fałszywego pozytywu: oficjalna prognoza GUS
2023 założyła wzrost dzietności do 1,49, podczas gdy faktyczna w 2024 r. wyniosła 1,10 —
rzeczywistość przebiła najniższy scenariusz. [TWIERDZENIE STRUKTURALNE] Nieliniowość
obciążenia (spokój do 2035) potwierdza mechanizm: sygnał jest z natury słaby dokładnie
w oknie, gdy interwencja jest jeszcze skuteczna, i staje się silny dopiero, gdy jest za
późno. LP4 to jedyny punkt atakujący tę asymetrię u źródła.

---

## Krok 5: Projekcja w przód — trzy reżimy dynamiczne

Pełny opis danych, metody i walidacji: [`docs/analiza_projekcja.md`](analiza_projekcja.md).
Tutaj — interpretacja projekcji jako reżimów zachowania systemu.

Scenariusze GUS (niski / główny / wysoki) odwzorowują się na reżimy dynamiczne systemu
zależnie od poziomu interwencji w hierarchii Meadows:

- **S1 — Inercja strukturalna** (≈ scenariusz niski): pętle nienaruszone, sterowniki
  działają bez interwencji. Trajektoria bazowa, nie „katastrofa" — przedłużenie obecnego
  reżimu, w którym każdy obrót pętli obniża pułap następnego.
- **S2 — Kompensacja peryferyjna** (≈ scenariusz główny): interwencja na niskich
  leverage points (LP1–LP2, transfery, migracja). Objawy łagodzone, pętle spowalniane,
  ale znak niezmieniony. Atraktor systemu, bo jedyny reżim mieszczący koszt i korzyść
  w tej samej kadencji.
- **S3 — Rekonfiguracja strukturalna** (≈ scenariusz wysoki, *co do wyniku*): odwrócenie
  znaku przynajmniej jednej pętli dominującej przez interwencję na wysokich leverage
  points (LP3–LP4).

[TWIERDZENIE STRUKTURALNE] **Zastrzeżenie o mapowaniu:** zestawienie scenariuszy GUS
z reżimami S1–S3 jest odwzorowaniem *wyników*, nie *mechanizmów*. GUS parametryzuje
scenariusze trzema współczynnikami wejściowymi (dzietność, umieralność, migracja);
rama SAR klasyfikuje reżimy przez poziom interwencji Meadows. Te osie są ortogonalne.
Scenariusz wysoki GUS osiąga 34,8 mln głównie migracją i długością życia (mechanizm
tożsamy z S2 zastosowanym z maksymalną intensywnością), nie przez odwrócenie pętli
dzietności definiujące S3. Kotwica ilościowa pełni tu funkcję kalibracji skali, nie
walidacji struktury przyczynowej — utożsamienie obu byłoby błędem kategorialnym.

### Domknięcie: asymetria prawdopodobieństw

[TWIERDZENIE STRUKTURALNE] Trzy reżimy nie są równie prawdopodobne. Ich rozkład jest
zdeterminowany przez Meta-sterownik I: S2 jest atraktorem, bo jako jedyny mieści koszt
i obserwowalną korzyść w jednym cyklu wyborczym. S1 jest domyślną trajektorią przy
paraliżu decyzyjnym. S3 wymaga złamania logiki cyklu — co empirycznie następuje
w systemach demokratycznych niemal wyłącznie pod presją egzogenicznego szoku. Bez zmiany
reguł generujących horyzont decyzyjny (LP3–LP4, nie ich objawy) system dryfuje między S1
a S2, przy czym każdy rok zwłoki obniża sufit osiągalny w S3 — bo kohorta zdolna do
rekonfiguracji sama się kurczy.

To jest strukturalne wyjaśnienie, dlaczego kryzys demograficzny pozostaje nierozwiązany
mimo powszechnej świadomości: rozwiązanie leży w punktach (LP3–LP4), do których dostęp
jest blokowany przez tę samą pętlę (P2), którą miałyby przeciąć.

---

*Dokument stanowi warstwę interpretacyjną. Wszystkie wartości liczbowe oznaczone
[SZACUNEK Z LITERATURY] pochodzą z projekcji GUS 2023–2060 i są policzone w warstwie
danowej projektu — zob. [`docs/analiza_projekcja.md`](analiza_projekcja.md) oraz
`notebooks/02_projekcja.ipynb`.*
