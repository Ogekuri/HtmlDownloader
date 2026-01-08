---
title: "Requisiti di HtmlDownloader"
description: Specifica dei requisiti software
version: "0.11.0"
date: "2026-01-08"
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
**Versione**: 0.11.0  
**Autore**: Ogekuri  
**Data**: 2026-01-08

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
- **DES-003**: Il downloader TI deve usare Playwright in modalità headless per caricare la pagina, espandere e scorrere la TOC, visitare ogni link della TOC per scaricare il contenuto della relativa sezione, effettuare auto-scroll quando necessario, catturare le risposte immagine dal network, riscrivere i riferimenti degli asset verso percorsi locali, assegnare e normalizzare ID univoci per intestazioni e sezioni e serializzare offline un unico documento che unisca tutte le sezioni scaricate; dopo l'estrazione della TOC deve eliminare tutte le voci iniziali fino alla prima voce che inizia con "1 " (compresa la prima voce numerata) e deve rimuovere l'ultima voce se è "IMPORTANT NOTICE"; durante l'esportazione della sezione finale "IMPORTANT NOTICE" non deve copiare il blocco di disclaimer TI (il paragrafo lungo che inizia con "TI PROVIDES TECHNICAL AND RELIABILITY DATA" e termina con Copyright 2024), pur mantenendo l'anchor e l'intestazione nel TOC; se più sezioni risultano identiche deve mantenere una sola istanza di contenuto e far puntare le voci duplicate della TOC all'anchor già presente senza aggiungere sezioni di reindirizzamento nel documento.
- **DES-004**: Il downloader Doxygen deve effettuare crawling in ampiezza nell'ambito del percorso di origine, costruire sezioni `page-N` con titolo e contenuto principale estratto, quindi generare un documento unico con indice.
- **DES-005**: I download di asset devono usare sessioni HTTP riutilizzate con streaming a chunk e riscrivere i riferimenti HTML verso i percorsi locali offline.
- **DES-006**: Il rilevamento del downloader deve combinare regole su URL e, se necessario, analisi dell'HTML iniziale limitata per determinare il tipo corretto o segnalare errore.
- **DES-007**: I downloader devono rimuovere da `document.html` tutti i riferimenti a fogli di stile esterni, i tag di stile e gli attributi di stile inline, producendo un HTML privo di personalizzazioni estetiche del sorgente.
- **DES-008**: `index.html` deve essere un frameset con due frame affiancati: a sinistra `toc.html`, a destra `document.html`; i link della TOC devono aprire gli anchor nel frame destro.

