# Kryzys dzietności w Polsce (1989–2025)
### Analiza eksploracyjna danych demograficznych GUS

> Od 1,99 do 1,10 dziecka na kobietę w 36 lat. Co dokładnie się wydarzyło i kiedy?

---

## Dlaczego ten projekt

Rok **1989** — początek szeregu — zastał TFR na poziomie 1,99, tuż poniżej progu zastępowalności. Rok **2024** przyniósł najniższy odczyt w historii pomiarów — **1,099**. Ten projekt rekonstruuje pełen łuk tego spadku na danych źródłowych GUS i sprawdza, **które składowe demograficzne za niego odpowiadają**.

Projekt nie zatrzymuje się na stwierdzeniu „dzietność spada". Pyta:
- Czy kobiety rodzą **mniej dzieci**, czy tylko **później**? (efekt *quantum* vs *tempo*)
- Kiedy nastąpiły punkty zwrotne i co się z nimi zbiegło?
- Jak zmieniała się struktura wieku matek i jak przekłada się to na liczbę urodzeń?

<!-- TODO: po ukończeniu analizy wstaw tu 1 kluczowy wykres jako "hero image" -->
<!-- ![Spadek TFR 1989-2025](figures/01_tfr_trend.png) -->

---

## Kluczowe wnioski

<!-- TODO: uzupełnić po analizie. Format: 3-5 punktów, każdy = jedno zdanie + liczba -->

1. *(do uzupełnienia)*
2. *(do uzupełnienia)*
3. *(do uzupełnienia)*

---

## Dane

