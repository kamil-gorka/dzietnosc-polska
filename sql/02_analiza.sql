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

-- ------------------------------------------------------------
-- DEKOMPOZYCJA KONTRFAKTYCZNA (walidacja Wykresu 6)
-- Rozkład spadku urodzeń 2002-2025 na efekt behawioralny (ASFR)
-- i efekt strukturalny (zmiana liczebności kohort kobiet).
--
-- Metoda: struktura wieku kobiet ZAMROŻONA na 2002 (nie 1995 —
-- 2002 to pierwszy rok z ASFR, baseline całego okna).
--   faktyczne      = Σ (asfr[rok] × kobiety[rok])       = urodzenia_zywe
--   kontrfaktyczne = Σ (asfr[rok] × kobiety[2002])
--   efekt struktury = faktyczne − kontrfaktyczne
--
-- Zamrożony mianownik to LICZEBNOŚCI kobiet (nie udziały procentowe).
-- ROUND tylko w warstwie prezentacji — sumy liczone na pełnej precyzji.
--
-- [FAKT EMPIRYCZNY] Zgodność z analizą w Pythonie:
--   Zmiana znaku efektu struktury między 2016 (+1030) a 2017 (-5281).
--   Efekt struktury w 2025 = -54454 urodzeń = 47,1% całego spadku
--   (spadek 2002->2025 = 115501; struktura odjęła 54454).
-- [TWIERDZENIE STRUKTURALNE] Efekt struktury nie jest przyczyną
--   niezależną — struktura wieku jest skutkiem dzietności sprzed
--   25-30 lat. Dywidenda strukturalna (szczyt +25646 w 2010) wygasa
--   monotonicznie i odwraca się, bo kohorty wyżu lat 80. wychodzą
--   z wieku rozrodczego, a wchodzą małe roczniki lat 90.
-- ------------------------------------------------------------
WITH struktura_2002 AS (
    SELECT
        grupa_wieku,
        kobiety AS kobiety_baza
    FROM widok_asfr
    WHERE rok = 2002
),
scenariusze AS (
    SELECT
        w.rok,
        SUM(w.asfr * w.kobiety)      AS faktyczne,
        SUM(w.asfr * s.kobiety_baza) AS kontrfaktyczne
    FROM widok_asfr AS w
    JOIN struktura_2002 AS s
        ON w.grupa_wieku = s.grupa_wieku
    GROUP BY w.rok
)
SELECT
    rok,
    ROUND(faktyczne)                  AS faktyczne,
    ROUND(kontrfaktyczne)             AS kontrfaktyczne,
    ROUND(faktyczne - kontrfaktyczne) AS efekt_struktury,
    CASE
        WHEN faktyczne >= kontrfaktyczne THEN 'sprzyja'
        ELSE 'odejmuje'
    END                               AS znak_efektu
FROM scenariusze
ORDER BY rok;