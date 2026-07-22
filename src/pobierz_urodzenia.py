"""Pobiera urodzenia żywe wg pojedynczych roczników wieku matki (BDL P2167)."""
from pathlib import Path

import pandas as pd
import requests

BASE = "https://bdl.stat.gov.pl/api/v1"
KATALOG_RAW = Path("data/raw")
SUBJECT = "P2167"

def pobierz_mape_zmiennych() -> dict[int, str]:
    """Zwraca {id_zmiennej: nazwa_rocznika} dla tematu P2167."""
    r = requests.get(
        f"{BASE}/variables",
        params={"subject-id": SUBJECT, "format": "json", "page-size": 100},
        headers={"Accept": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    return {v["id"]: v["n1"] for v in r.json()["results"]}


def pobierz_zmienna(var_id: int) -> pd.Series:
    """Pobiera jedną zmienną dla poziomu Polski. Zwraca Series indeksowaną rokiem."""
    r = requests.get(
        f"{BASE}/data/by-variable/{var_id}",
        params={"format": "json", "unit-level": 0, "page-size": 100},
        headers={"Accept": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    wyniki = r.json()["results"]
    if not wyniki:
        raise ValueError(f"Brak danych dla zmiennej {var_id}")

    wartosci = wyniki[0]["values"]
    return pd.Series(
        {int(w["year"]): w["val"] for w in wartosci},
        name=str(var_id),
    )

def pobierz_wszystkie() -> pd.DataFrame:
    """Pobiera wszystkie roczniki wieku matki. Kolumny = nazwy roczników."""
    mapa = pobierz_mape_zmiennych()

    serie = []
    for var_id, nazwa in mapa.items():
        s = pobierz_zmienna(var_id)
        s.name = nazwa
        serie.append(s)
        print(f"{nazwa:12} {s.index.min()}-{s.index.max()} ({len(s)})")

    return pd.concat(serie, axis=1).sort_index()

if __name__ == "__main__":
    urodzenia = pobierz_wszystkie()
    KATALOG_RAW.mkdir(parents=True, exist_ok=True)
    sciezka = KATALOG_RAW / "urodzenia_roczniki.csv"
    urodzenia.to_csv(sciezka, index_label="rok")
    print("zapisano:", sciezka.resolve())