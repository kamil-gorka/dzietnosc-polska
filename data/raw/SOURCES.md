# Źródła danych

Katalog `data/raw/` nie jest wersjonowany. Ten plik dokumentuje, skąd
pochodzą pliki źródłowe i w jakiej wersji zostały pobrane.

---

## bdl_polska.csv

- **Źródło:** Bank Danych Lokalnych GUS, REST API
- **Endpoint:** `https://bdl.stat.gov.pl/api/v1`
- **Temat (subject):** P2346
- **Zmienne:** TFR, urodzenia żywe, zgony, ludność w grupach wieku 0–14, 15–49, 65+
- **Zakres lat:** 1995–2025, poziom krajowy (`unit-level=0`)
- **Data pobrania:** 2026-07-13
- **Skrypt:** `src/pobierz_bdl.py`
- **Licencja:** dane publiczne GUS, dozwolone ponowne wykorzystanie z podaniem źródła

---

## rocznik/

- **Źródło:** Rocznik Demograficzny GUS 2025 (tablice)
- **URL:** https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5515/3/19/1/rocznik_demograficzny_2025_tablice.zip
- **Format:** ZIP → 15 plików XLS (format binarny Excel 97–2003)
- **Data pobrania:** 2026-07-15
- **Sposób pozyskania:** automatyczny — `src/pobierz_rocznik.py`
  (pobranie ZIP + rozpakowanie do `data/raw/rocznik/`)
- **Skrypt parsujący:** `src/parsuj_rocznik.py`

### Faktycznie wykorzystywany plik

Parser czyta **wyłącznie** `01_tablice przeglądowe_RD'2025.xls`. Pozostałe
14 plików pozostaje w katalogu jako niezmieniona zawartość archiwum
(zasada: raw stays raw — nie usuwamy nic z pobranego źródła).

| Arkusz | Kolumna | Zmienna |
|---|---|---|
| Tabl. I | 2 | ludność, stan 31 XII (tys.) |
| Tabl. I | 5 | urodzenia żywe (tys.) |
| Tabl. I | 6 | zgony ogółem (tys.) |
| Tabl. V | 15 | TFR |

Odczyt ograniczony do sekcji OGÓŁEM (maszyna stanów odrzuca bloki
MIASTA i WIEŚ). Zakres źródła: 1946–2024, pełny — zawężenie do lat
projektu następuje dopiero w `zloz_dane.py`.

- **Nieużywane z Rocznika:** struktura wieku (`03_ludność_struktura wg wieku`)
  — inny podział grup wiekowych niż BDL, patrz README, sekcja
  *Braki danych: struktura wiekowa 1989–1994*.

---

## kohorty_kobiet.csv

- **Źródło:** Bank Danych Lokalnych GUS, REST API
- **Endpoint:** `https://bdl.stat.gov.pl/api/v1`
- **Temat (subject):** P2137 (Ludność wg grup wieku i płci)
- **Zakres lat:** 1995–2025, poziom krajowy (`unit-level=0`)
- **Data pobrania:** 2026-07-21
- **Skrypt:** `src/pobierz_kohorty.py`
- **Zmienne** (kobiety, grupy 5-letnie):
  - 15–19 → 72299
  - 20–24 → 47738
  - 25–29 → 47696
  - 30–34 → 47695
  - 35–39 → 47716
  - 40–44 → 47698
  - 45–49 → 47727
- **Licencja:** dane publiczne GUS, dozwolone ponowne wykorzystanie z podaniem źródła

> Numeracja ID nie jest ciągła — 72299 (15–19) odstaje od pozostałych
> (47695–47738). Zweryfikowano przez `/variables/{id}`: wszystkie siedem
> zmiennych ma `n2 = "kobiety"`, właściwe grupy wieku w `n1`.

---

## urodzenia_roczniki.csv

- **Źródło:** Bank Danych Lokalnych GUS, REST API
- **Endpoint:** `https://bdl.stat.gov.pl/api/v1`
- **Temat (subject):** P2167 (Urodzenia żywe wg pojedynczych roczników wieku matki)
- **Zakres lat:** 2002–2025, poziom krajowy (`unit-level=0`)
- **Data pobrania:** 2026-07-22
- **Skrypt:** `src/pobierz_urodzenia.py`
- **Zmienne:** 40 kolumn — `ogółem`, `12 i mniej`, roczniki 13–49, `50 i więcej`.
  Mapa ID pobierana dynamicznie z `/variables?subject-id=P2167`, nie zapisana na sztywno.
- **Licencja:** dane publiczne GUS, dozwolone ponowne wykorzystanie z podaniem źródła

