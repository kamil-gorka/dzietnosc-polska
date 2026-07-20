# Źródła danych

Katalog `data/raw/` nie jest wersjonowany. Ten plik dokumentuje, skąd
pochodzą pliki źródłowe i w jakiej wersji zostały pobrane.

---

## bdl_polska.csv

- **Źródło:** Bank Danych Lokalnych GUS, REST API
- **Endpoint:** `https://api.stat.gov.pl/api/v1`
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

## Uwaga o odtwarzalności

Pliki BDL są pobierane automatycznie i powinny być identyczne przy
ponownym uruchomieniu skryptu — z zastrzeżeniem, że GUS rewiduje dane
wsteczne (szczególnie ostatnie 1–2 lata, publikowane najpierw jako wstępne).
Roczniki Demograficzne to statyczne pliki archiwalne — bez ryzyka rewizji.