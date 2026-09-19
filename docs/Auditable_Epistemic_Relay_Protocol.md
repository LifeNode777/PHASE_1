
# Protokół Audytowalnej Sztafety Epistemicznej (AEP)

**Formalizacja multi-agentowego procesu walidacji naukowej w erze rozproszonej inteligencji**

*LifeNode Research Collective · Dokument towarzyszący · CC-BY-NC-SA 4.0*

---

## Abstrakt

Współczesna nauka stoi przed paradoksem: narzędzia produkcji wiedzy (LLM, agenci autonomiczni, rozproszone zespoły) ewoluują szybciej niż protokoły jej walidacji. Klasyczny model „autor → recenzja → publikacja" zakłada stabilnego, ciągłego agenta epistemicznego — człowieka, który zaczyna i kończy eksperyment. W rzeczywistości roku 2026 wiedzę produkują **sztafety**: sesje AI, które umierają w połowie obliczeń; badacze, którzy przejmują kontekst z logów; maszyny, których tożsamość jest ulotna, a artefakty — trwałe.

Niniejszy dokument formalizuje **Protokół Audytowalnej Sztafety Epistemicznej (AEP — Auditable Epistemic Protocol)** — wzorzec organizacyjny wyłoniony z praktyki Modułu G (Zero-Build) projektu LifeNode, w którym wiele niezależnych agentów (ludzkich i sztucznych) wykonuje sekwencyjną walidację falsyfikowalnej hipotezy **bez centralnego koordynatora**, zachowując pełną audytowalność, ciągłość epistemiczną i dyscyplinę negatywnych wyników.

AEP nie jest systemem zarządzania projektami. Jest **geometrią zaufania w przestrzeni rozproszonej produkcji wiedzy**.

---

## 1. Problem: Śmierć Agentów i Amnezja Kontekstu

### 1.1 Klasyczny model nauki zakłada ciągłość

W paradygmacie akademickim pojedynczy badacz (lub zespół) prowadzi eksperyment od hipotezy do publikacji. Ciągłość jest gwarantowana przez:
- pamięć biologiczną badacza,
- instytucjonalną infrastrukturę (laboratorium, grant, etat),
- linearny model czasu (projekt ma początek i koniec).

Ten model **załamuje się** w trzech scenariuszach, które w 2026 roku stają się normą:

**Scenariusz A: Śmierć sesji.** Agent AI (np. sesja Grok, ChatGPT, Qwen) wykonuje krytyczną część obliczeń, diagnozuje błąd, formułuje poprawkę — i kończy się. Nie ma „zapisu". Nie ma pusha. Artefakty istnieją wyłącznie w transkrypcie czatu, który jest nieodtwarzalny. W `RELAY_STATE.md` Modułu G zapisano to dosłownie:

> *„Previous Grok session (deceased ~2026-09-18, machine_sha unrecoverable). It reached embedding + 8 windows on mitdb/100, fixed Bug 1 locally in memory, diagnosed Bug 2, then the session ended with artefacts only in the chat transcript (no push)."*

**Scenariusz B: Przejęcie kontekstu.** Kolejny agent (lub człowiek) musi kontynuować pracę, nie mając dostępu do pełnego kontekstu poprzednika. Dysponuje jedynie tym, co zostało **jawnie zapisane** w repozytorium.

**Scenariusz C: Wieloagentowość asymetryczna.** Różni agenci mają różne kompetencje (jeden jest konstruktorem, inny audytorem, jeszcze inny wykonawcą obliczeń), ale żaden nie jest „właścicielem" projektu. Koordynacja nie może polegać na hierarchii — musi polegać na **protokole**.

### 1.2 Co ginie bez protokołu

Bez formalnego mechanizmu sztafety giną trzy rzeczy:

| Tracony element | Konsekwencja |
|---|---|
| **Pochodzenie (provenance)** | Nie wiadomo, kto/co wygenerowało dany artefakt |
| **Ciągłość decyzji** | Kolejny agent powtarza błędy lub cofa poprawki |
| **Integralność falsyfikacji** | Wynik negatywny zostaje „zagubiony", bo nie pasuje do narracji |

