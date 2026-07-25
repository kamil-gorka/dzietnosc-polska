-- ============================================================
-- 01_schemat.sql
-- Schemat gwiazdy (star schema) dla analizy dzietności Polski.
--
-- Dwa wymiary (rok, grupa wieku) wspólne dla dwóch tabel faktów
-- o RÓŻNYM ZIARNIE:
--   fakt_roczny  — jeden wiersz na rok        (37 wierszy)
--   fakt_asfr    — jeden wiersz na rok+grupa  (168 wierszy)
--
-- Uruchamiane przez skrypt laduj_dane.py na świeżej bazie.
-- Kolejność CREATE ma znaczenie: wymiary PRZED faktami,
-- bo fakty odwołują się do nich kluczem obcym (FOREIGN KEY).
-- ============================================================

-- Włącz egzekwowanie kluczy obcych.
-- SQLite domyślnie ich NIE sprawdza (zaszłość historyczna) —
-- bez tej linii FOREIGN KEY byłby tylko dokumentacją, nie regułą.
PRAGMA foreign_keys = ON;

-- Idempotentność: kasujemy tabele, jeśli istnieją, zanim
-- utworzymy je od nowa. Dzięki temu skrypt można puścić
-- wielokrotnie i zawsze daje ten sam stan (reprodukowalność).
-- Kolejność DROP odwrotna do CREATE: najpierw fakty, potem
-- wymiary — inaczej FK zablokowałby skasowanie wymiaru,
-- do którego fakt się odwołuje.
DROP TABLE IF EXISTS fakt_asfr;
DROP TABLE IF EXISTS fakt_roczny;
DROP TABLE IF EXISTS wymiar_grupa_wieku;
DROP TABLE IF EXISTS wymiar_rok;


-- ------------------------------------------------------------
-- WYMIAR: rok
-- Jeden wiersz na każdy rok szeregu (1989–2025).
-- Atrybut zrodlo_tfr żyje TU (decyzja: proweniencja to cecha
-- roku, nie faktu) — RD2025 dla 1989–2001, BDL dla 2002+.
-- ------------------------------------------------------------
CREATE TABLE wymiar_rok (
    rok         INTEGER PRIMARY KEY,   -- klucz główny; naturalny, bo rok jest unikalny
    dekada      INTEGER NOT NULL,      -- pochodna: 1990, 2000, 2010... (do grupowania)
    zrodlo_tfr  TEXT    NOT NULL       -- 'RD2025' lub 'BDL' — skąd pochodzi TFR
);


-- ------------------------------------------------------------
-- WYMIAR: grupa wieku matki
-- Siedem grup pięcioletnich (15–19 ... 45–49).
-- Kolumna 'srodek' to środek przedziału (17.5, 22.5, ...) —
-- kluczowa, bo pozwala liczyć średni wiek matki W SQL-u
-- jako Σ(srodek × asfr) / Σ(asfr), zamiast wpisywać liczbę ręcznie.
-- ------------------------------------------------------------
CREATE TABLE wymiar_grupa_wieku (
    grupa_wieku TEXT PRIMARY KEY,      -- '15-19', '20-24', ... — klucz naturalny
    srodek      REAL    NOT NULL,      -- środek przedziału: 17.5 dla 15-19 itd.
    kolejnosc   INTEGER NOT NULL       -- 1..7 do sortowania (tekst '15-19' < '20-24' działa, ale to jawniej)
);


-- ------------------------------------------------------------
-- FAKT: dane roczne (ziarno = rok)
-- TFR, ruch naturalny, struktura ludności.
-- Kolumny struktury są NULLOWALNE — dla 1989–1994 BDL nie
-- publikuje podziału wg grup wieku, więc będą NULL.
-- NULL tu znaczy "brak danych", NIE "zero". To rozróżnienie
-- jest istotne: SUM() i AVG() ignorują NULL, więc statystyki
-- nie zostaną zafałszowane zerami, których nikt nie zmierzył.
-- ------------------------------------------------------------
CREATE TABLE fakt_roczny (
    rok                       INTEGER PRIMARY KEY,
    tfr                       REAL    NOT NULL,   -- kompletny dla 1989–2025
    urodzenia_zywe            INTEGER NOT NULL,   -- kompletny (ruch naturalny)
    zgony                     INTEGER NOT NULL,   -- kompletny
    ludnosc_przedprodukcyjna  INTEGER,            -- NULL dla 1989–1994
    ludnosc_produkcyjna       INTEGER,            -- NULL dla 1989–1994
    ludnosc_poprodukcyjna     INTEGER,            -- NULL dla 1989–1994

    -- Każdy rok w fakcie MUSI istnieć w wymiarze rok.
    FOREIGN KEY (rok) REFERENCES wymiar_rok (rok)
);


-- ------------------------------------------------------------
-- FAKT: ASFR (ziarno = rok × grupa wieku)
-- Cząstkowe współczynniki płodności. 24 lata × 7 grup = 168 wierszy.
-- Dwa klucze obce — to jest sedno gwiazdy: ten fakt wisi
-- na DWÓCH wymiarach jednocześnie.
-- Klucz główny złożony (rok, grupa) — para jednoznacznie
-- identyfikuje wiersz; nie ma dwóch ASFR dla tej samej pary.
-- ------------------------------------------------------------
CREATE TABLE fakt_asfr (
    rok          INTEGER NOT NULL,
    grupa_wieku  TEXT    NOT NULL,
    urodzenia    INTEGER NOT NULL,   -- urodzenia w tej grupie wieku matki
    kobiety      INTEGER NOT NULL,   -- liczebność kohorty (mianownik ASFR)
    asfr         REAL    NOT NULL,   -- urodzenia / kobiety

    PRIMARY KEY (rok, grupa_wieku),
    FOREIGN KEY (rok)         REFERENCES wymiar_rok (rok),
    FOREIGN KEY (grupa_wieku) REFERENCES wymiar_grupa_wieku (grupa_wieku)
);
