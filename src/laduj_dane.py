"""
laduj_dane.py — ładowanie danych z CSV do bazy SQLite.

Ostatni krok pipeline'u: pobierz -> zloz -> ZALADUJ DO SQL.

Buduje bazę od zera przy każdym uruchomieniu (idempotentnie):
  1. tworzy/otwiera plik data/processed/demografia.db
  2. wykonuje schemat z sql/01_schemat.sql (DROP + CREATE)
  3. ładuje dwa CSV do wymiarów i faktów
  4. weryfikuje integralność kluczy obcych

Uruchomienie (Anaconda Prompt, ze środowiskiem dzietnosc):
    python src/laduj_dane.py
"""

import sqlite3
from pathlib import Path

import pandas as pd

# ------------------------------------------------------------
# Ścieżki — zakotwiczone w korzeniu projektu, nie w katalogu
# uruchomienia. __file__ to ten plik (src/laduj_dane.py);
# .parent to src/, .parent.parent to korzeń dzietnosc-polska/.
# Dzięki temu skrypt działa niezależnie od tego, skąd go odpalisz.
# ------------------------------------------------------------
KORZEN = Path(__file__).resolve().parent.parent
KATALOG_DANYCH = KORZEN / "data" / "processed"
PLIK_BAZY = KATALOG_DANYCH / "demografia.db"
PLIK_SCHEMATU = KORZEN / "sql" / "01_schemat.sql"

CSV_ROCZNY = KATALOG_DANYCH / "dzietnosc_polska_1989_2025.csv"
CSV_ASFR = KATALOG_DANYCH / "asfr_polska_2002_2025.csv"

GRUPY = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
SRODKI = [17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5]


def utworz_schemat(con: sqlite3.Connection) -> None:
    """Wykonuje DDL z pliku 01_schemat.sql na podanym połączeniu."""
    ddl = PLIK_SCHEMATU.read_text(encoding="utf-8")
    con.executescript(ddl)
    print(f"[OK] schemat utworzony z {PLIK_SCHEMATU.name}")


def laduj_wymiar_rok(con: sqlite3.Connection, dr: pd.DataFrame) -> None:
    """Wymiar rok: rok + dekada (pochodna) + proweniencja TFR."""
    wymiar = pd.DataFrame({
        "rok": dr["rok"],
        "dekada": (dr["rok"] // 10) * 10,   # 1989 -> 1980, 1995 -> 1990 itd.
        "zrodlo_tfr": dr["zrodlo_tfr"],
    })
    wymiar.to_sql("wymiar_rok", con, if_exists="append", index=False)
    print(f"[OK] wymiar_rok: {len(wymiar)} wierszy")


def laduj_wymiar_grupa(con: sqlite3.Connection) -> None:
    """Wymiar grupy wieku: grupa + środek przedziału + kolejność."""
    wymiar = pd.DataFrame({
        "grupa_wieku": GRUPY,
        "srodek": SRODKI,
        "kolejnosc": range(1, len(GRUPY) + 1),
    })
    wymiar.to_sql("wymiar_grupa_wieku", con, if_exists="append", index=False)
    print(f"[OK] wymiar_grupa_wieku: {len(wymiar)} wierszy")


def laduj_fakt_roczny(con: sqlite3.Connection, dr: pd.DataFrame) -> None:
    """Fakt roczny: TFR, ruch naturalny, struktura (NULL dla 1989-1994)."""
    kolumny = [
        "rok", "tfr", "urodzenia_zywe", "zgony",
        "ludnosc_przedprodukcyjna", "ludnosc_produkcyjna", "ludnosc_poprodukcyjna",
    ]
    fakt = dr[kolumny].copy()
    # NaN w kolumnach struktury -> None (SQLite NULL), a nie 0.0.
    # to_sql tłumaczy NaN na NULL automatycznie; zostawiamy jako float.
    fakt.to_sql("fakt_roczny", con, if_exists="append", index=False)
    braki = con.execute(
        "SELECT COUNT(*) FROM fakt_roczny WHERE ludnosc_produkcyjna IS NULL"
    ).fetchone()[0]
    print(f"[OK] fakt_roczny: {len(fakt)} wierszy ({braki} z NULL w strukturze)")


def laduj_fakt_asfr(con: sqlite3.Connection, da: pd.DataFrame) -> None:
    """Fakt ASFR: rok x grupa wieku (168 wierszy)."""
    da.to_sql("fakt_asfr", con, if_exists="append", index=False)
    print(f"[OK] fakt_asfr: {len(da)} wierszy")


def sprawdz_integralnosc(con: sqlite3.Connection) -> None:
    """PRAGMA foreign_key_check zwraca wiersze łamiące klucze obce."""
    con.execute("PRAGMA foreign_keys = ON")
    naruszenia = con.execute("PRAGMA foreign_key_check").fetchall()
    if naruszenia:
        raise RuntimeError(f"Naruszenia kluczy obcych: {naruszenia}")
    print("[OK] integralność kluczy obcych: 0 naruszeń")


def main() -> None:
    KATALOG_DANYCH.mkdir(parents=True, exist_ok=True)

    # connect() tworzy plik bazy, jeśli nie istnieje.
    con = sqlite3.connect(PLIK_BAZY)
    try:
        con.execute("PRAGMA foreign_keys = ON")

        utworz_schemat(con)

        dr = pd.read_csv(CSV_ROCZNY)
        da = pd.read_csv(CSV_ASFR)

        # Kolejność ładowania: wymiary PRZED faktami (klucze obce).
        laduj_wymiar_rok(con, dr)
        laduj_wymiar_grupa(con)
        laduj_fakt_roczny(con, dr)
        laduj_fakt_asfr(con, da)

        sprawdz_integralnosc(con)
        con.commit()
        print(f"\n=== baza gotowa: {PLIK_BAZY} ===")
    finally:
        con.close()


if __name__ == "__main__":
    main()
