# 🚗 Auto Usate - Web App

Un'applicazione web realizzata con **Flask** e **HTML/CSS/JS** per la gestione e la visualizzazione di auto usate, con funzionalità di filtro dinamico.

---

## 🚀 Funzionalità principali

- Visualizzazione tabellare di tutte le auto disponibili
- Filtro avanzato per marca, modello, motore e colore
- Aggiornamento dinamico dei risultati senza ricaricare la pagina
- Visualizzazione immagini delle auto
- Interfaccia responsive e intuitiva

---

## 🏗 Architettura del progetto

Struttura semplificata del progetto:

```
auto_usate_app/
├── app.py                  # Applicazione Flask principale
├── static/
│   └── style.css           # Stili CSS
├── templates/
│   └── index.html          # Pagina principale per la visualizzazione e ricerca auto
└── README_index.md         # Questo file di documentazione
```

---

## 🖼 Funzionamento della pagina index.html

La pagina `index.html` rappresenta la schermata principale dell'applicazione e si compone di:

- **Header:** titolo della pagina.
- **Sezione filtro:** modulo per filtrare le auto per marca, modello, motore e colore.
- **Sezione risultati:** tabella che mostra tutte le auto disponibili, con le relative immagini.
- **Script JS:** intercetta il submit del form, invia i dati al server tramite fetch, aggiorna dinamicamente la tabella dei risultati senza ricaricare la pagina.

---

## ▶️ Esempio di utilizzo

1. Avvia il server Flask.
2. Vai su `http://localhost:5000` o l'indirizzo specificato.
3. Utilizza il form per filtrare le auto secondo le tue preferenze.
4. Visualizza i risultati aggiornati nella tabella sottostante.

---

## ⚙️ Installazione e configurazione

- Nessuna configurazione particolare richiesta.
- Assicurati che i percorsi dei file statici e template siano corretti.
- Il backend Flask deve fornire l'endpoint `/filtra_auto` che restituisce i dati filtrati in formato JSON.

---

## 📦 Dipendenze

- Flask (per il backend)
- HTML, CSS, JavaScript standard

---

## 🔗 Endpoints principali

- `/` → Pagina principale (index.html)
- `/filtra_auto` → Endpoint POST che riceve i filtri e restituisce la lista filtrata di auto in JSON

---

## 🛠 Tecnologie utilizzate

- Python 3.x
- Flask
- HTML5/CSS3/JavaScript

---

## 👨‍💻 Autori

- [@massimiliano](https://github.com/massimiliano)  
- Contributi e suggerimenti sono benvenuti!

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT.

---

# 📄 Spiegazione filtro dinamico in index.html

Questa documentazione spiega il funzionamento del codice JavaScript che gestisce il filtro dinamico delle auto nella pagina `index.html`.

---

## Funzionalità

Il codice permette di:
- Intercettare l'invio del form di filtro senza ricaricare la pagina.
- Inviare i dati inseriti dall'utente al server tramite una richiesta AJAX (fetch).
- Ricevere la lista filtrata delle auto dal backend in formato JSON.
- Aggiornare dinamicamente la tabella dei risultati nella pagina con le auto filtrate.

---

## Dettaglio del codice

```javascript
document.getElementById('filtroForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Raccolta dati dal form
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    // Invio della richiesta al server
    const response = await fetch('/filtra_auto', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    // Conversione della risposta in JSON
    const auto = await response.json();

    // Aggiornamento della tabella dei risultati
    const risultatiTabella = document.getElementById('risultatiTabella');
    risultatiTabella.innerHTML = auto.map(a => `
        <tr>
            <td>${a.marca}</td>
            <td>${a.modello}</td>
            <td>${a.motore}</td>
            <td>${a.colore}</td>
            <td><img src="${a.immagine}" alt="Immagine auto" width="100"></td>
        </tr>
    `).join('');
});
```

---

## Spiegazione passo-passo

1. **Intercettazione submit:**  
   Il codice aggiunge un event listener al form con id `filtroForm`. Quando l'utente invia il form, la funzione viene eseguita e il comportamento predefinito (ricaricare la pagina) viene bloccato con `e.preventDefault()`.

2. **Raccolta dati:**  
   I dati inseriti nei campi del form vengono raccolti tramite `FormData` e convertiti in un oggetto JavaScript (`data`) pronto per essere inviato al server.

3. **Richiesta AJAX:**  
   Viene effettuata una richiesta `fetch` di tipo POST verso l'endpoint `/filtra_auto`, inviando i dati del filtro in formato JSON.

4. **Gestione risposta:**  
   Il server risponde con la lista delle auto filtrate in formato JSON. Il codice converte la risposta in un array di oggetti auto.

5. **Aggiornamento tabella:**  
   La tabella con id `risultatiTabella` viene aggiornata dinamicamente: per ogni auto ricevuta, viene creata una riga HTML con i dati e l'immagine dell'auto.

---

## Vantaggi

- L'utente vede subito i risultati del filtro senza ricaricare la pagina.
- L'interfaccia è più reattiva e moderna.
- Il codice è facilmente estendibile per aggiungere altri filtri o colonne.

---