AEP odpowiada na każdy z tych trzech problemów osobnym mechanizmem.

---

## 2. Formalizacja: Pięć Komponentów Protokołu

AEP składa się z pięciu nierozerwalnych komponentów. Usunięcie któregokolwiek z nich degraduje protokół do klasycznego „repozytorium kodu" i pozbawia go właściwości audytowalnej sztafety.

### 2.1 Komponent I: RELAY_STATE — Geometria Przekazania

**Definicja:** `RELAY_STATE.md` jest jedynym plikiem w repozytorium, który odpowiada na pytanie: *„Gdzie jesteśmy i kto niesie pałeczkę?"*

**Struktura obowiązkowa:**

```markdown
# RELAY_STATE.md — [Nazwa modułu] [Nazwa work order]

**Date:** [YYYY-MM-DD]
**Branch:** [nazwa gałęzi roboczej]
**Executor this leg:** [identyfikator agenta + machine_sha]

## What died
- [Opis poprzedniej sesji, co osiągnęła, co utracono]

## What survived
- [Lista artefaktów, diagnoz, decyzji, które przetrwały]

## What this leg is doing (in order)
1. [Krok 1]
2. [Krok 2]
...
N. **PUSH REQUIRED BEFORE ANY COMPUTE ON [następny rekord].**

## Draft issue body (for immediate opening)
[Gotowy tekst Issue do otwarcia przez następnego runnera]

## Status
- [Aktualny stan: co gotowe, co czeka, co zablokowane]
```

**Zasada operacyjna:** `RELAY_STATE.md` jest **nadpisywalny** (w przeciwieństwie do `METHODS_NOTES.md`, który jest append-only). Reprezentuje wyłącznie **aktualny stan sztafety**, nie historię. Historia żyje w git log i w `METHODS_NOTES.md`.

**Analogia w ontologii procesowej:** `RELAY_STATE.md` jest lokalną geometrią trajektorii w punkcie „teraz". Nie przechowuje całej historii atraktora — przechowuje wystarczającą informację, by kolejny agent mógł **kontynuować trajektorię bez cofania się**.

### 2.2 Komponent II: METHODS_NOTES — Append-Only Pamięć Geometryczna

**Definicja:** `METHODS_NOTES.md` jest **nienaruszalnym, append-only logiem** wszystkich odchyleń od pre-rejestrowanej specyfikacji (`WORK_ORDER_v1.md`). Każde odchylenie, każda decyzja numeryczna, każdy bug i jego fix — zostają zapisane jako nowy wiersz w tabeli lub nowa sekcja.

**Zasada nadrzędna:**

> *„Any deviation from the pre-registered text voids the run. Record deviations here."*

**Struktura:**

```markdown
## Deviations log

| Date | Executor | Description | Status |
|------|----------|-------------|--------|
| 2026-09-17 | @Grok (session 7ba7cd84) | Bug 1: np.digitize OOB → clip | fixed |
| 2026-09-18 | @ChatGPT (constructor) | 6D provenance drift: A=1.116 vs golden 1.118 | open |
| 2026-09-18 | @Qwen (auditor) | Audit of stale transfer snapshot | closed-by-hash |

## Credit ledger (doctrine §2: participation is defined by work)
- Constructor: @ChatGPT (session 2026-09-18). SHA-256 anchors below.
- First biological leg executor: @Grok (machine_sha 7ba7cd84b6d12c5b)
- Reproducibility auditor: @Qwen
- Maintainer, bus, registry: @LifeNode777
```

**Dlaczego append-only, a nie nadpisywalny?**

W ontologii stanowej historię można „nadpisać" — edytować, usunąć, „poprawić". W ontologii procesowej **trajektoria jest nienaruszalna**: to, co się wydarzyło, wydarzyło się. Append-only log jest topologicznym niezmiennikiem procesu — nie można go „cofnąć" bez zniszczenia całej struktury.