> **Suma kontrolna:** `ogółem` = suma 39 roczników składowych (różnica maks. 0
> we wszystkich latach). Brak kategorii „wiek nieustalony".

> **Zakres krótszy niż `bdl_polska.csv`:** P2167 zaczyna się w 2002, nie 1995.
> Dekompozycja TFR/ASFR obejmie 2002–2025; rokiem bazowym dla kontrfaktycznego
> TFR jest 2002.

> **Traktowanie skrajów (decyzja metodologiczna):** urodzenia matek poniżej 15 lat
> doliczane do grupy 15–19, powyżej 49 lat do grupy 45–49 — zgodnie z praktyką GUS
> przy liczeniu TFR. Skala: <0,03% urodzeń rocznie (2024: 25 urodzeń w „50 i więcej",
> 25 w grupach poniżej 15 lat, przy 251 782 ogółem). ASFR skrajnych kohort jest przez
> to minimalnie zawyżony — licznik obejmuje kobiety spoza mianownika.
> Agregacja roczników do kohort 5-letnich następuje w `zloz_dane.py`, nie tutaj
> (zasada: raw stays raw).

---

## Uwaga o odtwarzalności

Pliki BDL są pobierane automatycznie i powinny być identyczne przy
ponownym uruchomieniu skryptu — z zastrzeżeniem, że GUS rewiduje dane
wsteczne (szczególnie ostatnie 1–2 lata, publikowane najpierw jako wstępne).
Roczniki Demograficzne to statyczne pliki archiwalne — bez ryzyka rewizji.

---

## Prognoza ludności GUS 2023–2060 (scenariusze demograficzne)

Wykorzystana w: Krok 5 projekcji (notebook `notebooks/02_projekcja.ipynb`),
wskaźniki obciążenia demograficznego i udziału 65+ dla trzech scenariuszy.

Źródło: Główny Urząd Statystyczny, „Prognoza ludności na lata 2023–2060".
Strona publikacji:
https://stat.gov.pl/obszary-tematyczne/ludnosc/prognoza-ludnosci/prognoza-ludnosci-na-lata-2023-2060,11,1.html

Data pobrania: 29.07.2026

Pobrano dwa odrębne pliki:

1. **Scenariusz główny (średni)** — pojedynczy plik XLSX (poziom powiatowy):
   „Prognoza ludności na lata 2023–2060. Tabela zbiorcza w formacie XLSX" (15,63 MB)
   https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5469/11/1/1/5-tabela_zbiorcza.xlsx
   → zapisany lokalnie jako `prognoza_gus_2023_2060/5-tabela_zbiorcza.xlsx` (arkusz „Główny scenariusz")

2. **Scenariusze alternatywne (niski i wysoki)** — archiwum ZIP (128,83 MB),
   rozpakowane lokalnie:
   „Prognoza ludności na lata 2023–2060. Scenariusze alternatywne w formacie XLSX w pliku ZIP"
   https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5469/11/1/1/6-scenariusze_alternatywne.zip
   → z archiwum użyto plików „Data table" (poziom powiatowy, arkusze „Low" i „High")
   → zapisane lokalnie jako:
       `prognoza_gus_2023_2060/Data table_niski.xlsx`  (scenariusz niski, arkusz „Low")
       `prognoza_gus_2023_2060/Data table_wysoki.xlsx` (scenariusz wysoki, arkusz „High")

Uwaga metodologiczna: scenariusz oficjalny (główny) zakłada wzrost TFR do 1,49 do 2060 r.;
faktyczny TFR w 2024 r. wyniósł 1,10 (poniżej najniższego scenariusza prognozy).
Wartości wskaźników w tym projekcie liczone są samodzielnie z pojedynczych roczników
wieku i walidowane przez odtworzenie oficjalnej kotwicy GUS (obciążenie demograficzne
scenariusza głównego: 70 w 2022 → 105 w 2060).

### Reprodukcja
Powyższe pliki (łącznie ~48 MB rozpakowanych XLSX) są **wykluczone z repozytorium**
przez `.gitignore` (reguła `data/raw/*`). Aby odtworzyć obliczenia Kroku 5:
1. pobierz oba pliki z podanych adresów,
2. rozpakuj ZIP, odszukaj „Data table.xlsx" w folderach `Niski/` i `Wysoki/`,
3. umieść trzy pliki bezpośrednio w `data/raw/prognoza_gus_2023_2060/` pod nazwami
   podanymi wyżej,
4. uruchom `notebooks/02_projekcja.ipynb` (Restart & Run All).