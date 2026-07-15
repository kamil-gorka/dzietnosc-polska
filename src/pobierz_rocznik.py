"""
pobierz_rocznik.py
==================
Pobiera i rozpakowuje tablice Rocznika Demograficznego GUS (ZIP -> XLS).

Domyślnie: Rocznik Demograficzny 2025 (najnowsza edycja, najdłuższy
zakres retrospektywny). Link zweryfikowany dosłownie ze strony GUS
(nie zgadnięty z wzorca URL).

Reprodukowalność: klon repo -> `python pobierz_rocznik.py` ->
`python parsuj_rocznik.py` odtwarza cały surowy zestaw danych rocznika.

Użycie:
    python pobierz_rocznik.py
"""

import zipfile
from pathlib import Path

import requests

# Link POTWIERDZONY ze strony https://stat.gov.pl/.../rocznik-demograficzny-2025,3,19.html
# (odczytany z HTML, nie zbudowany z wzorca - weryfikacja > zgadywanie)
URL_ROCZNIK_2025 = ("https://stat.gov.pl/download/gfx/portalinformacyjny/pl/"
                    "defaultaktualnosci/5515/3/19/1/"
                    "rocznik_demograficzny_2025_tablice.zip")

KATALOG_RAW = Path("data/raw/rocznik")
NAZWA_ZIP = "rocznik_demograficzny_2025_tablice.zip"


def pobierz(url, cel):
    """Pobiera plik ze strumieniowaniem, z obsługą błędów HTTP.

    stream=True + iter_content: nie wczytuje całości do pamięci (wzorzec
    skalowalny dla binariów). raise_for_status: HTTP 4xx/5xx -> wyjątek,
    zamiast cichego zapisu strony błędu jako pliku.
    """
    cel = Path(cel)
    cel.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=30) as resp:
        resp.raise_for_status()
        typ = resp.headers.get("Content-Type", "")
        if "zip" not in typ and "octet-stream" not in typ:
            print(f"  UWAGA: nieoczekiwany Content-Type: {typ!r}")
        with open(cel, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"  Pobrano: {cel} ({cel.stat().st_size / 1_048_576:.2f} MB)")
    return cel


def rozpakuj(sciezka_zip, katalog_docelowy):
    """Rozpakowuje ZIP i weryfikuje obecność pliku '01_tablice*.xls'.

    Dwuwarstwowa kontrola: is_zipfile (czy to w ogóle ZIP, nie strona 404)
    oraz obecność oczekiwanego pliku tablic (czy struktura się nie zmieniła).
    """
    katalog_docelowy = Path(katalog_docelowy)
    katalog_docelowy.mkdir(parents=True, exist_ok=True)
    if not zipfile.is_zipfile(sciezka_zip):
        raise ValueError(f"{sciezka_zip} nie jest prawidłowym ZIP-em "
                         f"(możliwe: pobrano stronę błędu zamiast pliku).")
    with zipfile.ZipFile(sciezka_zip) as z:
        z.extractall(katalog_docelowy)
        nazwy = z.namelist()
    tablice = [n for n in nazwy if Path(n).name.startswith("01_tablice")
               and n.lower().endswith(".xls")]
    if not tablice:
        raise FileNotFoundError(
            "Archiwum nie zawiera '01_tablice*.xls' - zmiana struktury rocznika?")
    print(f"  Rozpakowano {len(nazwy)} plików; tablice: {tablice[0]}")
    return katalog_docelowy / tablice[0]


def main():
    KATALOG_RAW.mkdir(parents=True, exist_ok=True)
    sciezka_zip = KATALOG_RAW / NAZWA_ZIP
    pobierz(URL_ROCZNIK_2025, sciezka_zip)
    plik_tablic = rozpakuj(sciezka_zip, KATALOG_RAW)
    print(f"OK: gotowe do parsowania -> {plik_tablic}")


if __name__ == "__main__":
    main()