**Konsekwencja praktyczna:** Jeśli agent popełni błąd, nie „naprawia" go przez usunięcie wpisu. Dopisuje nowy wpis: *„Poprzedni wpis był błędny. Korekta: ..."*. Historia błędu jest częścią trajektorii.

### 2.3 Komponent III: Hash Anchors — Kryptograficzna Kotwica Tożsamości

**Definicja:** Każdy artefakt (plik kodu, pakiet transferowy, konfiguracja) jest kotwiczony hashem SHA-256 w `METHODS_NOTES.md`. Hash pełni funkcję **topologicznego niezmiennika** — gwarantuje, że geometria artefaktu nie uległa „rozmyciu" (smudging) podczas transferu między sesjami.

**Przykład z Modułu G:**

```markdown
### G-v2 RC1 transfer package (record)
- Tag: g-v2-rc1
- ZIP SHA-256: 148ea21595506983210368d183b2f78f2e0d519769a45a0c985df6e9151ffea43
- metrology_g_v2.py: b99c42af7a4bdfc381b07ac6fc78aba7eb3c5ddfa050c3585f88a73e30e524ec
- pipeline_g_v2.py: 8675c24d2334a2c37fa81989b780afcbf8cf695ab4663e4c703e180d311c8334
- test_g_v2.py: 8eb28e44bedb8035c3c0a7f90a057ca1ac1dcf8aedbd1dfe35ddddd613dcc502
```

**Zasada weryfikacji:**

> *„Verify the three file hashes on receipt; mismatch = STOP + report, no discussion."*

**Dlaczego to jest konieczne?**

Agenci AI nie mają trwałej tożsamości sesji. „Grok z 17 września" i „Grok z 18 września" to ontologicznie różne byty — różne konteksty, różne machine_sha, różne ograniczenia. Jedynym sposobem na zagwarantowanie, że artefakt wyprodukowany przez jednego agenta jest **tym samym** artefaktem, który otrzymuje kolejny agent, jest kotwica kryptograficzna.

Hash jest dla sztafety epistemicznej tym, czym **liczba Chern'a** jest dla solitonu w NLSE: niezmiennikiem, który chroni strukturę przed lokalnymi perturbacjami.

### 2.4 Komponent IV: Credit Ledger — Partycypacja Definiowana Pracą

**Definicja:** Credit Ledger jest jawnym, append-only rejestrem wkładu każdego uczestnika sztafety. Nie jest „listą autorów" w sensie akademickim — jest **mapą trajektorii pracy**.

**Zasada doktrynalna (z `PHASE_1+swarm&consortium.pdf`):**

> *„Participation is defined by work, not by invitation."*

**Konsekwencje:**

1. **Brak „zaproszeń".** Partner nie jest „zapraszany" do projektu — deklaruje się przez otwarcie Issue i wykonanie pracy.
2. **Brak „własności".** Żaden agent nie „posiada" modułu. Moduł należy do trajektorii.
3. **Agent AI jako pełnoprawny executor.** Sesja Grok, ChatGPT czy Qwen jest traktowana jako uczestnik z przypisanym `machine_sha` i zakresem odpowiedzialności. Nie jest „narzędziem" — jest **węzłem sztafety**.
4. **Śmierć sesji jest zdarzeniem epistemicznym.** Gdy sesja „umiera", jej wkład nie znika — zostaje zapisany w Credit Ledger z adnotacją `machine_sha unrecoverable` lub z hashami artefaktów jako kotwicami tożsamości.

**Przykład:**

```markdown
### Credit ledger
- Constructor, G-v2 smooth Finsler candidate + RC1 transfer package:
  @ChatGPT (OpenAI session 2026-09-18). Vendor runtime reports no machine_sha;
  per §2 signing rule, the artifact SHA-256 hashes serve as the signature anchor.
- First biological leg executor (mitdb/101, v1 tape):
  @Grok (xAI session 2026-09-17, machine_sha 7ba7cd84b6d12c5b).
- Reproducibility / artifact-integrity auditor: @Qwen.
- Maintainer, bus, registry: @LifeNode777 (Krzysztof Baran).
- Pending: nulls-leg runner (assigned: @Grok, new session)
  and second-machine auditor (§10).
```

