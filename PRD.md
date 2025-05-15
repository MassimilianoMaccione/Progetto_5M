# 📄 Product Requirements Document (PRD) - School Booking App

## 1. Obiettivo del Prodotto

Realizzare una web app per la gestione di eventi scolastici che consenta a studenti e professori di:
- Visualizzare un calendario eventi
- Prenotare e annullare la partecipazione agli eventi (studenti)
- Creare e cancellare eventi (professori)
- Gestire autenticazione e ruoli

---

## 2. Stakeholder

- Studenti
- Professori
- Amministratori scolastici (opzionale)
- Sviluppatori

---

## 3. Funzionalità Principali

### Utente Studente
- Registrazione e login
- Visualizzazione eventi disponibili
- Prenotazione e annullamento prenotazione eventi
- Visualizzazione delle proprie prenotazioni

### Utente Professore
- Tutte le funzionalità dello studente
- Creazione di nuovi eventi (con titolo, luogo, data, ora, descrizione)
- Eliminazione di eventi creati

### Eventi
- Ogni evento ha: titolo, luogo, data, ora, descrizione
- Gli eventi sono visibili a tutti gli utenti autenticati

### Autenticazione
- Registrazione con scelta ruolo (studente/professore)
- Login/logout
- Gestione sessione utente

---

## 4. Requisiti Tecnici

- **Backend**: Python 3.x, Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS (Jinja2 template)
- **Persistenza**: Tutti i dati salvati su database SQL
- **Sicurezza**: Gestione sessione Flask, password in chiaro (per semplicità demo, in produzione usare hash)
- **Diagramma ER**: incluso nel progetto (Mermaid)
- **README**: dettagliato con istruzioni, struttura, endpoints

---

## 5. Architettura e Struttura

- `/school_booking_app.py`: logica Flask e gestione rotte
- `/templates/`: pagine HTML (welcome, auth, calendario)
- `/static/`: CSS
- `/school_booking.db`: database SQLite
- `/school_booking.sql`: script SQL per creazione DB
- `/er_diagram.txt`: diagramma ER
- `/README.md`: documentazione tecnica
- `/PRD.md`: questo documento

---

## 6. User Flow

1. L’utente apre la home page di benvenuto
2. Può registrarsi o accedere (scegliendo il ruolo)
3. Dopo il login, accede al calendario eventi
4. Se studente: può prenotare/annullare eventi
5. Se professore: può anche creare/eliminare eventi
6. Può effettuare il logout

---

## 7. Requisiti di Interfaccia

- Interfaccia semplice e responsiva
- Pulsanti chiari per prenotazione, annullamento, creazione, eliminazione eventi
- Visualizzazione nome utente vicino al logout
- Select per scelta ruolo in fase di registrazione

---

## 8. Requisiti Non Funzionali

- Facilità di installazione e avvio (solo Python e SQLite richiesti)
- Codice commentato e facilmente estendibile
- Nessuna dipendenza da servizi esterni

---

## 9. Vincoli

- Password salvate in chiaro (solo per demo, non per produzione)
- Nessuna gestione avanzata dei permessi (solo distinzione studente/professore)
- Nessuna email di conferma/invio notifiche

---

## 10. Success Criteria

- Tutte le funzionalità principali sono accessibili e funzionanti
- Il database viene popolato correttamente
- L’interfaccia è chiara e usabile da studenti e professori
- Il progetto è documentato e facilmente installabile

---

## Aggiornamento gestione eventi

Per facilitare i test e la presentazione, il sistema inserisce automaticamente una dozzina di eventi di esempio nel database, se questo risulta vuoto al primo avvio. In questo modo, la pagina del calendario mostra subito eventi già disponibili, evitando la situazione precedente in cui la pagina era vuota e gli eventi dovevano essere inseriti manualmente per essere visualizzati.

---

## Nota sulla visualizzazione eventi

La piattaforma permette già di creare nuovi eventi tramite il form dedicato, ma al momento non è ancora possibile visualizzare nell’interfaccia gli eventi inseriti dagli utenti: questi vengono correttamente registrati nel database, ma la loro visualizzazione sulla pagina sarà implementata in un aggiornamento futuro. In questo modo, sarà possibile consultare sia gli eventi di esempio che quelli aggiunti manualmente.

---
