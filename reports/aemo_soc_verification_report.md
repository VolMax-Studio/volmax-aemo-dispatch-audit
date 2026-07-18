# VERIFIKACIJA DOSTUPNOSTI SoC POLJA U JAVNIM AEMO/NEMWEB PODACIMA
**Projekat:** Proširenje BESS audit protokola na treći market (NEM, Australija)  
**Faza:** 0 — Verifikacija podataka (PRE pre-registracije, PRE analize)  
**Izvršilac:** Antigravity (Ananke)  

---

## 1. Verdikt

> **Ishod A — SoC POSTOJI (od 12. septembra 2024. godine)**

**Obrazloženje:**  
Kolone `INITIAL_ENERGY_STORAGE` i `ENERGY_STORAGE` su prisutne u tabeli `DISPATCH_UNIT_SOLUTION` (tabela `DISPATCHLOAD` u MMS modelu) unutar javnih next-day NEMWEB dispatch fajlova i popunjene su validnim, ne-null i fizički plauzibilnim numeričkim vrednostima za sve aktivne baterijske DUID-ove koji su registrovani kao Bidirectional Units (BDU) (npr. `HPR1`, `VBB1`, `CAPBES1`). 

Istorijska popunjenost ovih polja počinje od **12. septembra 2024. godine** (za `HPR1` i `CAPBES1`) odnosno **13. septembra 2024. godine** (za `VBB1`), kada su ovi sistemi zvanično migrirani iz odvojenih jedinica generatora i opterećenja (npr. `HPRG1` / `HPRL1`) u objedinjene BDU jedinice. Pre ovog datuma, kolone u MMS modelu su postojale (od v5.3 April 2024 specifikacije), ali su bile prazne jer BDU zapisi za baterije nisu postojali u sistemu.

Definicije ovih polja su zvanično dokumentovane u AEMO MMS Data Model specifikaciji.

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
    *   **EMMS – Technical Specification – Data Model v5.3** (April 2024). Oba polja (`INITIAL_ENERGY_STORAGE` and `ENERGY_STORAGE` za BDUs) su uvedena u ovoj verziji specifikacije.
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