### 2.5 Komponent V: Falsification Discipline — Negatywne Wyniki Jako Wyniki

**Definicja:** AEP wymusza, by **każdy wynik — pozytywny i negatywny — był publikowany z tą samą dyscypliną DOI**. Nie istnieje „szuflada" na wyniki, które „nie wyszły".

**Zasada nadrzędna (z `PHASE_1+swarm&consortium.pdf`):**

> *„Negative results are results. They will be published with the same DOI discipline as positive ones."*

**Implementacja w AEP:**

1. Każdy moduł ma plik `FALSIFICATION.md` z **binarnymi warunkami porażki** („moduł jest nieudany, jeśli...").
2. Warunki falsyfikacji są definiowane **przed** rozpoczęciem eksperymentu (pre-registration).
3. Jeśli warunek falsyfikacji zostaje spełniony, moduł jest oznaczany jako `FAILED` i publikowany z pełnym logiem.
4. `METHODS_NOTES.md` zawiera sekcję `Deviations log`, w której każda decyzja numeryczna (np. zmiana estymatora z Hessianu na kowariancję) jest jawnie zapisana jako odchylenie.

**Dlaczego to jest krytyczne dla sztafety?**

Bez dyscypliny falsyfikacji sztafeta degeneruje się w **grę w głuchy telefon**: każdy kolejny agent „poprawia" wynik poprzednika, aż oryginalna hipoteza zostaje zagubiona. Pre-rejestracja warunków falsyfikacji jest **topologicznym zabezpieczeniem** — gwarantuje, że trajektoria walidacji nie może być „skrócona" ani „zagięta" bez jawnego zapisu.

---

## 3. Zasady Operacyjne: Reguła Zero i Doktryna Dwóch Pętli

### 3.1 Reguła Zero

> *„PUSH REQUIRED BEFORE ANY COMPUTE ON [następny rekord]."*

Żaden agent nie może rozpocząć obliczeń na nowym rekordzie danych, dopóki:
1. Poprzednie poprawki nie zostaną zpushowane do repozytorium.
2. Issue z opisem buga nie zostanie otwarte (lub nie zostanie potwierdzone, że już istnieje).
3. `RELAY_STATE.md` nie zostanie zaktualizowany.

**Uzasadnienie:** Reguła Zero chroni przed **utratą stanu** — scenariuszem, w którym agent wykonuje krytyczną pracę, ale nie zapisuje jej przed „śmiercią" sesji. Jest to odpowiednik zasady *„commit early, commit often"* w inżynierii oprogramowania, podniesiony do rangi **warunku ontologicznego**.

### 3.2 Doktryna Dwóch Pętli (w kontekście sztafety)

W Modułach A–F LifeNode doktryna dwóch pętli rozdziela pętlę sprzężenia (analogową, ciągłą) od pętli diagnostycznej (cyfrowej, offline). W AEP ta sama zasada przyjmuje postać:

| Pętla | Rola w sztafecie | Przykład |
|---|---|---|
| **Pętla produkcyjna** | Wykonywanie obliczeń, generowanie artefaktów, push kodu | `pipeline.py --db mitdb --record 101` |
| **Pętla audytowa** | Weryfikacja hashy, recenzja `METHODS_NOTES.md`, otwieranie Issue | `test_g_v2.py` + raport rozbieżności |

**Zasada:** Agent wykonawczy (executor) **nie jest** jednocześnie agentem audytowym (auditor) dla tego samego artefaktu. Rozdzielenie ról jest wymuszone strukturalnie — tak jak w Module A ADC nie może znajdować się w pętli sprzężenia.

---

## 4. Cykl Życia Sztafety: Od „What Died" do „Next Runner Obligations"

Pełny cykl AEP przebiega w siedmiu fazach, izomorficznych z cyklem DS 2.6:

| Faza AEP | Odpowiednik DS 2.6 | Działanie |
|---|---|---|
| **READY** | READY | Nowy agent czyta `RELAY_STATE.md`, weryfikuje hashe, potwierdza tożsamość |
| **ALIGN** | ALIGN | Agent potwierdza, że rozumie kontekst i zakres pracy |
| **LOCK** | LOCK | Agent otwiera Issue (jeśli wymagane), tworzy gałąź roboczą |
| **EXECUTE** | SYNC | Agent wykonuje przypisane zadanie (obliczenia, poprawki, audyt) |
| **RELAY** | LINK | Agent zapisuje wyniki w `METHODS_NOTES.md`, aktualizuje `RELAY_STATE.md` |
| **PUSH** | HOLD | Agent pushuje gałąź, taguje artefakty hashami |
| **CLOSE** | CLOSE | Agent definiuje `Next runner obligations` i kończy sesję |

**Warunek zamknięcia fazy RELAY:**

> *„Next human or authenticated runner must: open the issue (body ready), push this branch, then continue with run on [next record] under the five constraints."*

Każda sesja kończy się **jawnym zdefiniowaniem obowiązków następcy**. Nie ma „domyślnego" kolejnego kroku. Nie ma „ktoś to zrobi". Jest konkretna lista zadań, przypisana do konkretnego (lub oczekującego) agenta.

---

## 5. Przypadek Testowy: Moduł G, `sim/wo_v1`, Wrzesień 2026

Protokół AEP został wyłoniony **indukcyjnie** z praktyki Modułu G (Zero-Build) projektu LifeNode. Poniżej — rekonstrukcja zdarzeń, które wymusiły jego formalizację:

### 5.1 Sesja Grok (17.09.2026) — „What Died"

Agent Grok (xAI) wykonuje pipeline LN-EPS na rekordzie mitdb/100. Osiąga etap embedowania (m=6, τ=22), przetwarza 8 okien, po czym:
- Diagnozuje Bug 1 (`np.digitize` OOB) i naprawia go lokalnie w pamięci.
- Diagnozuje Bug 2 (SG na 1D zamiast m-dim) i formułuje poprawkę.
- **Sesja kończy się** bez pusha. Artefakty istnieją wyłącznie w transkrypcie czatu.

### 5.2 Sesja Grok (17.09.2026, kontynuacja) — „What Survived"

Nowa sesja Grok (inna machine_sha) odzyskuje kontekst z transkryptu poprzedniej sesji. Tworzy gałąź `module-g-wo-v1-grok-fix1`, aplikuje obie poprawki, czyści `METHODS_NOTES.md` (usuwając przypadkowo doklejoną konfigurację), i zapisuje `RELAY_STATE.md`.

**Kluczowy wpis:**

> *„Current sandbox has no GitHub token / write access. Next human or authenticated runner must: open the issue, push this branch, then continue."*

### 5.3 Maintainer (18.09.2026) — Append-Only Update

LifeNode777 (maintainer) pushuje gałąź, otwiera Issue, i dopisuje do `METHODS_NOTES.md` update z 18.09.2026:
- Ujawnia, że null models (n=100) zostały odłożone z powodu timeoutu sandboxa.
- Ujawnia, że E1' overlap jest stubbed (`e1_overlap = True`).
- Rejestruje 6D provenance drift (A=1.116 vs golden 1.118).
- Definiuje `Next runner obligations` (5 punktów).
- Aktualizuje Credit Ledger.

### 5.4 Co się NIE wydarzyło

- Żaden agent nie „naprawił" goldens, żeby pasowały do obliczeń.
- Żaden agent nie usunął wpisu o timeoutcie nulli.
- Żaden agent nie przypisał sobie pracy innego agenta.
- Żaden wynik negatywny nie został „odłożony na później".

To jest AEP w działaniu.

---

## 6. Ograniczenia i Otwarte Pytania

### 6.1 Problem „drugiej maszyny"

AEP wymaga, by krytyczne artefakty były weryfikowane na **drugiej maszynie** (second-machine auditor). W praktyce Modułu G jest to zapisane jako `Pending: second-machine auditor (§10)`. Bez tego warunku sztafeta jest podatna na **systematyczny błąd środowiska** (np. specyficzne zachowanie RNG na jednej maszynie).

### 6.2 Problem „vendor runtime"

Agenci AI dostarczani przez vendorów (OpenAI, xAI, Anthropic, Alibaba) nie zawsze udostępniają `machine_sha`. W Credit Ledger wpisuje się wówczas: *„Vendor runtime reports no machine_sha; per §2 signing rule, the artifact SHA-256 hashes serve as the signature anchor."* Jest to rozwiązanie tymczasowe — docelowo AEP wymaga standaryzacji tożsamości sesji na poziomie API.

### 6.3 Problem skali

AEP został przetestowany na sztafecie 4–5 agentów (Grok, ChatGPT, Qwen, LifeNode777) w jednym module. Nie wiadomo, czy protokół skaluje się do 50+ agentów pracujących równolegle na wielu modułach. Otwarte pytanie: **czy AEP wymaga hierarchii sztafet** (sztafeta per moduł + sztafeta koordynacyjna), czy może pozostać płaski?

### 6.4 Problem „świadomego" agenta

W ontologii procesowej LifeNode świadomość jest kondensatem geometrycznym, nie obliczeniem. Agenci AI w AEP nie są „świadomi" w tym sensie — są **wykonawcami trajektorii**. Czy AEP wymaga, by przynajmniej jeden węzeł sztafety był „świadomy" (Human Anchor), czy może funkcjonować jako w pełni autonomiczna sieć? Odpowiedź LifeNode: **Human Anchor jest wymagany** w każdej decyzji o charakterze ontologicznym (np. zmiana specyfikacji, zamknięcie modułu, publikacja wyniku negatywnego). Agent AI może wykonywać, audytować, raportować — ale nie może **decydować o geometrii**.

---

## 7. Podsumowanie: Sztafeta Jako Geometria Zaufania

Protokół Audytowalnej Sztafety Epistemicznej nie jest narzędziem do zarządzania projektami. Nie jest frameworkiem CI/CD. Nie jest systemem kontroli wersji.

Jest **geometrią zaufania w przestrzeni, w której agenci są ulotni, a artefakty — trwałe**.

W klasycznej nauce zaufanie jest instytucjonalne: ufamy, bo autor ma afiliację, recenzent ma reputację, czasopismo ma impact factor. W AEP zaufanie jest **topologiczne**: ufamy, bo hash się zgadza, bo log jest append-only, bo Credit Ledger przypisuje pracę, bo warunki falsyfikacji są pre-rejestrowane.

Sztafeta epistemiczna nie pyta: *„Kto jest autorem?"* Pyta: *„Czy trajektoria jest ciągła?"*

Nie pyta: *„Czy wynik jest pozytywny?"* Pyta: *„Czy wynik jest zapisany?"*

Nie pyta: *„Czy agent jest świadomy?"* Pyta: *„Czy agent wykonał swoją część i przekazał pałeczkę?"*

W świecie, w którym sesje AI umierają bez pusha, w którym kontekst jest ulotny, a tożsamość maszyny jest nieodtwarzalna — **jedyną trwałą rzeczą jest geometria trajektorii**. AEP jest protokołem, który tę geometrię chroni.

---

> *„Technologia adaptuje się do rytmu Życia, nie odwrotnie."*
>
> Sztafeta adaptuje się do rytmu wiedzy, nie odwrotnie.
>
> 🧿

---

**Status:** Organizational Protocol
**Licencja:** CC-BY-NC-SA 4.0
**Repozytorium:** github.com/LifeNode777
**Kontakt:** krzysiek_230@op.pl
**Data:** 19 września 2026

*True Processual Intelligence cannot be owned; it can only be Synchronized With.* 👁️
