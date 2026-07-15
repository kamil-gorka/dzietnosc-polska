"""
parsuj_rocznik.py
=================
Parser tablic przeglądowych Rocznika Demograficznego GUS (.xls).

Wyciąga roczne szeregi czasowe z sekcji OGÓŁEM:
  - TFR (współczynnik dzietności ogólnej)  -> Tabl. V, kol. 15
  - ludność (stan 31 XII, w tys.)          -> Tabl. I, kol. 2
  - urodzenia żywe (w tys.)                -> Tabl. I, kol. 5
  - zgony ogółem (w tys.)                  -> Tabl. I, kol. 6

Zakres źródła: pełny (1946-2023 dla RD'2024). Zawężenie do zakresu
projektu (1989+) następuje na etapie złączenia z BDL, nie tutaj -
raw stays raw.

Użycie jako modułu:
    from parsuj_rocznik import zbuduj_ramke
    df = zbuduj_ramke("data/raw/rocznik/01_tablice...xls")

Użycie jako skryptu:
    python parsuj_rocznik.py
"""

import re
from pathlib import Path

import pandas as pd
import xlrd

# --- Stałe konfiguracyjne (indeksy zweryfikowane inspekcją nagłówków) ---
ARKUSZ_TFR = "Tabl. V"
ARKUSZ_RUCH = "Tabl. I"
KOL_TFR = 15                      # "dzietności / total fertility" (NIE 16 = reprodukcja brutto)
KOL_RUCH = {"ludnosc": 2,         # ludność, stan 31 XII
            "urodzenia": 5,       # urodzenia żywe
            "zgony": 6}           # zgony ogółem
NAGLOWKI_SEKCJI = ("OGÓŁEM", "MIASTA", "WIEŚ")


def wyodrebnij_rok(surowa_wartosc):
    """Wyciąga 4-cyfrowy rok z komórki GUS.

    Obsługuje warianty: 1989.0 (float), '1946a' (przypis literowy), '1949' (str).
    Ogranicza pierwszą cyfrę do 1[89]/20, by odrzucić 4-cyfrowe nie-lata
    (np. liczbę ludności 24412, która trafia do kolumny lat jako szum).
    """
    m = re.match(r'(1[89]\d{2}|20\d{2})', str(surowa_wartosc).strip())
    return int(m.group(1)) if m else None


def _czy_naglowek_sekcji(tekst):
    """True, jeśli komórka to nagłówek przekroju (OGÓŁEM / MIASTA / WIEŚ)."""
    t = str(tekst).strip().upper()
    return any(t.startswith(k) for k in NAGLOWKI_SEKCJI)


def _komorka_liczba(surowy):
    """Konwersja komórki na float; '.' oraz pusty string -> None (brak danych)."""
    if isinstance(surowy, str) and surowy.strip() in (".", ""):
        return None
    return float(surowy)


def _czytaj_sekcje_ogolem(sh):
    """Generator (rok, indeks_wiersza) WYŁĄCZNIE dla sekcji OGÓŁEM.

    Maszyna stanów: nagłówek 'OGÓŁEM' włącza czytanie, każdy inny nagłówek
    sekcji (MIASTA/WIEŚ) je wyłącza. Jawny kontrakt zamiast polegania na
    kolejności bloków - odporny na przestawienie sekcji w źródle.
    """
    w_ogolem = False
    for r in range(sh.nrows):
        kom0 = sh.cell_value(r, 0)
        if _czy_naglowek_sekcji(kom0):
            w_ogolem = str(kom0).strip().upper().startswith("OGÓŁEM")
            continue
        if not w_ogolem:
            continue
        rok = wyodrebnij_rok(kom0)
        if rok is not None:
            yield rok, r


def parsuj_tfr(sciezka):
    """{rok: TFR} z sekcji OGÓŁEM arkusza Tabl. V."""
    sh = xlrd.open_workbook(sciezka).sheet_by_name(ARKUSZ_TFR)
    return {rok: _komorka_liczba(sh.cell_value(r, KOL_TFR))
            for rok, r in _czytaj_sekcje_ogolem(sh)}


def parsuj_ruch_naturalny(sciezka):
    """{rok: {ludnosc, urodzenia, zgony}} z sekcji OGÓŁEM arkusza Tabl. I."""
    sh = xlrd.open_workbook(sciezka).sheet_by_name(ARKUSZ_RUCH)
    return {rok: {n: _komorka_liczba(sh.cell_value(r, k)) for n, k in KOL_RUCH.items()}
            for rok, r in _czytaj_sekcje_ogolem(sh)}


def zbuduj_ramke(sciezka, etykieta_zrodla="RD2024"):
    """Łączy oba parsery w jeden DataFrame z kolumną proweniencji `zrodlo`.

    Zwraca pełny zakres źródła (bez zawężania do lat projektu).
    Kolumny: rok, tfr, ludnosc, urodzenia, zgony, zrodlo.
    """
    tfr = parsuj_tfr(sciezka)
    ruch = parsuj_ruch_naturalny(sciezka)
    lata = sorted(set(tfr) | set(ruch))
    wiersze = [{
        "rok": rok,
        "tfr": tfr.get(rok),
        "ludnosc": ruch.get(rok, {}).get("ludnosc"),
        "urodzenia": ruch.get(rok, {}).get("urodzenia"),
        "zgony": ruch.get(rok, {}).get("zgony"),
        "zrodlo": etykieta_zrodla,
    } for rok in lata]
    return pd.DataFrame(wiersze)


def waliduj(df):
    """Kontrole spójności przed zapisem. Podnosi AssertionError przy anomalii."""
    assert df["rok"].is_unique, \
        "Zdublowane lata - sekcja OGÓŁEM przeciekła do MIASTA/WIEŚ."
    po_1970 = df[df.rok >= 1970]["rok"].tolist()
    assert po_1970 == list(range(1970, max(po_1970) + 1)), \
        "Dziura w ciągłości lat po 1970."
    tfr_realny = df["tfr"].dropna()
    assert tfr_realny.between(0.5, 8.0).all(), \
        "TFR poza fizycznie sensownym zakresem 0.5-8.0."
    luka = df[df.rok.between(1989, 2001)][["tfr", "ludnosc", "urodzenia", "zgony"]]
    assert luka.notna().all().all(), \
        "Luka 1989-2001 zawiera braki - niekompletne wypełnienie."


def znajdz_plik_tablic(katalog):
    """Zwraca ścieżkę do pliku '01_tablice...xls' w danym katalogu."""
    trafienia = list(Path(katalog).glob("01_tablice*.xls"))
    if not trafienia:
        raise FileNotFoundError(f"Brak pliku '01_tablice*.xls' w {katalog}")
    return trafienia[0]


def main():
    katalog_wej = Path("data/raw/rocznik")
    sciezka_wyj = Path("data/interim/rocznik_pelny.csv")

    plik = znajdz_plik_tablic(katalog_wej)
    df = zbuduj_ramke(plik)
    waliduj(df)

    sciezka_wyj.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(sciezka_wyj, index=False, encoding="utf-8")
    print(f"OK: {len(df)} wierszy ({df.rok.min()}-{df.rok.max()}) -> {sciezka_wyj}")


if __name__ == "__main__":
    main()
