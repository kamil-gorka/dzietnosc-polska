"""Pobiera liczebność kobiet w grupach wieku 15-49 z GUS BDL.

Źródło: temat P2137 (Ludność wg grup wieku i płci), poziom krajowy.
Wynik: data/raw/kohorty_kobiet.csv
"""

from pathlib import Path

import pandas as pd
import requests

BASE = "https://bdl.stat.gov.pl/api/v1"
ROOT = Path(__file__).resolve().parent.parent
WYJSCIE = ROOT / "data" / "raw" / "kohorty_kobiet.csv"

ROK_OD = 1995
ROK_DO = 2025

# ID zmiennych BDL, temat P2137, przekrój: kobiety
KOHORTY = {
    "15-19": 72299,
    "20-24": 47738,
    "25-29": 47696,
    "30-34": 47695,
    "35-39": 47716,
    "40-44": 47698,
    "45-49": 47727,
}


def pobierz_zmienna(var_id, rok_od=ROK_OD, rok_do=ROK_DO):
    """Zwraca szereg czasowy jednej zmiennej BDL jako pd.Series."""
    lata = [("year", r) for r in range(rok_od, rok_do + 1)]
    r = requests.get(
        f"{BASE}/data/by-variable/{var_id}",
        params=[("format", "json"), ("unit-level", "0"), ("page-size", "100")] + lata,
    )
    r.raise_for_status()
    wartosci = r.json()["results"][0]["values"]
    return pd.Series({w["year"]: w["val"] for w in wartosci}, name=var_id)


def main():
    serie = {}
    for nazwa, var_id in KOHORTY.items():
        serie[nazwa] = pobierz_zmienna(var_id)
        print(f"{nazwa}: {len(serie[nazwa])} lat")

    kob = pd.DataFrame(serie)
    kob.index.name = "rok"

    WYJSCIE.parent.mkdir(parents=True, exist_ok=True)
    kob.to_csv(WYJSCIE)
    print(f"zapisano: {WYJSCIE}")


if __name__ == "__main__":
    main()