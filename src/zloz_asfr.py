"""
zloz_asfr.py
============
Buduje szereg cząstkowych współczynników płodności (ASFR) 2002-2025
i weryfikuje go przez odtworzenie TFR publikowanego przez GUS.

Wejście:
  - data/raw/urodzenia_roczniki.csv  (BDL P2167): urodzenia żywe wg
    pojedynczego rocznika wieku matki, 12 i mniej ... 50 i więcej.
  - data/raw/kohorty_kobiet.csv      (BDL P2137): liczebność kobiet
    w siedmiu grupach 5-letnich 15-19 ... 45-49, stan na 31.12.
  - data/raw/bdl_polska.csv          (BDL P2346): TFR jako wzorzec
    kontrolny.

Wyjście:
  - data/processed/asfr_polska_2002_2025.csv, format długi:
    rok, grupa_wieku, urodzenia, kobiety, asfr

Agregacja skrajów: roczniki ponizej 15 lat doliczane do grupy 15-19,
50 i wiecej do 45-49. Licznik obejmuje wtedy urodzenia matek spoza
przedzialu wiekowego mianownika - to swiadomy kompromis, zgodny z
praktyka GUS, i zrodlo czesci rozbieznosci w kontroli TFR.

Kontrola: TFR = suma(ASFR) * 5 powinna odtworzyc wskaznik GUS.
Zgodnosc nie bedzie idealna - mianownik BDL to stan na 31.12, a GUS
liczy ASFR na ludnosc w polowie roku. Prog akceptacji: 3% w kazdym
roku. Reszta powinna byc szumem, nie trendem - monotoniczny dryf
oznaczalby blad strukturalny (np. przesuniecie roku w zlaczeniu).

Uzycie:
    python src/zloz_asfr.py
"""

from pathlib import Path

import pandas as pd

KATALOG = Path(__file__).resolve().parent.parent

SCIEZKA_URODZENIA = KATALOG / "data" / "raw" / "urodzenia_roczniki.csv"
SCIEZKA_KOHORTY = KATALOG / "data" / "raw" / "kohorty_kobiet.csv"
SCIEZKA_BDL = KATALOG / "data" / "raw" / "bdl_polska.csv"
SCIEZKA_WYJ = KATALOG / "data" / "processed" / "asfr_polska_2002_2025.csv"

ROK_MIN = 2002
ROK_MAX = 2025

# Mapowanie rocznika wieku matki na grupe 5-letnia.
# Klucze to nazwy kolumn w urodzenia_roczniki.csv (stringi, tez dla liczb).
GRUPY = {
    "15-19": ["12 i mniej", "13", "14", "15", "16", "17", "18", "19"],
    "20-24": [str(w) for w in range(20, 25)],
    "25-29": [str(w) for w in range(25, 30)],
    "30-34": [str(w) for w in range(30, 35)],
    "35-39": [str(w) for w in range(35, 40)],
    "40-44": [str(w) for w in range(40, 45)],
    "45-49": [str(w) for w in range(45, 50)] + ["50 i więcej"],
}

TOLERANCJA = 0.03  # 3% wzglednej roznicy TFR


def sprawdz_kompletnosc(urodz):
    """Suma roczników musi odtworzyć kolumnę `ogółem`.

    Jesli nie odtwarza, w danych jest kategoria nieuwzgledniona w GRUPY
    (np. wiek nieustalony) i agregacja gubilaby czesc urodzen.
    """
    wszystkie = [k for lista in GRUPY.values() for k in lista]
    brakujace = [k for k in wszystkie if k not in urodz.columns]
    assert not brakujace, f"Brak kolumn w pliku urodzen: {brakujace}"

    suma = urodz[wszystkie].sum(axis=1)
    roznica = (suma - urodz["ogółem"]).abs()
    assert (roznica == 0).all(), (
        "Suma rocznikow nie odtwarza kolumny 'ogolem'. "
        f"Max roznica: {roznica.max()}. Sprawdz, czy plik nie zawiera "
        "kategorii wieku nieuwzglednionej w slowniku GRUPY."
    )


def agreguj_urodzenia(urodz):
    """Sumuje pojedyncze roczniki do siedmiu grup, zwraca format dlugi."""
    out = pd.DataFrame({"rok": urodz["rok"]})
    for grupa, kolumny in GRUPY.items():
        out[grupa] = urodz[kolumny].sum(axis=1)
    return out.melt(id_vars="rok",
                    var_name="grupa_wieku",
                    value_name="urodzenia")


