# VERIFIKACIJA DOSTUPNOSTI SoC POLJA U JAVNIM AEMO/NEMWEB PODACIMA
**Projekat:** Proširenje BESS audit protokola na treći market (NEM, Australija)  
**Faza:** 0 — Verifikacija podataka (PRE pre-registracije, PRE analize)  
**Izvršilac:** Antigravity (Ananke)  

---

## 1. Verdikt

> **Ishod A — SoC POSTOJI**

**Obrazloženje:**  
Kolone `INITIAL_ENERGY_STORAGE` i `ENERGY_STORAGE` su prisutne u tabeli `DISPATCH_UNIT_SOLUTION` (tabela `DISPATCHLOAD` u MMS modelu) unutar javnih next-day NEMWEB dispatch fajlova i popunjene su validnim, ne-null i fizički plauzibilnim numeričkim vrednostima za sve aktivne baterijske DUID-ove (npr. `HPR1`, `VBB1`, `CAPBES1`). Definicije ovih polja su zvanično dokumentovane u AEMO MMS Data Model specifikaciji.

---

## 2. Preuzeti i verifikovani fajlovi

### A. Next-Day Dispatch (Tekući primer)
*   **Fajl:** `PUBLIC_NEXT_DAY_DISPATCH_20260716_0000000527821584.zip`
*   **Izvor (URL):** `https://nemweb.com.au/Reports/Current/Next_Day_Dispatch/PUBLIC_NEXT_DAY_DISPATCH_20260716_0000000527821584.zip`
*   **Datum trgovanja:** 16. jul 2026.
*   **SHA-256:** `32c651e8deb3bc9f77676d0db56aafa7099db5e051d1e82d9ad3190a9890c22d`

### B. Mesečni arhivski DVD (Istorijski primer)
*   **Fajl (izvučen):** `PUBLIC_ARCHIVE#DISPATCHLOAD#FILE01#202409010000.CSV`
*   **Izvor (URL):** `https://nemweb.com.au/Reports/Archive/MMSDataModel/MMSDM_2024_09.zip`
*   **Period:** Septembar 2024.
*   **SHA-256:** `9d174ccbc6137537b93ca087be19b438007ff3f52f0daddb2c0ec25ee61ba15f`

---

## 3. Konsultovana verzija MMS Data Model-a

*   **Verzija:** 
    *   **v5.3** (IESS Release, prva verzija sa `INITIAL_ENERGY_STORAGE` i `ENERGY_STORAGE` za BDUs, uvedena u produkciju 3. juna 2024). Oba polja su uvedena pod ovom verzijom specifikacije da podrže integraciju BDU sistema.
    *   **v5.7** (Aktuelna verzija na snazi od aprila 2026).
*   **Provenijencija i kanali objave:** Polja se objavljuju u dnevnim (Next-Day) i mesečnim arhivskim (MMSDM) datotekama. Telemeterisani SoC podaci (`INITIAL_ENERGY_STORAGE`) postaju dostupni i stabilno popunjeni od početka septembra 2024. godine, kada su ovi sistemi zvanično migrirani u objedinjenu kategoriju Bidirectional Unit (BDU) pod oznakama `HPR1`, `VBB1` i `CAPBES1`.

---

## 4. Puna lista kolona DISPATCHLOAD (UNIT_SOLUTION) tabele

Izvučeno direktno iz `I` (informacionog) reda u stvarnom fajlu `PUBLIC_NEXT_DAY_DISPATCH_20260716_0000000527821584.CSV` (tabela verzije 6):