| Źródło | Zakres | Format | Sposób pozyskania |
|---|---|---|---|
| [Bank Danych Lokalnych GUS](https://bdl.stat.gov.pl/bdl/) | 2002–2025 (TFR), 1995–2025 (pozostałe) | JSON | REST API (`src/pobierz_bdl.py`) |
| [Rocznik Demograficzny GUS](https://stat.gov.pl/) | 1989–2001 | XLS (ZIP) | skrypt (`src/pobierz_rocznik.py`) |
| [BDL GUS — urodzenia wg wieku matki](https://bdl.stat.gov.pl/bdl/) | 2002–2025 | JSON | REST API (`src/pobierz_urodzenia.py`), temat P2167 |
| [BDL GUS — kobiety wg grup wieku](https://bdl.stat.gov.pl/bdl/) | 1995–2025 | JSON | REST API (`src/pobierz_kohorty.py`), temat P2137 |

**Uwaga metodologiczna o jakości danych:** BDL udostępnia TFR od 2002 r., dlatego lata 1989–2001 uzupełniono z Rocznika Demograficznego. Połączenie dwóch źródeł o różnej strukturze udokumentowano w `src/zloz_dane.py`. Dane za 2025 r. mogą mieć charakter wstępny — GUS publikuje statystyki demograficzne z opóźnieniem (Q1–Q2 za rok poprzedni).

### Analizowane zmienne
- Współczynnik dzietności ogólnej (TFR)
- Urodzenia żywe i zgony (przyrost naturalny)
- Cząstkowe współczynniki płodności (ASFR) wg grup wieku matki
- Urodzenia według pojedynczego rocznika wieku matki
- Struktura wieku kobiet w wieku rozrodczym (15–49)

---

## Struktura projektu

```
dzietnosc-polska/
├── data/
│   ├── raw/              # dane źródłowe — poza repo (.gitignore)
│   │   └── SOURCES.md    # spis źródeł z datami pobrania
│   ├── interim/          # pośrednie wyniki parsowania (rocznik_pelny.csv)
│   └── processed/        # dane po czyszczeniu, gotowe do analizy
├── notebooks/
│   ├── 01_eksploracja.ipynb
│   └── 02_pobranie_kohorty.ipynb
├── src/
│   ├── pobierz_bdl.py       # klient API GUS BDL (TFR, ruch naturalny)
│   ├── pobierz_kohorty.py   # kobiety wg grup wieku 15–49 (P2137)
│   ├── pobierz_urodzenia.py # urodzenia wg rocznika wieku matki (P2167)
│   ├── szukaj_zmiennych.py  # wyszukiwanie ID zmiennych w BDL
│   ├── pobierz_rocznik.py   # Roczniki Demograficzne XLS
│   ├── parsuj_rocznik.py    # ekstrakcja danych 1989–2001
│   ├── zloz_dane.py         # scalenie serii BDL + Rocznik
│   ├── zloz_asfr.py         # agregacja ASFR + kontrola TFR
│   └── sprawdzenie.py       # walidacja zgodności serii
├── sql/
│   └── analiza.sql       # zapytania analityczne
├── figures/              # wyeksportowane wykresy
├── docs/                 # dokumentacja i kontekst analityczny
├── environment.yml       # definicja środowiska (reprodukowalność)
└── README.md
```

---

## Jak odtworzyć analizę

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/kamil-gorka/dzietnosc-polska.git
cd dzietnosc-polska

# 2. Odtwórz środowisko
conda env create -f environment.yml
conda activate dzietnosc

# 3. Pobierz dane z API GUS
python src/pobierz_bdl.py

# 4. Pobierz i sparsuj Roczniki Demograficzne (1989–2001)
python src/pobierz_rocznik.py
python src/parsuj_rocznik.py

# 5. Pobierz dane do dekompozycji ASFR
python src/pobierz_kohorty.py
python src/pobierz_urodzenia.py

# 6. Złóż serie
python src/zloz_dane.py
python src/zloz_asfr.py

# 7. Uruchom notebooki
jupyter lab
```

---

## Stack technologiczny

**Python** (pandas, matplotlib, seaborn, requests) · **SQL** (SQLite) · **Jupyter** · **Git**

---

## Kontekst analityczny

Projekt wyrasta z szerszej analizy systemowej kryzysu demograficznego (`docs/`), w której zidentyfikowano m.in. rozróżnienie między **efektem tempo** (odraczanie urodzeń) a **efektem quantum** (realny spadek liczby dzieci). To rozróżnienie jest kluczowe: gdyby spadek TFR wynikał głównie z odraczania, byłby częściowo artefaktem pomiaru okresowego. Analiza danych sprawdza, która składowa dominuje.

---

## Decyzje metodologiczne

Repozytorium nie zawiera surowych danych — `data/raw/` jest w `.gitignore`.
Pipeline odtwarzający zbiór opisano wyżej, w sekcji *Jak odtworzyć analizę*.
Spis źródeł z datami pobrania: `data/raw/SOURCES.md`.

### Walidacja danych historycznych

Rocznik Demograficzny dostarcza TFR dla lat 1989–2001, dla których BDL
nie publikuje danych. W latach 2002–2024 (23 lata) oba źródła zachodzą
na siebie — porównanie wykazało zgodność do trzeciego miejsca po przecinku.

Ograniczenie: nie jest to niezależne potwierdzenie. Oba kanały publikują
tę samą produkcję GUS. Zgodność potwierdza poprawność scalenia serii
i spójność dystrybucji, nie poprawność samych szacunków.

### Weryfikacja ASFR przez odtworzenie TFR

Odtworzony TFR (Σ ASFR × 5) zgadza się ze wskaźnikiem GUS ze średnim
błędem względnym 1,02% (max 1,94%, próg akceptacji 3%). Reszta nie jest
szumem — koreluje z rokiem na poziomie 0,858, przechodząc od −0,54% (2002)
przez zero (~2006) do +1,94% (2020) i z powrotem do +1,27% (2025).

Odrzucone wyjaśnienia:
- **Data referencyjna mianownika** (31.12 vs połowa roku): efekt poziomu,
  nie trendu. Korelacja reszty z tempem zmiany kohorty: −0,355.
- **Skraje w liczniku bez odpowiednika w mianowniku** (urodzenia matek
  <15 i 50+): udział 0,012–0,023% urodzeń, dwa rzędy wielkości za mało.
- **Rewizja spisowa jednego ze źródeł**: udział kobiet 15–49 w ludności
  ogółem spada gładko 26,2% → 22,7% bez nieciągłości w 2011 ani 2021.

Hipoteza otwarta: GUS prawdopodobnie liczy TFR sumą ASFR po pojedynczych
rocznikach, nie po grupach pięcioletnich. Przy przesuwającej się medianie
wieku matki (26 → 30 lat) aproksymacja grupowa generuje narastające
obciążenie. Weryfikacja wymaga kohort kobiet w pojedynczych rocznikach.

### Braki danych: struktura wiekowa 1989–1994

Kolumny `ludnosc_przedprodukcyjna`, `ludnosc_produkcyjna`,
`ludnosc_poprodukcyjna` mają wartości `NaN` dla lat 1989–1994.

Powód: BDL udostępnia szeregi ludności wg grup wieku od 1995 r.
Wcześniejsze dane istnieją w Rocznikach Demograficznych, ale w innym
podziale grup wiekowych (5-letnie kohorty bez agregatów) i po korekcie
NSP 2002, co czyni je nieporównywalnymi z serią 1995+ bez dodatkowej
harmonizacji.

Decyzja: braki pozostawiono jako `NaN` zamiast imputacji. Analizy
oparte na strukturze wiekowej ograniczono do 1995+; analizy TFR
i ruchu naturalnego obejmują pełen zakres 1989–2025.

**Uwaga:** dotyczy to wyłącznie kolumn grup wiekowych pochodzących z BDL.
Ruch naturalny (urodzenia, zgony) jest kompletny dla całego zakresu
1989–2025, ponieważ dla lat 1989–1994 pochodzi z tablic Rocznika.

### Dlaczego `data/raw/` jest poza repozytorium

1. Format — tablice Rocznika to pliki binarne XLS, których Git nie diffuje.
2. Źródło prawdy — dane należą do GUS. Repozytorium zawiera kod
   odtwarzający zbiór, nie jego kopię.
3. Odtwarzalność — wymuszenie uruchomienia pipeline'u weryfikuje,
   że skrypty faktycznie działają.

W repozytorium znajdują się: `data/interim/rocznik_pelny.csv` (wynik parsera),
`data/processed/` (dane gotowe do analizy, CSV), `data/raw/SOURCES.md`
(spis źródeł z datami pobrania).

---

## Autor

**Kamil** · [LinkedIn](#) · [GitHub](#)

*Projekt portfolio — analiza danych.*