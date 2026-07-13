"""Skrypt rozpoznawczy: pobiera zmienne z tematu P2346 (dzietnosc)."""
import requests

BASE = "https://bdl.stat.gov.pl/api/v1"

def zmienne_tematu(subject_id):
    """Pobiera wszystkie zmienne nalezace do danego tematu."""
    r = requests.get(f"{BASE}/variables",
                     params={"subject-id": subject_id,
                             "format": "json", "page-size": 100})
    r.raise_for_status()
    return r.json()["results"]

print("=== ZMIENNE W TEMACIE P2346 (dzietnosc i reprodukcja) ===")
for v in zmienne_tematu("P2346"):
    print(v["id"], "|", v.get("n1"), "|", v.get("n2"),
          "|", v.get("measureUnitName"))