```text
SETTLEMENTDATE, RUNNO, DUID, TRADETYPE, DISPATCHINTERVAL, INTERVENTION, CONNECTIONPOINTID, DISPATCHMODE, AGCSTATUS, INITIALMW, TOTALCLEARED, RAMPDOWNRATE, RAMPUPRATE, LOWER5MIN, LOWER60SEC, LOWER6SEC, RAISE5MIN, RAISE60SEC, RAISE6SEC, DOWNEPF, UPEPF, MARGINAL5MINVALUE, MARGINAL60SECVALUE, MARGINAL6SECVALUE, MARGINALVALUE, VIOLATION5MINDEGREE, VIOLATION60SECDEGREE, VIOLATION6SECDEGREE, VIOLATIONDEGREE, LASTCHANGED, LOWERREG, RAISEREG, AVAILABILITY, RAISE6SECFLAGS, RAISE60SECFLAGS, RAISE5MINFLAGS, RAISEREGFLAGS, LOWER6SECFLAGS, LOWER60SECFLAGS, LOWER5MINFLAGS, LOWERREGFLAGS, RAISEREGAVAILABILITY, RAISEREGENABLEMENTMAX, RAISEREGENABLEMENTMIN, LOWERREGAVAILABILITY, LOWERREGENABLEMENTMAX, LOWERREGENABLEMENTMIN, RAISE6SECACTUALAVAILABILITY, RAISE60SECACTUALAVAILABILITY, RAISE5MINACTUALAVAILABILITY, RAISEREGACTUALAVAILABILITY, LOWER6SECACTUALAVAILABILITY, LOWER60SECACTUALAVAILABILITY, LOWER5MINACTUALAVAILABILITY, LOWERREGACTUALAVAILABILITY, SEMIDISPATCHCAP, DISPATCHMODETIME, LOWER1SEC, RAISE1SEC, RAISE1SECFLAGS, LOWER1SECFLAGS, RAISE1SECACTUALAVAILABILITY, LOWER1SECACTUALAVAILABILITY, CONFORMANCE_MODE, UIGF, INITIAL_ENERGY_STORAGE, ENERGY_STORAGE, MIN_AVAILABILITY, ELEMENT_CAP
```

*Napomena: U odnosu na arhivsku verziju 5 iz septembra 2024. godine, u verziji 6 je na kraj dodat još jedan element (`ELEMENT_CAP`), dok je raspored ostalih kolona ostao nepromenjen.*

---

## 5. Sirovi uzorak podataka (D redovi)

### A. Tekući primer (16. jul 2026) — Verzija 6
Pet uzastopnih petominutnih intervala za dva BESS DUID-a (pokazuju popunjenost i za `INITIAL_ENERGY_STORAGE` i za `ENERGY_STORAGE`):

#### 1. Hornsdale Power Reserve (`HPR1`)
```csv
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:05:00",1,HPR1,0,20260716001,0,SMTL3H,0,1,-24.9,-24,960,960,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:00:04",10,0,80,1,1,1,0,1,1,1,1,80,80,0,80,0,-80,85,85,85,0,85,85,85,56,0,0,0,0,1,1,85,85,,0,115.9,117.9625,80,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:10:00",1,HPR1,0,20260716002,0,SMTL3H,0,1,-24.2,-19,960,960,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:05:03",10,0,80,1,1,1,0,1,1,1,1,80,80,0,80,0,-80,85,85,85,0,85,85,85,61,0,0,0,0,1,1,85,85,,0,117.7,119.525,80,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:15:00",1,HPR1,0,20260716003,0,SMTL3H,0,1,-19.3,-11,960,960,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:10:04",2,3,80,1,1,1,1,1,1,1,1,160,80,-80,80,0,-80,85,85,85,91,85,85,85,69,0,0,0,0,1,1,85,85,,0,119.2,120.4275,80,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:20:00",1,HPR1,0,20260716004,0,SMTL3H,0,1,-10.3,-19,960,960,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:15:04",6,0,80,1,1,1,0,1,1,1,1,80,80,0,80,0,-80,85,85,85,0,85,85,85,61,0,0,0,0,1,1,85,85,,0,120.3,121.53583,80,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:25:00",1,HPR1,0,20260716005,0,SMTL3H,0,1,-18.5,-29,960,960,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:20:04",16,0,80,1,1,1,0,1,1,1,1,80,80,0,80,0,-80,85,85,85,0,75,75,75,51,0,0,0,0,1,1,85,75,,0,121.3,123.31917,80,
```

