# PRE-REGISTRACIONI PLAN ZA AUDIT SoC TELEMETRIJSKE EFIKASNOSTI AEMO BESS FLOTE
**Faza:** 1 — Metodologija i pre-registracija  
**Datum:** 18. jul 2026.  
**Izvršilac:** Antigravity (Ananke)  

---

## 1. Cilj audita

Cilj ovog audita je sistematska provera konzistentnosti i proračun efikasnosti ciklusa punjenja i pražnjenja (Round Trip Efficiency + pomoćna potrošnja) svih aktivnih baterijskih sistema registrovanih kao Bidirectional Units (BDU) na australijskom AEMO (NEM) tržištu. Audit se oslanja isključivo na javno dostupne telemeterisane podatke i projekcije iz tabele `DISPATCHLOAD`.

---

## 2. Vremenski i prostorni opseg (Scope)

### A. Vremenski opseg
- **Početak:** **12. septembar 2024. godine u 00:05:00** (trenutak aktivacije prvog jedinstvenog BDU zapisa u NEM-u).
- **Kraj:** **30. jun 2026. godine** (opseg od 21+ mesec, koji pruža dugoročnu statističku reprezentativnost i eliminiše sezonske confound-ere; kraj je fiksiran na 30.6.2026 radi celobrojnih meseci i da opseg bude zamrznut pre analize; jul 2026+ van opsega ove pre-registracije).

### B. Obuhvaćena flota (BESS Fleet)
U audit ulaze svi baterijski sistemi koji ispunjavaju sledeće kriterijume:
1. Registrovani su kao BDU (Bidirectional Unit) u tabeli `DISPATCHLOAD` u posmatranom periodu.
2. Imaju popunjena polja `INITIAL_ENERGY_STORAGE` i `ENERGY_STORAGE`.
3. Nazivna snaga sistema je $\ge 50$ MW.

**Primarna lista jedinica:**
- `HPR1` (Hornsdale Power Reserve)
- `VBB1` (Victorian Big Battery)
- `CAPBES1` (Capital BESS)
- *Napomena:* Jedinice koje su aktivirane tokom ovog perioda (npr. `KESSB1` nakon puštanja u rad) biće uključene od datuma njihove registracije kao BDU.

---

## 3. Metodologija i pravila računanja (Frozen Rules)

Proračun količnika $\eta(t)$ vrši se za svaki petominutni dispatch interval $t$ prema formuli:

$$\eta(t) = \frac{\text{INITIAL\_ENERGY\_STORAGE}(t+1) - \text{INITIAL\_ENERGY\_STORAGE}(t)}{\text{ENERGY\_STORAGE}(t) - \text{INITIAL\_ENERGY\_STORAGE}(t)}$$

Gde je:
- $\text{INITIAL\_ENERGY\_STORAGE}(t)$ telemeterisani SoC na početku intervala $t$.
- $\text{ENERGY\_STORAGE}(t)$ projektovani SoC na kraju intervala $t$, izračunat od strane AEMO na osnovu integracije dispatch instrukcija.

### A. Egzogena podela režima rada (TOTALCLEARED)
Podela na punjenje i pražnjenje vrši se isključivo na osnovu eksternog tržišnog signala targeta (`TOTALCLEARED`), a ne na osnovu smera promene SoC-a (kako bi se izbegla selekcija po ishodu):
- **Režim punjenja (Charge):** $TOTALCLEARED(t) < 0$ MWh.
- **Režim pražnjenja (Discharge):** $TOTALCLEARED(t) > 0$ MWh.
- Interval se odbacuje ako je $TOTALCLEARED(t) = 0$ (standby režim).

### B. Parametarski pragovi šuma ($\theta$)
Zbog ekstremne osetljivosti količnika na male vrednosti imenioca (u režimu mirovanja ili minimalnog rada, gde deljenje sa $\approx 0$ uzrokuje eksploziju vrednosti i visok standardni otklon), prag se ne fiksira na jedinstvenu vrednost, već se količnik $\eta$ analizira i prijavljuje kao funkcija praga:
- **Analizirani pragovi:** $\theta \in \{0.5, 1.0, 2.0, 5.0\}$ MWh.
- **Pravilo:** Za svaki prag $\theta$, interval se odbacuje ako je apsolutna projektovana promena SoC-a manja od tog praga:
  $$|\text{ENERGY\_STORAGE}(t) - \text{INITIAL\_ENERGY\_STORAGE}(t)| < \theta$$