def rozciagnij_kohorty(koh):
    """Zamienia format szeroki kohort na dlugi."""
    return koh.melt(id_vars="rok",
                    var_name="grupa_wieku",
                    value_name="kobiety")


def zloz(urodz_dl, koh_dl):
    """Zlacza licznik z mianownikiem i liczy ASFR.

    `how='inner'` jest tu celowe: automatycznie przycina do lat
    wspolnych dla obu zrodel. Jesli ktores zrodlo ma luke, wiersz
    zniknie zamiast dac ASFR z NaN w mianowniku.
    """
    df = urodz_dl.merge(koh_dl, on=["rok", "grupa_wieku"], how="inner")
    df = df[df["rok"].between(ROK_MIN, ROK_MAX)].copy()
    df["asfr"] = df["urodzenia"] / df["kobiety"]
    return df.sort_values(["rok", "grupa_wieku"]).reset_index(drop=True)


def waliduj_tfr(df, bdl):
    """Odtwarza TFR z ASFR i porownuje ze wskaznikiem GUS.

    Wypisuje tabele reszt rok po roku - sam fakt zmieszczenia sie w
    progu nic nie mowi o tym, czy blad jest szumem czy trendem.
    """
    tfr_obl = (df.groupby("rok")["asfr"].sum() * 5).rename("tfr_obliczony")
    tfr_gus = bdl.set_index("rok")["tfr"].rename("tfr_gus")

    por = pd.concat([tfr_obl, tfr_gus], axis=1, join="inner")
    por["roznica"] = por["tfr_obliczony"] - por["tfr_gus"]
    por["wzgledna_%"] = por["roznica"] / por["tfr_gus"] * 100

    print("\nKontrola: odtworzenie TFR z ASFR")
    print(por.round(4).to_string())
    print(f"\nMax |roznica wzgledna|: {por['wzgledna_%'].abs().max():.2f}%")
    print(f"Srednia roznica wzgledna: {por['wzgledna_%'].mean():.2f}%")

    korelacja = por.reset_index()[["rok", "wzgledna_%"]].corr().iloc[0, 1]
    print(f"Korelacja reszty z rokiem: {korelacja:.3f} "
          "(wartosc bliska +/-1 sugeruje dryf strukturalny)")

    assert por["wzgledna_%"].abs().max() < TOLERANCJA * 100, (
        "Odtworzony TFR odbiega od GUS o wiecej niz "
        f"{TOLERANCJA * 100:.0f}%. Sprawdz parowanie licznika z mianownikiem."
    )


def waliduj(df):
    """Kontrole struktury ramki przed zapisem."""
    lata = sorted(df["rok"].unique())
    assert lata == list(range(lata[0], lata[-1] + 1)), "Szereg lat nieciagly."
    assert df.groupby("rok").size().nunique() == 1, \
        "Nie kazdy rok ma komplet grup wiekowych."
    assert df["asfr"].notna().all(), "Brak ASFR w ktoryms wierszu."
    assert (df["asfr"] > 0).all(), "Niedodatni ASFR."
    assert (df["asfr"] < 0.3).all(), "ASFR poza sensownym zakresem."


def main():
    urodz = pd.read_csv(SCIEZKA_URODZENIA)
    koh = pd.read_csv(SCIEZKA_KOHORTY)
    bdl = pd.read_csv(SCIEZKA_BDL)

    # Kolumny roczników wczytują się jako nazwy tekstowe ('13', '14'...),
    # więc słownik GRUPY operuje na stringach - patrz komentarz przy GRUPY.
    urodz.columns = [str(c) for c in urodz.columns]

    sprawdz_kompletnosc(urodz)

    df = zloz(agreguj_urodzenia(urodz), rozciagnij_kohorty(koh))
    waliduj(df)
    waliduj_tfr(df, bdl)

    SCIEZKA_WYJ.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SCIEZKA_WYJ, index=False, encoding="utf-8")
    print(f"\nOK: {len(df)} wierszy ({df.rok.min()}-{df.rok.max()}, "
          f"{df.grupa_wieku.nunique()} grup) -> {SCIEZKA_WYJ}")


if __name__ == "__main__":
    main()