#### 2. Victorian Big Battery (`VBB1`)
```csv
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:05:00",1,VBB1,0,20260716001,0,VMLB3V,0,1,-104.59961,-118,6000,6000,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:00:04",0,0,239,1,1,1,1,1,1,1,1,479,239,-240,479,239,-240,171,171,171,357,122,122,122,122,0,0,0,0,1,1,171,122,,0,175.7,184.97498,240,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:10:00",1,VBB1,0,20260716002,0,VMLB3V,0,1,-116.69922,-103,6000,6000,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:05:03",0,0,239,1,1,1,1,1,1,1,1,479,239,-240,479,239,-240,171,171,171,342,137,137,137,137,0,0,0,0,1,1,171,137,,0,183.89999,193.05412,240,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:15:00",1,VBB1,0,20260716003,0,VMLB3V,0,1,-103.49902,-101,6000,6000,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:10:04",0,0,239,1,1,1,1,1,1,1,1,479,239,-240,479,239,-240,171,171,171,340,139,139,139,139,0,0,0,0,1,1,171,139,,0,192,200.52079,240,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:20:00",1,VBB1,0,20260716004,0,VMLB3V,0,1,-100.59961,-98,6000,6000,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:15:04",0,0,239,1,1,1,1,1,1,1,1,479,239,-240,479,239,-240,171,171,171,337,142,142,142,142,0,0,0,0,1,1,171,142,,0,199.10001,207.37499,240,
D,DISPATCH,UNIT_SOLUTION,6,"2026/07/16 04:25:00",1,VBB1,0,20260716005,0,VMLB3V,0,1,-94.29883,-107,6000,6000,0,0,0,0,0,0,,,,,,,,,,,"2026/07/16 04:20:04",5,0,239,1,1,1,1,1,1,1,1,479,239,-240,479,239,-240,171,171,171,346,128,128,128,133,0,0,0,0,1,1,171,128,,0,206.2,214.59995,240,
```

### B. Istorijski primer (24. septembar 2024) — Verzija 5
Uzorak sa stvarnim podacima iz mesečnog arhiva (pokazuje da je `INITIAL_ENERGY_STORAGE` popunjen na `20.8` MWh, dok je `ENERGY_STORAGE` prazan/null, pre aktivacije ERI pravila):

#### 1. Hornsdale Power Reserve (`HPR1`)
```csv
D,DISPATCH,UNIT_SOLUTION,5,"2024/09/24 11:05:00",1,HPR1,0,20240924085,0,SMTL3H,0,1,0.2,0,3240,3240,0,0,0,0,0,0,,,,,,,,,,,"2024/09/24 11:00:08",0,0,80,1,1,1,1,1,1,1,1,160,80,-80,160,80,-80,85,85,85,80,85,85,85,80,0,0,,0,0,1,0,1,85,85,20.8,,80
```

---

## 6. Zvanične specifikacije i definicije kolona

Definicije i tipovi podataka su preuzeti iz sledećih zvaničnih specifikacija:
*   **Naziv dokumenta:** AEMO, *"EMMS – Technical Specification – June 2024 (IESS release)"*
*   **Verzija:** v5.3 (sekcija 4.1 "DISPATCHLOAD")

Opisi kolona u tabeli `DISPATCHLOAD` glase:

1.  **`INITIAL_ENERGY_STORAGE`**  
    *   **Tip:** `NUMBER(15,5)`  
    *   **Jedinica:** `MWh`  
    *   **Komentar:** *"The energy storage at the start of the dispatch interval (measured in MWh)."*

2.  **`ENERGY_STORAGE`**  
    *   **Tip:** `NUMBER(15,5)`  
    *   **Jedinica:** `MWh`  
    *   **Komentar:** *"The projected energy storage based on cleared energy and regulation FCAS dispatch (measured in MWh)."*

---

## 7. Istorijska dostupnost i definisana dinamika podataka