- **Obrazloženje:** Prijavljivanjem celokupne krive $\eta(\theta)$ izbegava se selektivno biranje praga koji "pogoduje" određenom rezultatu. Stabilnost ili nestabilnost krive $\eta(\theta)$ kroz različite pragove predstavlja primarni nalaz audita.

### C. Dodatni uslovi za odbacivanje intervala
Interval $t$ se odbacuje iz proračuna ukoliko je ispunjen bilo koji od sledećih uslova:
1. **Null polja:** Bilo koje od 4 ključna polja (`INITIAL_ENERGY_STORAGE(t)`, `ENERGY_STORAGE(t)`, `INITIAL_ENERGY_STORAGE(t+1)`, `TOTALCLEARED(t)`) je prazno (`""` ili `NaN`).
2. **Vremenska diskontinualnost (Gaps):** Razlika između `SETTLEMENTDATE` za interval $t+1$ i interval $t$ nije tačno 5 minuta (npr. prekid u telemetriji ili prelazak na sledeći mesec/dan bez kontinualnosti).
3. **FCAS Regulation filter (Confound):** Dodeljena je FCAS Regulation obaveza za datu jedinicu u intervalu $t$ (`LOWERREG > 0` ili `RAISEREG > 0`). Ovo eliminiše van-intervalne komponente i osigurava da $\eta$ meri isključivo odziv na čistu energiju priključne tačke.

---

## 4. Statistički rezultati koji se prijavljuju

Za svaku baterijsku jedinicu i za svaki od četiri pre-registrovana praga $\theta \in \{0.5, 1.0, 2.0, 5.0\}$ MWh biće generisana tabela sa sledećim kolonama za oba režima rada (punjenje i pražnjenje):
- **Naziv jedinice (DUID)**
- **Režim rada (punjenje / pražnjenje)**
- **Prag $\theta$ (MWh)**
- **Ukupan broj intervala u sirovom opsegu ($N_{total}$)**
- **Broj odbačenih intervala po kategorijama:**
  - $N_{cleared=0}$ (TOTALCLEARED == 0)
  - $N_{noise}$ (imenilac $< \theta$ MWh)
  - $N_{null}$ (prazna polja)
  - $N_{gap}$ (diskontinuitet vremena / kraj dana)
  - $N_{fcas\_reg}$ (FCAS Regulation aktivnost: LOWERREG > 0 ili RAISEREG > 0)
- **Broj preživelih intervala ($n$)**
- **Statistika preživelih intervala:**
  - Srednja vrednost ($\text{mean}(\eta)$)
  - Standardni otklon ($\text{std}(\eta)$)
  - Minimalna i maksimalna vrednost ($\text{min}(\eta)$, $\text{max}(\eta)$)

---

## 5. Hipoteze za verifikaciju (Audit Claims)

Nakon izvršenja audita nad celokupnim istorijskim periodom, testiraće se sledeća primarna hipoteza (zasnovana na pilot opažanju 16.7.2026. godine za HPR1 i VBB1; predmet provere na punom istorijskom opsegu):
1. **Hipoteza o asimetriji stabilnosti i rekonsilijacije:**
   - Tokom **pražnjenja**, vrednost $\eta$ će pokazati stabilnost i rekonsilijaciju bližu vrednosti $1.0$ na zdravom uzorku $n$ kroz sve posmatrane pragove $\theta$ (sa sporim padom broja preživelih intervala $n$).
   - Tokom **punjenja**, vrednost $\eta$ će pokazati nestabilnost i visoku osetljivost na promenu praga $\theta$ (gde srednja vrednost značajno varira ili raste dok uzorak $n$ brzo opada ka nuli).

---

## 6. Minimalni pragovi izveštavanja (Scope Rules)

Kako bi se izbeglo prijavljivanje statističkih artefakata na suviše malim uzorcima:
- **Pravilo minimalnog uzorka:** Statistički rezultati (srednja vrednost, standardna devijacija) za par (jedinica, režim) se **neće prijavljivati** niti smatrati reprezentativnim ukoliko je broj preživelih intervala $n < 100$ za posmatrani prag $\theta$.
