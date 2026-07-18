"""
sprawdzenie.py
==============
Skrypt roboczy: inspekcja surowego CSV z BDL przed złączeniem.

Wypisuje kształt, typy i pierwsze wiersze, oraz zakres lat z niepustym
TFR. Posłużył do ustalenia, że BDL ma TFR wyłącznie dla 2002-2025 -
co przesądziło o zakresie luki do wypełnienia z Rocznika (1989-2001)
i o zakresie nakładki walidacyjnej (2002-2024).

Nie jest częścią pipeline'u; zachowany jako ślad diagnostyczny.
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")

bdl = pd.read_csv(RAW / "bdl_polska.csv")
print(bdl.shape)
print(bdl.dtypes)
print(bdl.head())

print(bdl["tfr"].notna().sum())
print(bdl.loc[bdl["tfr"].notna(), ["rok", "tfr"]])