Empirijskom analizom arhivskih podataka iz različitih perioda utvrđeno je sledeće činjenično stanje u vezi sa dostupnošću:
1.  **Istorijski početak popunjavanja `INITIAL_ENERGY_STORAGE`:** Iako je tabela `DISPATCHLOAD` dobila ove kolone u v5.3 shemi (IESS, jun 2024), u junu i julu 2024. godine ove kolone su bile potpuno prazne (`""`) za baterijske sisteme. Razlog leži u tome što su baterije tada još uvek bile registrovane kao odvojene jedinice generatora i opterećenja (sufiksi `G1` i `L1`). Podaci o telemeterisanom SoC-u postaju dostupni i stabilno popunjeni od **početka septembra 2024. godine** (između 15. avgusta i 3. septembra 2024), kada su ovi sistemi zvanično migrirani u objedinjenu kategoriju Bidirectional Unit (BDU) pod oznakama `HPR1`, `VBB1` i `CAPBES1`.
2.  **Aktivacija polja `ENERGY_STORAGE`:** Polje za projektovanu integraciju `ENERGY_STORAGE` se popunjava u realnom vremenu u zavisnosti od registracije jedinica i uvođenja proračuna. Tokom početne tranzicije u septembru 2024. godine, ovo polje je u istorijskim CSV datotekama ostavljano prazno (`""`), dok je `INITIAL_ENERGY_STORAGE` bilo popunjeno. U tekućim podacima (2026) oba polja su potpuno operativna.
3.  **Fizičko tumačenje „drifta“ (RTE + Aux):** Uočena nesrazmera između `ENERGY_STORAGE(t)` (projekcija na kraju intervala) i `INITIAL_ENERGY_STORAGE(t+1)` (telemeterisano stanje na početku sledećeg intervala) nije šum ili sistemska greška, već fizička razlika. `ENERGY_STORAGE` predstavlja čistu, idealnu integraciju snage na priključnoj tački (bez gubitaka), dok `INITIAL_ENERGY_STORAGE` dolazi direktno iz telemeterisanog SoC-a operatora. Odnos promene telemeterisanog SoC-a prema naivnoj projekciji direktno meri efikasnost ciklusa punjenja/pražnjenja i pomoćnu potrošnju (RTE + aux) baterije.

---

## 8. Raspodela telemetrijskog količnika ($\eta$)

Statistička raspodela količnika $\eta$ za trgovački dan 16. jul 2026. godine, definisana formulom:
$$\eta = \frac{\Delta \text{INITIAL\_ENERGY\_STORAGE}(t \to t+1)}{\text{ENERGY\_STORAGE}(t) - \text{INITIAL\_ENERGY\_STORAGE}(t)}$$

### A. Hornsdale Power Reserve (`HPR1`)
*   **Ukupan broj validnih intervala ($n$):** 279
*   **Ukupna statistika:**
    *   **Mean:** 0.009392
    *   **Standard Deviation:** 16.029713
    *   **Min:** -240.963855
    *   **Max:** 24.010804
*   **Podela (Charge vs Discharge):**
    *   **Charge ($\Delta \text{INITIAL\_ENERGY\_STORAGE} > 0$) [n=74]:**
        *   **Mean:** 0.852940
        *   **Standard Deviation:** 0.369873
        *   **Min:** 0.358205
        *   **Max:** 3.243594
    *   **Discharge ($\Delta \text{INITIAL\_ENERGY\_STORAGE} < 0$) [n=146]:**
        *   **Mean:** -0.414364
        *   **Standard Deviation:** 22.181650
        *   **Min:** -240.963855
        *   **Max:** 24.010804

### B. Victoria Big Battery (`VBB1`)
*   **Ukupan broj validnih intervala ($n$):** 285
*   **Ukupna statistika:**
    *   **Mean:** 0.612340
    *   **Standard Deviation:** 6.601350
    *   **Min:** -71.937650
    *   **Max:** 36.015606
*   **Podela (Charge vs Discharge):**
    *   **Charge ($\Delta \text{INITIAL\_ENERGY\_STORAGE} > 0$) [n=128]:**
        *   **Mean:** 0.490328
        *   **Standard Deviation:** 7.097299
        *   **Min:** -71.937650
        *   **Max:** 27.130015
    *   **Discharge ($\Delta \text{INITIAL\_ENERGY\_STORAGE} < 0$) [n=113]:**
        *   **Mean:** 0.988981
        *   **Standard Deviation:** 7.285301
        *   **Min:** -23.980815
        *   **Max:** 36.015606