### 3.2 Funzioni
- **REQ-001**: La CLI deve accettare `--from-url` e `--to-dir` obbligatori e `--user-agent` opzionale, creando la directory di destinazione se assente.
- **REQ-002**: L'applicazione deve identificare automaticamente quale downloader utilizzare e terminare con errore se non è determinabile.
- **REQ-003**: Per TI "document-viewer" deve scaricare tutte le sezioni referenziate dalla TOC remota a partire dalla prima voce che inizia con "1 " e fermarsi ai contenuti di "IMPORTANT NOTICE" (l'intestazione permane ma il blocco di disclaimer TI che segue non deve essere esportato), fonderle in un unico `document.html` con stile minimale e immagini salvate localmente, riscrivere i link asset, creare `toc.html` con TOC gerarchica ripulita dalle voci precedenti alla prima numerata e senza l'ultima voce "IMPORTANT NOTICE", generare `index.html` frameset che mostra a sinistra la TOC e a destra il documento navigabile tramite anchor, e inserire in apertura di `document.html` una riga di titolo ricavata dalla prima voce della TOC (o, se assente, dal titolo della prima sezione scaricata).
- **REQ-004**: Per export Doxygen deve scaricare e fondere le pagine HTML entro l'ambito individuato, riscrivere i link asset, scaricare le risorse con barra di avanzamento, creare `toc.html` con TOC gerarchica e generare `index.html` frameset che mostra a sinistra la TOC e a destra il documento navigabile tramite anchor.
- **REQ-005**: L'esecuzione deve stampare su stdout il downloader selezionato e i percorsi principali salvati; messaggi di avanzamento e di verifica devono essere mostrati solo quando attivati da `--verbose` o `--debug`.
- **REQ-006**: I nomi file derivati dagli URL devono essere sanificati (rimozione caratteri non validi, query fingerprint) per essere compatibili con il file system.
- **REQ-007**: `toc.html` generato da `document-viewer` e `doxygen-export` deve presentare un sommario gerarchico (TOC ad albero) coerente con la struttura delle sezioni esportate; per `document-viewer` la TOC deve iniziare dalla prima voce che inizia con "1 " e non deve contenere la voce finale "IMPORTANT NOTICE"; tutti i link della TOC devono puntare ad anchor esistenti dentro `document.html` e aprirsi nel frame destro del frameset; il titolo mostrato in `toc.html` deve essere "TOC" e non deve includere link "Apri documento completo".
- **REQ-008**: La CLI deve esporre le opzioni `--verbose` e `--debug`; per `document-viewer` `--verbose` deve mostrare gli avanzamenti dell'auto-scroll e l'esito dei check su estrazione/salvataggio di `toc.html` e `document.html`, mentre `--debug` deve includere questi dettagli; per `doxygen-export` `--verbose` deve mostrare gli avanzamenti del salvataggio degli elementi della TOC e `--debug` deve mostrare l'esito dei check su generazione di `toc.html` e `document.html`.

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

## 5. Cronologia revisioni
| Data | Versione | Motivazione e descrizione cambiamento |
|------|----------|---------------------------------------|
| 2026-01-08 | 0.11.0 | Eliminato dal `document-viewer` l'ultimo blocco di disclaimer TI (i paragrafi che iniziano con "TI PROVIDES TECHNICAL AND RELIABILITY DATA" e terminano con il copyright) mantenendo la sola intestazione "IMPORTANT NOTICE AND DISCLAIMER" nel documento esportato e aggiornati i test associati. |
| 2026-01-08 | 0.10.0 | Aggiunta riga di titolo in apertura di `document.html` per il downloader `document-viewer`, derivata dalla prima voce della TOC o dalla prima sezione; introdotto requisito di test dedicato. |
| 2026-01-08 | 0.9.0 | Aggiornata TOC per mostrare titolo "TOC" senza link "Apri documento completo" e rimossa la generazione di sezioni di reindirizzamento per duplicati nel downloader `document-viewer`; aggiunto test per assicurare assenza di placeholder e corretta deduplicazione. |
| 2026-01-08 | 0.8.0 | Allineata TOC `document-viewer` alla prima voce numerata, esclusa la voce finale "IMPORTANT NOTICE" dalla TOC e limitati i contenuti di `document.html` all'intervallo tra la prima voce numerata e "IMPORTANT NOTICE" inclusa; aggiornati test attesi. |
| 2026-01-08 | 0.7.0 | Aggiunte opzioni `--verbose` e `--debug` con log differenziati per document-viewer e doxygen-export; aggiornati output attesi della CLI. |
| 2026-01-08 | 0.6.0 | Aggiunto requisito di test TST-007 per verifica contenuti testuali di `document.html` dal downloader document-viewer, verificando presenza di sezioni, tabelle e dati specifici del documento sprz457. |
| 2026-01-08 | 0.5.0 | Scaricamento sezioni TOC per `document-viewer`, unione in `document.html`, allineamento anchor TOC-documento e nuovo test di verifica collegamenti. |
| 2026-01-07 | 0.0 | Prima stesura draft dei requisiti in italiano. |
| 2026-01-07 | 0.2.0 | Aggiunta rimozione stili per `document.html` e TOC gerarchico su `index.html` per entrambi i downloader. |
| 2026-01-07 | 0.3.0 | Introdotti output `toc.html`, frameset `index.html` con TOC/documento e navigazione degli anchor nel frame destro. |
| 2026-01-07 | 0.4.0 | Aggiunto requisito di test TST-005 per verifica completa TOC del documento sprz457. |
