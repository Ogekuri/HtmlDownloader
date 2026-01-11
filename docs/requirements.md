---
title: "Requisiti di HtmlDownloader"
description: Specifica dei requisiti software
version: "0.33"
date: "2026-01-11"
author: "Ogekuri"
scope:
  paths:
    - "**/*.py"
    - "**/*.ipynb"
    - "**/*.c"
    - "**/*.h"
    - "**/*.cpp"
  excludes:
    - ".*/**"
visibility: "draft"
tags: ["markdown", "requirements"]
---

# Requisiti di HtmlDownloader
**Versione**: 0.33
**Autore**: Ogekuri
**Data**: 2026-01-11

## Indice
- [Requisiti di HtmlDownloader](#requisiti-di-htmldownloader)
  - [Indice](#indice)
  - [1. Introduzione](#1-introduzione)
    - [1.1 Regole del documento](#11-regole-del-documento)
    - [1.2 Ambito del progetto](#12-ambito-del-progetto)
  - [2. Requisiti di progetto](#2-requisiti-di-progetto)
    - [2.1 Funzioni di progetto](#21-funzioni-di-progetto)
    - [2.2 Vincoli di progetto](#22-vincoli-di-progetto)
  - [3. Requisiti](#3-requisiti)
    - [3.1 Progettazione e implementazione](#31-progettazione-e-implementazione)
    - [3.2 Funzioni](#32-funzioni)
    - [3.3 Output del documento](#33-output-del-documento)
  - [4. Requisiti di test](#4-requisiti-di-test)
  - [5. Cronologia revisioni](#5-cronologia-revisioni)

## 1. Introduzione
### 1.1 Regole del documento
- Il documento deve essere redatto in italiano.
- I requisiti devono essere elencati come punti elenco usando i verbi "deve" o "must" per indicare azioni obbligatorie.
- Ogni ID requisito (PRJ, CTN, DES, REQ, TST) deve essere univoco.
- I prefissi degli ID devono seguire il gruppo: PRJ- per funzioni di progetto, CTN- per vincoli, DES- per progettazione/implementazione, REQ- per funzioni, TST- per test.
- Ogni requisito deve essere identificabile, verificabile e testabile.
- A ogni modifica si deve aggiornare data e versione in intestazione e corpo e aggiungere una riga alla cronologia revisioni.

### 1.2 Ambito del progetto
HtmlDownloader è un tool CLI che scarica contenuti HTML da URL e li rende disponibili offline con un file indice e risorse locali. Gestisce sia pagine TI "document-viewer" (applicazione JS) sia siti statici export Doxygen.

Struttura del progetto (escludendo percorsi nascosti):
```
HtmlDownloader/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── TODO.md
├── htmldownloader.sh
├── test.sh
├── venv.sh
├── docs/
│   ├── requirements.md
│   └── requirements_DRAFT.md
├── src/
│   └── htmldownloader/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
└── tech/
```

## 2. Requisiti di progetto
### 2.1 Funzioni di progetto
- **PRJ-001**: L'applicazione deve fornire una CLI per scaricare pagine TI "document-viewer" in formato offline leggibile.
- **PRJ-002**: L'applicazione deve supportare l'aggregazione di siti esportati con Doxygen in un unico documento offline con indice.
- **PRJ-003**: Il processo di download deve produrre `document.html`, `toc.html`, `index.html` (frameset con toc/documento) e la cartella `assets/` nella directory di destinazione.

### 2.2 Vincoli di progetto
- **CTN-001**: L'applicazione deve funzionare con Python ≥ 3.8 e dipende da `requests`, `beautifulsoup4` (parser `lxml`), `playwright` e `tqdm`.
- **CTN-002**: Per il downloader TI è necessario Chromium installato tramite `playwright install chromium` prima dell'esecuzione.
- **CTN-003**: Il crawler Doxygen deve limitarsi a un massimo di 250 pagine HTML per evitare download eccessivi.
- **CTN-004**: Tutti i percorsi di output devono essere risolti come percorsi assoluti e creati se mancanti.

## 3. Requisiti
### 3.1 Progettazione e implementazione
- **DES-001**: Il codice deve organizzare i downloader in classi derivate da `BaseDownloader` e registrarli tramite `DownloaderRegistry` per rilevamento dinamico.
- **DES-002**: Gli asset scaricati devono essere salvati in `assets/<host>/<path>` con nomi sanificati e creazione preventiva delle directory padre.
- **DES-003**: Il downloader TI deve usare Playwright in modalità headless per caricare la pagina, espandere e scorrere la TOC, visitare ogni link della TOC per scaricare il contenuto della relativa sezione, effettuare auto-scroll quando necessario, catturare le risposte immagine dal network, riscrivere i riferimenti degli asset verso percorsi locali, assegnare e normalizzare ID univoci per intestazioni e sezioni e serializzare offline un unico documento che unisca tutte le sezioni scaricate; dopo l'estrazione della TOC deve eliminare tutte le voci iniziali fino alla prima voce che inizia con "1 " (compresa la prima voce numerata) e deve rimuovere l'ultima voce se è "IMPORTANT NOTICE"; durante l'esportazione della sezione finale "IMPORTANT NOTICE" non deve copiare il blocco di disclaimer TI (il paragrafo lungo che inizia con "IMPORTANT NOTICE" e termina con Copyright 2024); se più sezioni risultano identiche deve mantenere una sola istanza di contenuto e far puntare le voci duplicate della TOC all'anchor già presente senza aggiungere sezioni di reindirizzamento nel documento.
- **DES-004**: Il downloader Doxygen deve effettuare crawling in ampiezza nell'ambito del percorso di origine, costruire sezioni `page-N` con titolo e contenuto principale estratto, quindi generare un documento unico con indice.
- **DES-005**: I download di asset devono usare sessioni HTTP riutilizzate con streaming a chunk e riscrivere i riferimenti HTML verso i percorsi locali offline.
- **DES-006**: Il rilevamento del downloader deve combinare regole su URL e, se necessario, analisi dell'HTML iniziale limitata per determinare il tipo corretto o segnalare errore.
- **DES-007**: I downloader devono rimuovere da `document.html` tutti i riferimenti a fogli di stile esterni, i tag di stile e gli attributi di stile inline, producendo un HTML privo di personalizzazioni estetiche del sorgente.
- **DES-008**: `index.html` deve essere un frameset con due frame affiancati: a sinistra `toc.html`, a destra `document.html`; i link della TOC devono aprire gli anchor nel frame destro.
- **DES-009**: I downloader devono onorare un limite opzionale di voci di TOC (`limit`) applicato dopo la pulizia della TOC: l'albero viene troncato alle prime `limit` voci in visita pre-order e solo le sezioni corrispondenti vengono scaricate e serializzate in `document.html`; per `doxygen-export` il limite si applica durante l'estrazione della TOC in ordine di lettura, terminando l'espansione quando sono state esplose le prime `limit` voci, e `document.html` deve essere generato seguendo le voci della TOC estratta e troncata nello stesso ordine, includendo solo i contenuti delle prime `limit` voci.
- **DES-010**: Il crawler `doxygen-export` deve utilizzare Playwright per caricare la TOC dal menu laterale (`#nav-tree-contents > ul`), simulare il click su tutte le voci espandibili fino a espandere completamente l'albero, catturare l'HTML risultante della TOC espansa e derivarne una rappresentazione testuale gerarchica; deve supportare una modalità "solo TOC" che salta il crawling delle pagine e la generazione di `document.html`, producendo file di output grezzi della TOC.
- **DES-011**: Il crawler `doxygen-export` deve utilizzare Playwright per estrarre la TOC dal selettore `#nav-tree-contents > ul`, simulare il click su tutte le voci espandibili fino a espandere completamente l'albero, catturare l'HTML risultante della TOC espansa e derivarne una rappresentazione testuale gerarchica; deve supportare una modalità "solo TOC" che salta il crawling delle pagine e la generazione di `document.html`, producendo file di output grezzi della TOC.
- **DES-012**: Il downloader Doxygen deve consolidare le voci della TOC che referenziano lo stesso contenuto del documento, assicurando che tutti i link della TOC puntino agli anchor corretti nel document.html esportato.
- **DES-013**: Durante l'esportazione di document.html, il downloader Doxygen deve escludere gli elementi TOC dal contenuto delle pagine per prevenire la duplicazione della navigazione nel documento finale.
- **DES-014**: I downloader devono implementare un metodo `post_process` comune che esegue una pipeline di operazioni di verifica dopo il completamento del download.
- **DES-015**: La pipeline di post-processing deve includere una verifica di congruità della TOC, controllando che ogni link presente in `toc.html` punti a un anchor esistente in `document.html` e che il testo del link corrisponda al contenuto dell'intestazione associata nel documento.
- **DES-016**: La pipeline di post-processing deve includere una verifica della profondità massima della TOC; se la profondità supera 6 livelli, deve essere emesso un warning.
- **DES-017**: La pipeline di post-processing deve includere una funzione che rimuove dalla TOC le voci a profondità >=7 e rimuove i prefissi di heading (come "1. ", "1.1. ") dalle voci della TOC e dai titoli delle intestazioni in document.html.
- **DES-018**: La pipeline di post-processing deve includere all'inizio una funzione `clean_document_style` che rimuove da `document.html` e `toc.html` tutti i riferimenti a fogli di stile esterni, tag di stile, attributi `style` e attributi `class`, producendo HTML privi di personalizzazioni estetiche.
- **DES-019**: L'output deve garantire che tutte le intestazioni `h1..h6` presenti in `document.html` siano referenziate da un `href` in `toc.html` tramite `id` diretto oppure tramite `id` del contenitore `div`/`section` che le contiene; inoltre ogni `href` della TOC deve referenziare un heading oppure un contenitore `div`/`section` che contiene almeno un heading.
- **DES-020**: La pipeline di post-processing deve includere una funzione `_test_toc_headings`, eseguita dopo `_enforce_toc_headings`, che verifica e blocca il rilascio del documento quando: (1) esistono heading `h1..h6` non referenziati dalla TOC né direttamente né tramite un contenitore `div`/`section`; (2) la TOC contiene `href` che non puntano a heading o contenitori con almeno un heading; (3) il livello della TOC non corrisponde al livello dell'heading (profondità 1 → `h1`, profondità 2 → `h2`, ecc.); la funzione deve riportare tramite `--verbose` le fasi del controllo e tramite `--debug` se una heading è referenziata per id o per contenitore.
- **DES-021**: La pipeline di post-processing deve includere una funzione `fix_heading_ref_position`, eseguita dopo `_test_toc_headings`, che garantisce che ogni `href` (fragment `#...`) presente in `toc.html` referenzi un elemento `h1..h6` in `document.html`; se un fragment referenzia un contenitore (`div`/`section` o equivalente) che contiene almeno un heading, l'`id` deve essere spostato dal contenitore al primo heading contenuto. Al termine, nessun `href` della TOC deve puntare a contenitori.
- **DES-022**: La pipeline di post-processing deve includere una funzione `fix_heading_numbering`, eseguita dopo `fix_heading_ref_position` e prima di `_test_toc_headings`, che esegue due operazioni: (1) rimuove il numbering pre-esistente dalle voci della TOC in `toc.html` e dai titoli delle intestazioni `h1..h6` in `document.html`, dove per numbering si intendono prefissi numerici del tipo "1 ", "1.", "1.2 ", "1.2.", "1.2.3 ", "1.2.3.", ecc.; (2) aggiunge il numbering coerente con posizione e livello nella TOC sia in `toc.html` sia in `document.html`, mantenendo corrispondenza tra testo della voce e testo dell'intestazione, a meno che non sia specificata l'opzione `--disable-numbering`.
- **DES-023**: Durante la generazione e/o post-processing di `document.html`, i downloader devono normalizzare tutti i collegamenti `<a href>` presenti nel documento in modo che ogni link sia: (1) un link esterno con schema esplicito (`http://`, `https://`, `ftp://`, `ftps://`, ecc.), oppure (2) un link ad anchor interno del solo tipo `#<id>` dove `<id>` esiste in `document.html`; tutti i link a documenti HTML (es: `qualcosa.html`, `document.html#...`) devono essere riscritti in `#<id>` quando risolvibili, altrimenti resi non cliccabili (rimozione di `href`).
- **DES-024**: Il codice deve introdurre un downloader `ResourceExplorerDownloader` modulare che seleziona un modulo in base all'HTML iniziale della pagina e delega il download al modulo attivato.
- **DES-025**: La pipeline di post-processing deve includere una funzione `_add_document_style`, eseguita dopo `_clean_document_style` e prima di `_normalize_document_links`, che aggiunge bordi alle tabelle e alle immagini in `document.html` iniettando stili CSS; le immagini che non sono contenute in una tabella devono ricevere un bordo con lo stesso spessore dei bordi delle tabelle (1px solid black).

### 3.2 Funzioni
- **REQ-001**: La CLI deve accettare `--from-url` e `--to-dir` obbligatori e `--user-agent` opzionale, creando la directory di destinazione se assente.
- **REQ-002**: L'applicazione deve identificare automaticamente quale downloader utilizzare e terminare con errore se non è determinabile.
- **REQ-003**: Per TI "document-viewer" deve scaricare tutte le sezioni referenziate dalla TOC remota a partire dalla prima voce che inizia con "1 " e fermarsi ai contenuti di "IMPORTANT NOTICE" (il blocco di disclaimer TI che segue non deve essere esportato), fonderle in un unico `document.html` con stile minimale e immagini salvate localmente, riscrivere i link asset, creare `toc.html` con TOC gerarchica ripulita dalle voci precedenti alla prima numerata e senza l'ultima voce "IMPORTANT NOTICE", generare `index.html` frameset che mostra a sinistra la TOC e a destra il documento navigabile tramite anchor, e inserire in apertura di `document.html` una riga di titolo ricavata dalla prima voce della TOC (o, se assente, dal titolo della prima sezione scaricata).
- **REQ-004**: Per export Doxygen deve scaricare e fondere le pagine HTML entro l'ambito individuato, riscrivere i link asset, scaricare le risorse con barra di avanzamento, creare `toc.html` con TOC gerarchica e generare `index.html` frameset che mostra a sinistra la TOC e a destra il documento navigabile tramite anchor.
- **REQ-005**: L'esecuzione deve stampare su stdout il downloader selezionato e i percorsi principali salvati; messaggi di avanzamento e di verifica devono essere mostrati solo quando attivati da `--verbose` o `--debug`.
- **REQ-006**: I nomi file derivati dagli URL devono essere sanificati (rimozione caratteri non validi, query fingerprint) per essere compatibili con il file system.
- **REQ-007**: `toc.html` generato da `document-viewer` e `doxygen-export` deve presentare un sommario gerarchico (TOC ad albero) coerente con la struttura delle sezioni esportate; per `document-viewer` la TOC deve iniziare dalla prima voce che inizia con "1 " e non deve contenere la voce finale "IMPORTANT NOTICE"; tutti i link della TOC devono puntare ad anchor esistenti dentro `document.html` e aprirsi nel frame destro del frameset; il titolo mostrato in `toc.html` deve essere "TOC" e non deve includere link "Apri documento completo".
- **REQ-008**: La CLI deve esporre le opzioni `--verbose` e `--debug`; per `document-viewer` `--verbose` deve mostrare gli avanzamenti dell'auto-scroll e l'esito dei check su estrazione/salvataggio di `toc.html` e `document.html`, mentre `--debug` deve includere questi dettagli; per `doxygen-export` `--verbose` deve mostrare gli avanzamenti dell'espansione della TOC e del download delle sezioni del documento, mentre `--debug` deve mostrare le informazioni di debug dell'esito delle operazioni utili alla comprensione di eventuali problematiche.
- **REQ-009**: La CLI deve esporre l'opzione opzionale `--limit <max>` (intero positivo) che tronca la TOC pulita alle prime `<max>` voci e interrompe il download/serializzazione delle sezioni a quel punto; `toc.html` e `document.html` devono contenere al massimo `<max>` voci/sezioni coerenti; valori non positivi devono causare errore di validazione.
- **REQ-012**: Dopo il completamento del download, i downloader devono eseguire automaticamente il post-processing per verificare l'integrità dei file generati.
- **REQ-013**: La CLI deve esporre l'opzione `--disable-numbering` che disabilita l'aggiunta del numbering durante `fix_heading_numbering` nel post-processing, mantenendo attiva la sola rimozione del numbering pre-esistente.
- **REQ-014**: Con `--verbose` i downloader devono stampare un riepilogo delle modifiche ai collegamenti in `document.html` (numero link analizzati, riscritti, rimossi e mantenuti); con `--debug` devono evidenziare esempi di collegamenti problematici e l'esito della risoluzione (riscritto vs rimosso).
- **REQ-015**: Per URL `https://dev.ti.com/tirex/explore/node` la CLI deve selezionare `ResourceExplorerDownloader`; se nessun modulo si attiva deve terminare con errore.
- **REQ-016**: Il modulo `RMModuleDoxigen` deve attivarsi quando la pagina contiene un `div.css-1aefuid-contentContainer` con un `iframe` o `frame` dotato di `src`, deve costruire l'URL Doxygen usando base `https://dev.ti.com/tirex/explore/` e delegare il download a `DoxygenExportDownloader` passando tutte le opzioni CLI (inclusi `--limit`, `--user-agent`, `--verbose`, `--debug`, `--disable-numbering`).
- **REQ-017**: La CLI deve esporre le opzioni `--version` e `--ver` che stampano su stdout solo la versione corrente del programma (es: `0.2.3`) e terminano immediatamente l'esecuzione (exit code 0), senza richiedere `--from-url`/`--to-dir` e senza altri messaggi.

### 3.3 Output del documento
- **REQ-010**: Il crawler `doxygen-export` deve inserire all'inizio di `document.html` una riga di titolo con il nome del documento ottenuto dall'intestazione superiore della pagina (`#titlearea`/`#projectname`/`#projectnumber` quando presenti); il titolo deve precedere tutte le sezioni scaricate.

## 4. Requisiti di test
| ID Requisito di Test | Requisito Collegato / Contesto | Procedura di Test |
|----------------------|--------------------------------|-------------------|
| **TST-001** | **REQ-003**, **DES-003** | Eseguire la CLI con un URL TI "document-viewer" e verificare che `document.html`, `index.html` e `assets/` contengano contenuti leggibili e immagini locali; controllare la presenza di ID sulle intestazioni e la navigabilità dell'indice. |
| **TST-002** | **REQ-004**, **DES-004** | Eseguire la CLI con un export Doxygen e verificare che il crawler rispetti il limite di 250 pagine, che `document.html` contenga sezioni `page-N` con titolo corretto e che gli asset siano referenziati localmente. |
| **TST-003** | **REQ-001**, **REQ-002** | Avviare la CLI con parametri obbligatori, verificare la selezione automatica del downloader o l'errore esplicito se il tipo non è determinabile, e controllare i messaggi su stdout. |
| **TST-004** | **DES-007**, **DES-008**, **REQ-007** | Eseguire entrambi i downloader su casi rappresentativi e verificare che `document.html` non contenga riferimenti a stylesheet o stili inline, che `toc.html` contenga il TOC gerarchico coerente con titolo "TOC" e senza link aggiuntivi al documento completo, e che `index.html` mostri due frame con TOC a sinistra e documento a destra, con link del TOC che navigano il documento. |
| **TST-008** | **DES-003**, **REQ-003**, **REQ-007** | Eseguire il downloader `document-viewer` su un caso con sezioni duplicate e verificare che `document.html` non contenga sezioni di reindirizzamento del tipo "Vedere ... →" e che le voci duplicate della TOC puntino all'anchor già presente nel documento senza aggiungere nuovi contenuti duplicati. |
| **TST-005** | **REQ-003**, **DES-003** | Eseguire la CLI con URL `https://www.ti.com/document-viewer/lit/html/sprz457` e verificare che `toc.html` contenga la tabella dei contenuti a partire dalla prima voce numerata ("1 Usage Notes and Advisories Matrices"), includa le voci intermedie fino a "Revision History" e non contenga la voce finale "IMPORTANT NOTICE"; verificare che siano presenti le voci attese: "1 Usage Notes and Advisories Matrices" con sottosezione "1.1 Devices Supported", sezione "2 Silicon Usage Notes and Advisories" con sottosezioni "2.1 Silicon Usage Notes" (contenente i2287, i2330, i2351, i2424) e "2.2 Silicon Advisories" (contenente tutti gli advisory ID da i2049 a i2482), più le sezioni "Trademarks" e "Revision History". |
| **TST-006** | **REQ-003**, **REQ-007**, **DES-003** | Dopo il download `document-viewer`, verificare che ogni link presente in `toc.html` (a partire dalla prima voce numerata) punti a un anchor esistente in `document.html`, che la TOC non contenga la voce "IMPORTANT NOTICE" e che l'apertura nel frame destro porti alla sezione corretta. |
| **TST-007** | **REQ-003**, **DES-003** | Eseguire la CLI con URL `https://www.ti.com/document-viewer/lit/html/sprz457` e verificare che `document.html` inizi dai contenuti dell'anchor corrispondente alla prima voce numerata ("1 Usage Notes and Advisories Matrices") e termini con la sezione "IMPORTANT NOTICE AND DISCLAIMER" priva del blocco di disclaimer TI (i paragrafi che iniziano con "TI PROVIDES TECHNICAL AND RELIABILITY DATA" e terminano con il copyright); controllare la presenza dei contenuti testuali principali (tabelle, usage notes i2287/i2330/i2351/i2424, advisory i2049/i2062/i2103/i2184/i2160/i2482, sezioni "1.1 Devices Supported", "2 Silicon Usage Notes and Advisories", "2.1 Silicon Usage Notes", "2.2 Silicon Advisories", "Trademarks", "Revision History") e l'assenza di duplicati della heading principale. |
| **TST-009** | **REQ-003**, **DES-003** | Eseguire il downloader `document-viewer` e verificare che `document.html` inizi con una singola riga di titolo uguale alla prima voce della TOC (o al titolo della prima sezione quando la TOC è assente) e che tale riga preceda tutte le sezioni scaricate. |
| **TST-010** | **REQ-009**, **DES-009** | Eseguire la CLI con `--limit <max>` su entrambi i downloader: verificare che `toc.html` contenga al massimo `<max>` voci in ordine coerente con la TOC pulita e che `document.html` contenga solo le sezioni corrispondenti, senza sezioni oltre la soglia. |
| **TST-011** | **REQ-004**, **REQ-009**, **DES-004**, **DES-009** | Eseguire la CLI sul Doxygen export `https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html` con `--limit 30` e verificare che `toc.html` e `document.html` contengano esclusivamente le prime 30 voci/sezioni (`page-1`...`page-30`) e nessuna voce o sezione oltre la soglia; tutti i link della TOC devono puntare ad anchor presenti in `document.html`; `toc.html` deve riportare le prime trenta voci in questo esatto ordine rispettando la gerarchia: Introduction, Getting Started, Migration Information, Block Diagram, Directory Structure, Licenses, Help and Support, Documentation Credits, Getting Started, Introduction, Getting Started Goals, Terms and Abbreviations, Getting Started Steps, Next Steps, Download, Install and Setup SDK and Tools, Host PC Requirements, Download and Install the SDK, Download and Install Additional SDK Tools, SysConfig, GCC AARCH64 Compiler, GCC ARM (R5) Compiler, Python3, OpenSSL, dfu-util, Windows, Steps to install windows generic USB drivers., Setps to Install drivers for using SBL DFU., Linux, PRU-CGT, Mono Runtime. |
| **TST-012** | **REQ-004**, **REQ-010** | Eseguire la CLI sul Doxygen export `https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html` e verificare che `document.html` inizi con una riga di titolo contenente "AM64x MCU+ SDK 11.02.00" estratta dall'intestazione superiore della pagina e che tale riga preceda tutte le sezioni scaricate. |
| **TST-013** | **DES-010** | Eseguire il test che istanzia direttamente il downloader `doxygen-export` con `toc_only=True`, estrae la TOC via Playwright, genera `toc_raw.html` e `toc_raw.txt` e verifica che corrispondano ai file di riferimento `src/tests/toc.html` e `src/tests/toc.txt`; il test confronta l'albero TOC espanso, ignorando la validazione del sotto-albero "API Reference". |
| **TST-014** | **DES-011** | Eseguire il test che istanzia direttamente il downloader `doxygen-export` con `toc_only=True`, estrae la TOC via Playwright dal selettore `#nav-tree-contents > ul`, genera `toc_raw.html` e `toc_raw.txt` e verifica che corrispondano ai file di riferimento `src/tests/toc.html` e `src/tests/toc.txt`; il test confronta l'albero TOC espanso, ignorando la validazione del sotto-albero "API Reference". |
| **TST-015** | **DES-012**, **DES-013** | Eseguire la CLI sul Doxygen export e verificare che le voci duplicate della TOC puntino agli anchor corretti nel document.html consolidato e che il contenuto delle pagine non contenga elementi TOC duplicati dalla navigazione originale. |
| **TST-016** | **DES-019**, **REQ-004** | Eseguire la CLI sul Doxygen export `https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html` con `--limit 30` e verificare che tutte le intestazioni `h1..h6` in `document.html` siano referenziate da un `href` in `toc.html` tramite `id` diretto o tramite `id` del contenitore `div`/`section` che le contiene; verificare inoltre che ogni `href` della TOC referenzi un heading o un contenitore che contiene almeno un heading. |
| **TST-017** | **DES-019**, **REQ-003** | Eseguire la CLI sul TI document-viewer `https://www.ti.com/document-viewer/lit/html/spradj8` e verificare che tutte le intestazioni `h1..h6` in `document.html` siano referenziate da un `href` in `toc.html` tramite `id` diretto o tramite `id` del contenitore `div`/`section` che le contiene; verificare inoltre che ogni `href` della TOC referenzi un heading o un contenitore che contiene almeno un heading. |
| **TST-018** | **DES-021** | Eseguire un download che produce `toc.html` e `document.html` e verificare che ogni `href` con fragment in `toc.html` punti a un elemento `h1..h6` in `document.html` (non a contenitori `div`/`section`). |
| **TST-019** | **DES-022**, **REQ-013** | Creare un output minimale con `toc.html` e `document.html` contenenti intestazioni `h1..h6` con id e voci TOC annidate, includendo prefissi numerici in formati diversi ("1 ", "1.", "1.2 ", "1.2.", ...). Eseguire `fix_heading_numbering` e verificare che: (1) i prefissi numerici pre-esistenti siano rimossi sia in TOC sia in intestazioni; (2) se `--disable-numbering` non è impostato, venga aggiunto un numbering coerente con il nesting della TOC e identico tra voce TOC e heading corrispondente; (3) se `--disable-numbering` è impostato, il numbering non venga aggiunto e TOC/intestazioni rimangano senza prefissi numerici. |
| **TST-020** | **DES-023**, **REQ-014** | Eseguire la funzione di test `test_sprz457_post_links` nel file `tests/test_sprz457.py` che, dopo aver garantito la presenza del download, verifica tutti i link `<a href>` presenti in `temp/test_sprz457/document.html`: sono ammessi solo link esterni con schema (`http://`, `https://`, `ftp://`, `ftps://`, ecc.) oppure link interni del tipo `#<id>` dove `<id>` esiste nel documento; ogni altro tipo di link deve causare fallimento del test. |
| **TST-021** | **DES-023**, **REQ-014** | Eseguire la funzione di test `test_spradj8_post_links` nel file `tests/test_spradj8.py` con le stesse regole di validazione link di TST-020 su `temp/test_spradj8/document.html`. |
| **TST-022** | **DES-023**, **REQ-014** | Eseguire la funzione di test `test_api_guide_post_links` nel file `tests/test_api_guide_limit.py` con le stesse regole di validazione link di TST-020 su `temp/test_api_guide_am64x/document.html`. |
| **TST-023** | **REQ-015**, **REQ-016**, **DES-024** | Eseguire la CLI con `https://dev.ti.com/tirex/explore/node?node=A__AD2nw6Uu4txAz2eqZdShBg__DIGITAL-POWER-SDK-AM263X__k-hvNHd__LATEST` e `--limit 30`; verificare che la CLI completi con successo, che `toc.html` e `document.html` esistano, che `toc.html` contenga 30 voci, che ogni link della TOC punti a un anchor presente in `document.html` e che gli eventuali anchor `page-*` non superino `page-30`; verificare inoltre che l'output indichi `resource-explorer` come downloader selezionato. |
| **TST-024** | **REQ-017** | Eseguire il parser della CLI con `--version` e con `--ver` e verificare che: (1) la CLI termini immediatamente con exit code 0; (2) stdout contenga esclusivamente la stringa della versione seguita da newline (`<versione>\n`), senza altri messaggi. |

## 5. Cronologia revisioni
| Data | Versione | Motivazione e descrizione cambiamento |
|------|----------|---------------------------------------|
| 2026-01-11 | 0.33 | Aggiunto comando CLI `--version`/`--ver` per stampare la versione del programma e terminare immediatamente; aggiunto requisito REQ-017 e test TST-024. |
| 2026-01-11 | 0.32 | Consolidati i test post-link TST-020, TST-021, TST-022 nei rispettivi file di test di download, eliminando i file separati e la dipendenza dalla variabile d'ambiente RUN_POST_LINK_TESTS. |
| 2026-01-10 | 0.31 | Estesa funzione `_add_document_style` per aggiungere bordi anche alle immagini non contenute in tabelle, con lo stesso spessore dei bordi delle tabelle. |
| 2026-01-10 | 0.30 | Aggiunta funzione `_add_document_style` nella pipeline di post-processing per aggiungere bordi alle tabelle in document.html. |
| 2026-01-10 | 0.29 | Aggiunto ResourceExplorerDownloader modulare con RMModuleDoxigen e test limit 30 su dev.ti.com. |
| 2026-01-10 | 0.28 | Aggiunta normalizzazione dei link in document.html per consentire solo link esterni con schema o anchor interni `#id`, con logging `--verbose/--debug` e tre test finali di verifica su output in temp/. |
| 2026-01-10 | 0.27 | Aggiunta funzione `fix_heading_numbering` nella pipeline di post-processing e nuova opzione CLI `--disable-numbering` per disabilitare l'aggiunta del numbering mantenendo la rimozione dei prefissi numerici. |
| 2026-01-10 | 0.26 | Aggiunta funzione `_test_toc_headings` alla pipeline di post-processing con logging dettagliato per garantire coerenza tra TOC e heading e il rispetto dei livelli TOC↔heading. |
| 2026-01-09 | 0.25 | Aggiunta verifica di consistenza TOC↔heading: tutte le intestazioni `h1..h6` devono essere referenziate dalla TOC e ogni href della TOC deve referenziare un heading o un contenitore con heading; aggiunti requisiti di test dedicati. |
| 2026-01-09 | 0.24 | Aggiunta funzione clean_document_style nella pipeline di post-processing per rimuovere riferimenti a stili da document.html e toc.html; aggiornati versione e data. |
| 2026-01-09 | 0.23 | Rimossa opzione CLI `--toc-only` e relativo requisito REQ-011; aggiornati test TST-013 e TST-014 per istanziare direttamente il downloader con toc_only=True e generare toc_raw files nei test; aggiornati versione e data. |
| 2026-01-09 | 0.22 | Aggiunta funzione di post-processing per rimuovere voci TOC a profondità >=7 e prefissi di heading dalle voci TOC e titoli intestazioni in document.html; aggiornati versione e data. |
| 2026-01-09 | 0.21 | Aggiunta funzione di post-processing comune con pipeline per verifica congruità TOC e profondità massima; aggiornati versione e data. |
| 2026-01-09 | 0.20 | Aggiornata la gestione del limite per doxygen-export per fermare l'espansione TOC dopo le prime voci in ordine di lettura e generare document.html dalle voci estratte; aggiornato TST-011 con lista attesa e gerarchia per --limit 30; aggiornati versione e data. |
| 2026-01-09 | 0.19 | Aggiornato limite test doxygen-export da 10 a 30 voci con lista specifica attesa e chiarito che per doxygen-export il limite si applica durante l'estrazione della TOC in ordine di lettura (DES-009, TST-011); aggiornati versione e data. |
| 2026-01-09 | 0.17 | Aggiunta consolidazione voci TOC duplicate per Doxygen export (DES-012) ed esclusione elementi TOC dal contenuto pagine (DES-013) con test TST-015; aggiornati versione e data. |
| 2026-01-09 | 0.16 | Aggiunta specifica DES-011 per estrazione TOC Doxygen con Playwright dal selettore `#nav-tree-contents > ul` e test TST-014 per verifica corrispondenza con file di riferimento; aggiornati versione e data. |
| 2026-01-09 | 0.15 | Aggiunta estrazione TOC Doxygen via Playwright con modalità `--toc-only` e test sul nav tree AM64X API Guide; aggiornati versione e data. |
| 2026-01-08 | 0.14 | Aggiunto requisito per titolo di documento nei crawler Doxygen e test dedicato sul caso AM64X API Guide; aggiornati versione e data. |
| 2026-01-08 | 0.13 | Aggiunto requisito di test per verificare il limite `--limit` sul Doxygen export AM64X (`api_guide_am64x`) con 10 voci scaricate; aggiornati versione e data. |
| 2026-01-08 | 0.12 | Aggiunta opzione `--limit <max>` per troncare la TOC e interrompere il download dopo le prime `<max>` voci per tutti i downloader; aggiornati requisiti e test associati. |
| 2026-01-08 | 0.11 | Eliminato dal `document-viewer` l'ultimo blocco di disclaimer TI (i paragrafi che iniziano con "TI PROVIDES TECHNICAL AND RELIABILITY DATA" e terminano con il copyright) mantenendo la sola intestazione "IMPORTANT NOTICE AND DISCLAIMER" nel documento esportato e aggiornati i test associati. |
| 2026-01-08 | 0.10 | Aggiunta riga di titolo in apertura di `document.html` per il downloader `document-viewer`, derivata dalla prima voce della TOC o dalla prima sezione; introdotto requisito di test dedicato. |
| 2026-01-08 | 0.9 | Aggiornata TOC per mostrare titolo "TOC" senza link "Apri documento completo" e rimossa la generazione di sezioni di reindirizzamento per duplicati nel downloader `document-viewer`; aggiunto test per assicurare assenza di placeholder e corretta deduplicazione. |
| 2026-01-08 | 0.8 | Allineata TOC `document-viewer` alla prima voce numerata, esclusa la voce finale "IMPORTANT NOTICE" dalla TOC e limitati i contenuti di `document.html` all'intervallo tra la prima voce numerata e "IMPORTANT NOTICE" inclusa; aggiornati test attesi. |
| 2026-01-08 | 0.7 | Aggiunte opzioni `--verbose` e `--debug` con log differenziati per document-viewer e doxygen-export; aggiornati output attesi della CLI. |
| 2026-01-08 | 0.6 | Aggiunto requisito di test TST-007 per verifica contenuti testuali di `document.html` dal downloader document-viewer, verificando presenza di sezioni, tabelle e dati specifici del documento sprz457. |
| 2026-01-08 | 0.5 | Scaricamento sezioni TOC per `document-viewer`, unione in `document.html`, allineamento anchor TOC-documento e nuovo test di verifica collegamenti. |
| 2026-01-07 | 0.4 | Aggiunto requisito di test TST-005 per verifica completa TOC del documento sprz457. |
| 2026-01-07 | 0.3 | Introdotti output `toc.html`, frameset `index.html` con TOC/documento e navigazione degli anchor nel frame destro. |
| 2026-01-07 | 0.2 | Aggiunta rimozione stili per `document.html` e TOC gerarchico su `index.html` per entrambi i downloader. |
| 2026-01-07 | 0.1 | Prima stesura draft dei requisiti in italiano. |
