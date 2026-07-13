"""Pobiera dane demograficzne dla Polski z API BDL GUS i zapisuje do CSV."""
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://bdl.stat.gov.pl/api/v1"
KATALOG_RAW = Path("data/raw")

# Mapa: co pobieramy. ID -> czytelna nazwa kolumny.
ZMIENNE = {
    59049: "tfr",                    # wspolczynnik dzietnosci ogolnej
    59:    "urodzenia_zywe",
    65:    "zgony",
    149:   "ludnosc_przedprodukcyjna",
    152:   "ludnosc_produkcyjna",
    155:   "ludnosc_poprodukcyjna",
}


def pobierz_zmienna(var_id: int) -> pd.DataFrame:
    """Pobiera jedna zmienna dla poziomu Polski. Zwraca DataFrame [rok, wartosc]."""
    r = requests.get(
        f"{BASE}/data/by-variable/{var_id}",
        params={"format": "json", "unit-level": 0, "page-size": 100},
        timeout=30,
    )
    r.raise_for_status()
    surowe = r.json()

    # Struktura: results -> [0] -> values -> [{year, val}, ...]
    wyniki = surowe["results"]
    if not wyniki:
        raise ValueError(f"Brak danych dla zmiennej {var_id}")

    wartosci = wyniki[0]["values"]

    return pd.DataFrame(
        {
            "rok": [int(w["year"]) for w in wartosci],
            "wartosc": [w["val"] for w in wartosci],
        }
    )


def main() -> None:
    KATALOG_RAW.mkdir(parents=True, exist_ok=True)

    ramki = []
    for var_id, nazwa in ZMIENNE.items():
        print(f"Pobieram {nazwa} (id={var_id})...", end=" ")
        df = pobierz_zmienna(var_id)
        df = df.rename(columns={"wartosc": nazwa})
        ramki.append(df.set_index("rok"))
        print(f"OK, {len(df)} lat ({df['rok'].min()}-{df['rok'].max()})")
        time.sleep(0.3)          # szanujemy limity API (5 zapytan/sekunde)

    # Laczymy wszystkie zmienne po roku
    dane = pd.concat(ramki, axis=1).sort_index().reset_index()

    sciezka = KATALOG_RAW / "bdl_polska.csv"
    dane.to_csv(sciezka, index=False, encoding="utf-8")

    print(f"\nZapisano: {sciezka}")
    print(f"Zakres lat: {dane['rok'].min()}-{dane['rok'].max()}, wierszy: {len(dane)}")
    print("\nPodglad:")
    print(dane.head(10).to_string(index=False))


if __name__ == "__main__":
    main()