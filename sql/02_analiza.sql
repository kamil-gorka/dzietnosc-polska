-- ============================================================
-- 02_analiza.sql — zapytania analityczne nad schematem gwiazdy
-- Projekt: dzietnosc-polska
-- Baza: data/processed/demografia.db
-- Zależności: 01_schemat.sql (tabele) + loader CSV muszą być wykonane wcześniej
-- ============================================================
-- Konwencja: DBeaver służy do pisania/testowania; źródłem prawdy
-- jest ten plik (wersjonowany). Zapytania walidują wnioski
-- postawione wcześniej wizualnie (Wykresy 1-6, wnioski 1-3).
-- ============================================================


-- ------------------------------------------------------------
-- WIDOK: widok_asfr
-- Łączy fakt ASFR z wymiarem grupy wieku (dokleja srodek + kolejnosc).
-- Świadomie BEZ ORDER BY — sortowanie należy do zapytań nad widokiem,
-- nie do samej definicji widoku (widok to zbiór wierszy, nie ich kolejność).
-- ------------------------------------------------------------
CREATE VIEW widok_asfr AS
SELECT
    f.rok,
    f.grupa_wieku,
    g.srodek,
    g.kolejnosc,
    f.urodzenia,
    f.kobiety,
    f.asfr
FROM fakt_asfr AS f
JOIN wymiar_grupa_wieku AS g
    ON f.grupa_wieku = g.grupa_wieku;


-- ------------------------------------------------------------
-- TEST INTEGRALNOŚCI: domknięcie dwóch źródeł urodzeń
-- Sprawdza, że suma urodzeń po grupach wieku (fakt_asfr)
-- równa się urodzeniom żywym z ruchu naturalnego (fakt_roczny)
-- we wspólnym oknie 2002-2025.
-- Wynik oczekiwany: kolumna roznica = 0 we wszystkich 24 wierszach.
-- [FAKT EMPIRYCZNY] Potwierdzono: różnica zerowa dla całego okresu.
-- ------------------------------------------------------------
SELECT
    fr.rok,
    fr.urodzenia_zywe                     AS z_faktu_rocznego,
    SUM(fa.urodzenia)                     AS suma_z_asfr,
    fr.urodzenia_zywe - SUM(fa.urodzenia) AS roznica
FROM fakt_roczny AS fr
JOIN fakt_asfr AS fa
    ON fr.rok = fa.rok
GROUP BY fr.rok
ORDER BY fr.rok;


-- ------------------------------------------------------------
-- WALIDACJA WNIOSKU 3: średni wiek matki (MAB) 2002-2025
-- MAB = mean age at childbearing = średnia środków przedziałów
-- ważona ASFR-em (NIE surowymi urodzeniami!).
-- Ważenie ASFR-em eliminuje wpływ struktury wieku populacji —
-- mierzy czystą intensywność rodzenia w danym wieku, nie liczebność kohort.
-- [FAKT EMPIRYCZNY] Punkty kontrolne zgodne z analizą w Pythonie:
--   2002 -> 27,72 | 2013 -> 28,86 | 2025 -> 30,46
--   Przesunięcie +2,75 roku w 24 lata, trend ściśle monotoniczny.
-- ------------------------------------------------------------
SELECT
    rok,
    SUM(srodek * asfr) * 1.0 / SUM(asfr) AS mab
FROM widok_asfr
GROUP BY rok
ORDER BY rok;


-- ------------------------------------------------------------
-- FUNKCJE OKIENKOWE: zmiana rok-do-roku + skumulowany ubytek urodzeń
-- Źródło: fakt_roczny (urodzenia_zywe, pełne 1989-2025) — wybrane
-- zamiast fakt_asfr ze względu na zasięg (37 lat vs 24), po
-- potwierdzeniu przez test integralności, że oba źródła są tożsame.
--
-- LAG  -> zmiana rok-do-roku (lokalna). NULL dla 1989 (brak poprzednika).
-- SUM() OVER -> suma krocząca (skumulowana zmiana względem 1995).
--
-- CTE (WITH) konieczne: SQLite zabrania zagnieżdżania funkcji
-- okienkowej wewnątrz innej funkcji okienkowej. Pierwsze piętro
-- liczy zmianę (LAG), drugie sumuje ją narastająco (SUM OVER).
--
-- [FAKT EMPIRYCZNY] Test poprawności: skumulowana_zmiana w 2025
--   = -326136 = 238264 - 564400 (teleskopowo).
-- [TWIERDZENIE STRUKTURALNE] Krzywa skumulowana zawraca w górę
--   tylko raz (2003->2009, echo wyżu + wczesne polityki). Ślady
--   500+ (2016/17) spłaszczają ją chwilowo, ale nie odwracają
--   trajektorii — pod spodem pracuje kurcząca się struktura kohort.
-- ------------------------------------------------------------
WITH zmiany AS (
    SELECT
        rok,
        urodzenia_zywe,
        urodzenia_zywe - LAG(urodzenia_zywe) OVER (ORDER BY rok) AS zmiana_rdr
    FROM fakt_roczny
)
SELECT
    rok,
    urodzenia_zywe,
    zmiana_rdr,
    SUM(zmiana_rdr) OVER (ORDER BY rok) AS skumulowana_zmiana
FROM zmiany
ORDER BY rok;