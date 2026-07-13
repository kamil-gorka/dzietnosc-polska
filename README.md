# Kryzys dzietności w Polsce (1989–2025)
### Analiza eksploracyjna danych demograficznych GUS

> Od 1,99 do 1,10 dziecka na kobietę w 36 lat. Co dokładnie się wydarzyło i kiedy?

---

## Dlaczego ten projekt

Rok **1989** to pierwszy rok, w którym współczynnik dzietności (TFR) w Polsce spadł poniżej poziomu zastępowalności pokoleń (2,1). Rok **2024** przyniósł najniższy odczyt w historii pomiarów — **1,099**. Ten projekt rekonstruuje pełen łuk tego spadku na danych źródłowych GUS i sprawdza, **które składowe demograficzne za niego odpowiadają**.

Projekt nie zatrzymuje się na stwierdzeniu „dzietność spada". Pyta:
- Czy kobiety rodzą **mniej dzieci**, czy tylko **później**? (efekt *quantum* vs *tempo*)
- Kiedy nastąpiły punkty zwrotne i co się z nimi zbiegło?
- Jak zmieniała się struktura wieku matek i jak przekłada się to na liczbę urodzeń?

<!-- TODO: po ukończeniu analizy wstaw tu 1 kluczowy wykres jako "hero image" -->
<!-- ![Spadek TFR 1989-2025](figures/01_tfr_trend.png) -->

---

## Kluczowe wnioski

<!-- TODO: uzupełnić po analizie. Format: 3-5 punktów, każdy = jedno zdanie + liczba -->

1. *(do uzupełnienia)*
2. *(do uzupełnienia)*
3. *(do uzupełnienia)*

---

## Dane

| Źródło | Zakres | Format | Sposób pozyskania |
|---|---|---|---|
| [Bank Danych Lokalnych GUS](https://bdl.stat.gov.pl/bdl/) | 1995–2025 | JSON | REST API (`src/pobierz_bdl.py`) |
| [Rocznik Demograficzny GUS](https://stat.gov.pl/) | 1989–1994 | XLSX | pobranie ręczne |

**Uwaga metodologiczna o jakości danych:** BDL udostępnia dane od 1995 r., dlatego lata 1989–1994 uzupełniono z Rocznika Demograficznego. Połączenie dwóch źródeł o różnej strukturze udokumentowano w `notebooks/02_czyszczenie.ipynb`. Dane za 2025 r. mogą mieć charakter wstępny — GUS publikuje statystyki demograficzne z opóźnieniem (Q1–Q2 za rok poprzedni).

### Analizowane zmienne
- Współczynnik dzietności ogólnej (TFR)
- Urodzenia żywe i zgony (przyrost naturalny)
- Średni wiek matki przy urodzeniu dziecka
- Urodzenia według kolejności dziecka
- Struktura wieku kobiet w wieku rozrodczym (15–49)

---

## Struktura projektu

```
dzietnosc-polska/
├── data/
│   ├── raw/              # dane źródłowe — NIE MODYFIKOWAĆ
│   └── processed/        # dane po czyszczeniu, gotowe do analizy
├── notebooks/
│   ├── 01_pozyskanie.ipynb
│   ├── 02_czyszczenie.ipynb
│   └── 03_analiza_wizualizacja.ipynb
├── src/
│   └── pobierz_bdl.py    # klient API GUS BDL
├── sql/
│   └── analiza.sql       # zapytania analityczne
├── figures/              # wyeksportowane wykresy
├── docs/                 # dokumentacja i kontekst analityczny
├── environment.yml       # definicja środowiska (reprodukowalność)
└── README.md
```

---

## Jak odtworzyć analizę

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/<TWOJ_LOGIN>/dzietnosc-polska.git
cd dzietnosc-polska

# 2. Odtwórz środowisko
conda env create -f environment.yml
conda activate dzietnosc

# 3. Pobierz dane z API GUS
python src/pobierz_bdl.py

# 4. Uruchom notebooki
jupyter lab
```

---

## Stack technologiczny

**Python** (pandas, matplotlib, seaborn, requests) · **SQL** (SQLite) · **Jupyter** · **Git**

---

## Kontekst analityczny

Projekt wyrasta z szerszej analizy systemowej kryzysu demograficznego (`docs/`), w której zidentyfikowano m.in. rozróżnienie między **efektem tempo** (odraczanie urodzeń) a **efektem quantum** (realny spadek liczby dzieci). To rozróżnienie jest kluczowe: gdyby spadek TFR wynikał głównie z odraczania, byłby częściowo artefaktem pomiaru okresowego. Analiza danych sprawdza, która składowa dominuje.

---

## Autor

**Karol** · [LinkedIn](#) · [GitHub](#)

*Projekt portfolio — analiza danych.*
