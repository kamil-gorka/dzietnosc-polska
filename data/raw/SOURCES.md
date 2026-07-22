# Źródła danych

Katalog `data/raw/` nie jest wersjonowany. Ten plik dokumentuje, skąd
pochodzą pliki źródłowe i w jakiej wersji zostały pobrane.

---

## bdl_polska.csv

- **Źródło:** Bank Danych Lokalnych GUS, REST API
- **Endpoint:** `https://bdl.stat.gov.pl/api/v1`
- **Temat (subject):** P2346
- **Zmienne:** TFR, urodzenia żywe, zgony, ludność w grupach wieku 0–14, 15–49, 65+
- **Zakres lat:** 1995–2025
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
- **Temat (subject):** P2137 (Ludność wg grup wieku i płci)
- **Zakres lat:** 1995–2025, poziom krajowy (`unit-level=0`)
- **Data pobrania:** 2026-07-21
- **Skrypt pobierający:** `src/pobierz_kohorty.py`
- **Zmienne** (kobiety, grupy 5-letnie):
  15-19 → 72299
  20-24 → 47738
  25-29 → 47696
  30-34 → 47695
  35-39 → 47716
  40-44 → 47698
  45-49 → 47727
- **Licencja:** dane publiczne GUS, dozwolone ponowne wykorzystanie z podaniem źródła

> Numeracja ID nie jest ciągła — 72299 (15–19) odstaje od pozostałych
> (47695–47738). Zweryfikowano przez `/variables/{id}`: wszystkie siedem
> zmiennych ma `n2 = "kobiety"`, właściwe grupy wieku w `n1`.

---

## Uwaga o odtwarzalności

Pliki BDL są pobierane automatycznie i powinny być identyczne przy
ponownym uruchomieniu skryptu — z zastrzeżeniem, że GUS rewiduje dane
wsteczne (szczególnie ostatnie 1–2 lata, publikowane najpierw jako wstępne).
Roczniki Demograficzne to statyczne pliki archiwalne — bez ryzyka rewizji.