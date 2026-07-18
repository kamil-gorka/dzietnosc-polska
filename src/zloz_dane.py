"""
zloz_dane.py
============
Złączenie dwóch źródeł GUS w jeden ciągły szereg 1989-2025.

Źródła:
  - BDL REST API (data/raw/bdl_polska.csv): TFR 2002-2025, ruch naturalny
    i ludność wg grup ekonomicznych 1995-2025.
  - Rocznik Demograficzny 2025 (data/interim/rocznik_pelny.csv): TFR
    i ruch naturalny 1946-2024, wypełnia lukę 1989-2001.

Walidacja nakładki (2002-2024, 23 lata) wykazała zgodność TFR co do
trzeciego miejsca dziesiętnego (max |różnica| = 0.0). Oba kanały
publikują tę samą produkcję GUS - zgodność potwierdza spójność
dystrybucji, nie stanowi niezależnego potwierdzenia metodologii.

Jednostki: rocznik podaje ruch naturalny w tysiącach z jednym miejscem
po przecinku (precyzja do 100 osób), BDL w sztukach. Dla lat 1995+
pierwszeństwo ma BDL jako dokładniejszy.

Użycie:
    python src/zloz_dane.py
"""

from pathlib import Path

import pandas as pd

SCIEZKA_BDL = Path("data/raw/bdl_polska.csv")
SCIEZKA_ROCZNIK = Path("data/interim/rocznik_pelny.csv")
SCIEZKA_WYJ = Path("data/processed/dzietnosc_polska_1989_2025.csv")

ROK_MIN = 1989
ROK_MAX = 2025
LUKA = (1989, 2001)          # lata, dla których BDL nie ma TFR
KOL_LICZEBNOSCI = [
    "urodzenia_zywe",
    "zgony",
    "ludnosc_przedprodukcyjna",
    "ludnosc_produkcyjna",
    "ludnosc_poprodukcyjna",
]


def przygotuj_luke(rocz):
    """Wycina z rocznika lata luki i przelicza tysiące na sztuki.

    Nie bierze kolumny `ludnosc` - rocznik podaje ludność ogółem, BDL
    rozbija ją na trzy grupy ekonomiczne. To nie są zamienniki, więc
    dla 1989-1994 grupy pozostają puste (świadoma decyzja projektowa).
    """
    luka = rocz[rocz["rok"].between(*LUKA)].copy()
    luka["urodzenia_zywe"] = (luka["urodzenia"] * 1000).round()
    luka["zgony"] = (luka["zgony"] * 1000).round()
    return luka[["rok", "tfr", "urodzenia_zywe", "zgony"]]


def zloz(bdl, luka):
    """Scala ramki kolumna po kolumnie, z pierwszeństwem dla BDL.

    `combine_first` bierze wartość z BDL, a gdy tam NaN - sięga do
    rocznika. Dzięki temu dla lat 1995-2001 TFR pochodzi z rocznika,
    ale ruch naturalny i ludność zostają z dokładniejszego BDL.
    Zwykłe `concat` + `drop_duplicates` wyrzuciłoby jedną z tych grup.
    """
    pelny = (bdl.set_index("rok")
                .combine_first(luka.set_index("rok"))
                .reset_index())
    pelny["zrodlo_tfr"] = pelny["rok"].apply(
        lambda r: "RD2025" if r <= LUKA[1] else "BDL"
    )
    for kol in KOL_LICZEBNOSCI:
        pelny[kol] = pelny[kol].astype("Int64")
    return pelny


def waliduj(df):
    """Kontrole przed zapisem. Podnosi AssertionError przy anomalii."""
    assert df["rok"].is_unique, "Zdublowane lata."
    assert list(df["rok"]) == list(range(ROK_MIN, ROK_MAX + 1)), \
        "Szereg lat nieciągły lub poza zakresem projektu."
    assert df["tfr"].notna().all(), "Brak TFR w którymś roku."
    assert df["tfr"].between(0.5, 8.0).all(), \
        "TFR poza fizycznie sensownym zakresem."
    assert df["urodzenia_zywe"].notna().all(), "Brak urodzeń w którymś roku."


def main():
    bdl = pd.read_csv(SCIEZKA_BDL)
    rocz = pd.read_csv(SCIEZKA_ROCZNIK)

    pelny = zloz(bdl, przygotuj_luke(rocz))
    waliduj(pelny)

    SCIEZKA_WYJ.parent.mkdir(parents=True, exist_ok=True)
    pelny.to_csv(SCIEZKA_WYJ, index=False, encoding="utf-8")
    print(f"OK: {len(pelny)} wierszy ({pelny.rok.min()}-{pelny.rok.max()}) "
          f"-> {SCIEZKA_WYJ}")


if __name__ == "__main__":
    main()