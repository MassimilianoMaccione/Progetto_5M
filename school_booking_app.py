from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Configurazione Flask-Mail per invio email di conferma
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Sostituisci con la tua email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Sostituisci con la tua password
mail = Mail(app)

# Percorsi dei file JSON
USERS_FILE = 'users.json'
BOOKINGS_FILE = 'bookings.json'
EVENTS_FILE = 'events.json'

# Inizializza i file JSON se non esistono
for file in [USERS_FILE, BOOKINGS_FILE, EVENTS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

@app.route('/')
def index():
    return render_template('booking.html')

# Visualizzazione calendario interattivo
@app.route('/calendario', methods=['GET'])
def calendario():
    with open(EVENTS_FILE, 'r') as f:
        events = json.load(f)
    return jsonify(events)

# Creazione e modifica eventi (solo per docenti e amministratori)
@app.route('/gestione_eventi', methods=['POST', 'PUT'])
def gestione_eventi():
    data = request.json
    with open(EVENTS_FILE, 'r') as f:
        events = json.load(f)
    if request.method == 'POST':  # Creazione evento
        events.append(data)
    elif request.method == 'PUT':  # Modifica evento
        for event in events:
            if event['id'] == data['id']:
                event.update(data)
                break
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f)
    return jsonify({"message": "Evento gestito con successo!"}), 200

# Modulo di iscrizione con supporto per prenotazioni di gruppo
@app.route('/iscrizione', methods=['POST'])
def iscrizione():
    data = request.json
    with open(BOOKINGS_FILE, 'r') as f:
        bookings = json.load(f)
    bookings.append(data)
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f)
    return jsonify({"message": "Iscrizione completata!"}), 201

@app.route('/prenotazioni', methods=['GET'])
def get_bookings():
    with open(BOOKINGS_FILE, 'r') as f:
        bookings = json.load(f)
    return jsonify(bookings)

@app.route('/prenota', methods=['POST'])
def book_event():
    data = request.json
    with open(BOOKINGS_FILE, 'r') as f:
        bookings = json.load(f)
    bookings.append(data)
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f)
    return jsonify({"message": "Prenotazione effettuata con successo!"}), 201

# Registrazione utenti con email/password
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if any(user['email'] == data['email'] for user in users):
        return jsonify({"message": "Email già registrata!"}), 400
    data['verified'] = False  # Account non verificato
    users.append(data)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

    # Invia email di conferma
    verification_link = f"http://localhost:5000/verify?email={data['email']}"
    msg = Message('Conferma il tuo account', sender='your-email@gmail.com', recipients=[data['email']])
    msg.body = f"Ciao {data['name']}, clicca sul link per verificare il tuo account: {verification_link}"
    mail.send(msg)

    return jsonify({"message": "Registrazione completata! Controlla la tua email per confermare l'account."}), 201

# Verifica account tramite email
@app.route('/verify', methods=['GET'])
def verify_account():
    email = request.args.get('email')
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    for user in users:
        if user['email'] == email:
            user['verified'] = True
            break
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    return "Account verificato con successo! Ora puoi accedere."

# Login utenti
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    user = next((u for u in users if u['email'] == data['email'] and u['password'] == data['password']), None)
    if user:
        if not user['verified']:
            return jsonify({"message": "Account non verificato. Controlla la tua email."}), 403
        return jsonify({"message": "Login effettuato con successo!", "role": user['role']}), 200
    return jsonify({"message": "Credenziali non valide."}), 401

# Dashboard utente
@app.route('/dashboard', methods=['GET'])
def dashboard():
    email = request.args.get('email')
    with open(BOOKINGS_FILE, 'r') as f:
        bookings = json.load(f)
    user_bookings = [b for b in bookings if b['email'] == email]
    return jsonify(user_bookings)

# Calendario eventi
@app.route('/eventi', methods=['GET', 'POST'])
def eventi():
    if request.method == 'GET':
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)
        return jsonify(events)
    elif request.method == 'POST':
        data = request.json
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)
        events.append(data)
        with open(EVENTS_FILE, 'w') as f:
            json.dump(events, f)
        return jsonify({"message": "Evento aggiunto con successo!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