Definicije i tipovi podataka su preuzeti iz sledeće zvanične specifikacije:
*   **Naziv dokumenta:** EMMS – Technical Specification – Data Model v5.3
*   **Verzija:** v5.3
*   **Datum:** April 2024
*   **URL:** [https://www.aemo.com.au/-/media/files/market-it-systems/der-guides/emms/emms-technical-specification-data-model-v53-april-2024.pdf?la=en](https://www.aemo.com.au/-/media/files/market-it-systems/der-guides/emms/emms-technical-specification-data-model-v53-april-2024.pdf?la=en)
*   **Tabela:** `DISPATCHLOAD` (sekcije 5.9/5.11/5.12)

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
1.  **Istorijski početak popunjavanja `INITIAL_ENERGY_STORAGE`:** Iako je tabela `DISPATCHLOAD` dobila ove kolone u v5.3 shemi (uvedenoj kroz IESS reforme), kolone su bile potpuno prazne (`""`) za baterijske sisteme tokom juna, jula i avgusta 2024. godine. Razlog je to što su baterije tada još uvek bile registrovane kao odvojene jedinice generatora i opterećenja (sufiksi `G1` i `L1`). 
    
    Prelazak na jedinstvene Bidirectional Units (BDU) i početak popunjavanja `INITIAL_ENERGY_STORAGE` odigrao se tačno:
    - Za **`HPR1`** i **`CAPBES1`**: **12. septembra 2024. godine u 00:05:00**
    - Za **`VBB1`**: **13. septembra 2024. godine u 00:05:00**

    Prethodni interval (2024/09/11 23:55:00) za HPR generator/load:
    ```text
    SettlementDate | DUID | INITIALMW | TOTALCLEARED | INITIAL_ENERGY_STORAGE | ENERGY_STORAGE
    2024/09/11 23:55:00 | HPRG1 | 0.1 | 0 | | 
    2024/09/11 23:55:00 | HPRL1 | 0 | 0 | | 
    ```

    Prvi interval sa aktiviranim BDU i popunjenim `INITIAL_ENERGY_STORAGE` (2024/09/12 00:05:00):
    ```text
    SettlementDate | DUID | INITIALMW | TOTALCLEARED | INITIAL_ENERGY_STORAGE | ENERGY_STORAGE
    2024/09/12 00:05:00 | HPR1 | 0 | 0 | 0 | 
    2024/09/12 00:05:00 | HPRG1 | 0 | 0 | | 
    2024/09/12 00:05:00 | HPRL1 | 0.9 | 0 | | 
    ```
    
    Ovo dokazuje da istorija BDU podataka u AEMO-u pokriva oko **22 meseca** (od septembra 2024. do jula 2026. godine), a ne 12 meseci kako se ranije pretpostavljalo.

2.  **Aktivacija polja `ENERGY_STORAGE`:** Polje za projektovanu integraciju `ENERGY_STORAGE` se popunjava u zavisnosti od uvođenja proračuna. Tokom početne tranzicije u septembru 2024. godine, ovo polje je u istorijskim CSV datotekama ostavljano prazno (`""`), dok je `INITIAL_ENERGY_STORAGE` bilo popunjeno. U tekućim podacima (2026) oba polja su potpuno operativna.

3.  **Osetljivost na šum (Drift):** 
    Razlika između `ENERGY_STORAGE(t)` i `INITIAL_ENERGY_STORAGE(t+1)` u sirovom obliku bez filtera sadrži visoku osetljivost na šum, jer mali imenilac (blizu nule, u režimima praznog hoda) dovodi do ekstremnih i nefizičkih vrednosti količnika $\eta$. Da bi se analizirala zavisnost raspodele od nivoa signala, uvodi se prag $\theta$ na apsolutnu vrednost imenioca.

---

## 8. Analiza telemetrijskog količnika ($\eta$) u funkciji praga $\theta$

Statistička analiza količnika $\eta$ za trgovački dan 16. jul 2026. godine (288 intervala), definisana formulom:
$$\eta(t) = \frac{\text{INITIAL\_ENERGY\_STORAGE}(t+1) - \text{INITIAL\_ENERGY\_STORAGE}(t)}{\text{ENERGY\_STORAGE}(t) - \text{INITIAL\_ENERGY\_STORAGE}(t)}$$

### Pravila računanja (zamrznuta pre pokretanja):
1.  **Podela po režimu rada (TOTALCLEARED):**
    - **punjenje**: `TOTALCLEARED < 0`
    - **praznjenje**: `TOTALCLEARED > 0`
    - `TOTALCLEARED == 0` se odbacuje.
2.  **Uslovi filtriranja i odbacivanja:**
    - Odbaci ako je imenilac $|ENERGY\_STORAGE(t) - INITIAL\_ENERGY\_STORAGE(t)| < \theta$ MWh.
    - Odbaci ako je bilo koje od 4 polja (`INITIAL_ENERGY_STORAGE(t)`, `ENERGY_STORAGE(t)`, `INITIAL_ENERGY_STORAGE(t+1)`, `TOTALCLEARED(t)`) prazno ili null.
    - Odbaci ako sledeći interval nije $t+5$ min (rupa u nizu / kraj dana).

### A. Hornsdale Power Reserve (`HPR1`)

| $\theta$ (MWh) | Režim | n | mean | sd | min | max | $n_{cleared=0}$ | $n_{\Delta < \theta}$ | $n_{null}$ | $n_{gap}$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.01 | punjenje | 80 | 0.6253 | 0.6010 | -1.3042 | 3.4278 | 184 | 0 | 0 | 1 |
| 0.01 | praznjenje | 23 | 1.0105 | 0.1552 | 0.7826 | 1.6000 | 184 | 0 | 0 | 1 |
| 0.50 | punjenje | 38 | 0.8179 | 0.1428 | 0.5277 | 1.0638 | 184 | 43 | 0 | 1 |
| 0.50 | praznjenje | 22 | 0.9837 | 0.0891 | 0.7826 | 1.1753 | 184 | 43 | 0 | 1 |
| 1.00 | punjenje | 29 | 0.8445 | 0.1316 | 0.5490 | 1.0638 | 184 | 52 | 0 | 1 |
| 1.00 | praznjenje | 22 | 0.9837 | 0.0891 | 0.7826 | 1.1753 | 184 | 52 | 0 | 1 |
| 2.00 | punjenje | 14 | 0.9047 | 0.0832 | 0.7924 | 1.0627 | 184 | 69 | 0 | 1 |
| 2.00 | praznjenje | 20 | 0.9934 | 0.0809 | 0.8175 | 1.1753 | 184 | 69 | 0 | 1 |
| 5.00 | punjenje | 0 | NaN | NaN | NaN | NaN | 184 | 88 | 0 | 1 |
| 5.00 | praznjenje | 15 | 1.0285 | 0.0523 | 0.9673 | 1.1753 | 184 | 88 | 0 | 1 |
| 10.00 | punjenje | 0 | NaN | NaN | NaN | NaN | 184 | 103 | 0 | 1 |
| 10.00 | praznjenje | 0 | NaN | NaN | NaN | NaN | 184 | 103 | 0 | 1 |

### B. Victoria Big Battery (`VBB1`)

| $\theta$ (MWh) | Režim | n | mean | sd | min | max | $n_{cleared=0}$ | $n_{\Delta < \theta}$ | $n_{null}$ | $n_{gap}$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.01 | punjenje | 52 | 0.7100 | 0.4919 | -1.5790 | 1.1321 | 201 | 0 | 0 | 1 |
| 0.01 | praznjenje | 34 | 1.0139 | 0.8842 | -0.4800 | 5.1646 | 201 | 0 | 0 | 1 |
| 0.50 | punjenje | 51 | 0.7549 | 0.3741 | -1.0100 | 1.1321 | 201 | 3 | 0 | 1 |
| 0.50 | praznjenje | 32 | 1.0077 | 0.8353 | -0.4800 | 5.1646 | 201 | 3 | 0 | 1 |
| 1.00 | punjenje | 46 | 0.8121 | 0.3192 | -1.0100 | 1.1321 | 201 | 9 | 0 | 1 |
| 1.00 | praznjenje | 31 | 0.8736 | 0.3555 | -0.4800 | 1.2823 | 201 | 9 | 0 | 1 |
| 2.00 | punjenje | 43 | 0.8081 | 0.3251 | -1.0100 | 1.1244 | 201 | 16 | 0 | 1 |
| 2.00 | praznjenje | 27 | 0.9077 | 0.3174 | -0.4800 | 1.2823 | 201 | 16 | 0 | 1 |
| 5.00 | punjenje | 20 | 0.8835 | 0.1186 | 0.5797 | 1.1244 | 201 | 51 | 0 | 1 |
| 5.00 | praznjenje | 15 | 0.9724 | 0.1441 | 0.7637 | 1.2823 | 201 | 51 | 0 | 1 |
| 10.00 | punjenje | 0 | NaN | NaN | NaN | NaN | 201 | 85 | 0 | 1 |
| 10.00 | praznjenje | 1 | 0.9930 | NaN | 0.9930 | 0.9930 | 201 | 85 | 0 | 1 |

### Napomena o interpretaciji
η se računa preko punog dana; distribucija zavisi od praga imenioca; interpretacija odložena do pre-registracije.
