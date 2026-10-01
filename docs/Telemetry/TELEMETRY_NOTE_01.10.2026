# TELEMETRY NOTE 01.10.2026 — BONUS

## Dwie modalności akwizycji: payload opisowy vs payload wykonywalny (XPT vs PHASE_1)

**Obserwacja:** 2026-09-30, panele Traffic (XPT: okno 09/17–30; PHASE_1: okno 09/16–29)
**Kontekst:** w dniach poprzedzających pomiar w XPT commitowano artykuł opisowy w README, a w PHASE_1 — artefakty inżynieryjne (pliki aparatury Modułu H).

**Sygnatury ostatniego dnia okna:**

| Kanał | XPT (09/30) | PHASE_1 (09/29) |
|---|---:|---:|
| clones / unique cloners | 25 / 14 | 54 / 27 |
| views / unique visitors | 11 / 1 | 108 / 5 |
| clones ÷ views | 2,3 | 0,5 |
| cloners ÷ visitors | 14,0 | 5,4 |

**Wzorce:**
1. **XPT (proza):** umiarkowany skok klonów bez warstwy przeglądarkowej. Nowe tożsamości pojawiają się wyłącznie w przestrzeni klonów (14 cloners vs bazowe 3–5), unique visitors płaskie (1). Popular content płytkie (Overview 71/3). Sygnatura: fetch headless — klient git bez sesji HTTP (mirror/sync).
2. **PHASE_1 (artefakty):** równoczesny spike klonów i views, nadwyżka unique visitors (5 vs bazowe 2–3) oraz głęboka nawigacja po nowych ścieżkach (/tree/main/docs 42/2, MODULE_H… 20/2 i 18/1, docs/Telemetry 18/2). Sygnatura: inspekcja-then-fetch — przeglądanie drzewa, potem powtórne pobrania (~2 klony/cloner).
3. **Racjo okien:** clones/views = 60,9% (XPT) vs 33,3% (PHASE_1) — proporcja stabilnie rozdziela obie modalności także w sumach okien.

**Wnioski:**
- Triggerem pulsu w obu repo jest commit (sąsiedztwo 0–1 dnia); typ payloadu nie decyduje o obecności pulsu, lecz o **modalności akwizycji**: proza angażuje wyłącznie warstwę mirrorów, artefakt wykonywalny dodatkowo warstwę inspekcyjną (nowe tożsamości przeglądarkowe + nawigacja po ścieżkach).
- Kanały panelu Traffic to dwa detektory o różnych selektywnościach: kanał klonów widzi operacje git, kanał views widzi sesje HTTP. Aktor pobierający przez git bez otwarcia strony jest strukturalnie niewidzialny w kanale przeglądarkowym — brak visitors nie oznacza braku aktorów.
- „Unique visitors" nie jest licznikiem odbiorców, lecz licznikiem tożsamości przeglądarkowych; nowi odbiorcy mogą pojawić się wyłącznie w przestrzeni klonów i zostać przeoczeni przy obserwacji jednego kanału.
- Diagnostyka operacyjna: ilorazy clones÷views oraz cloners÷visitors działają jako wskaźnik modalności (headless: >1 i wysoki; inspekcyjna: <1 i umiarkowany).
- Dyscyplina metryk: clones ≠ readers, views ≠ readership; repozytoria porównywać sygnaturami kanałów, nie amplitudą pulsu.
