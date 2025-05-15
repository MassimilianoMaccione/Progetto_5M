from flask import Flask, render_template, request, jsonify, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'

DATABASE = os.path.join(app.root_path, 'school_booking.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'utente'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                date TEXT,
                description TEXT
            )
        ''')
        # --- AGGIUNGI SOLO SE NON ESISTONO ---
        columns = [row[1] for row in cursor.execute("PRAGMA table_info(event)").fetchall()]
        if 'luogo' not in columns:
            cursor.execute('ALTER TABLE event ADD COLUMN luogo TEXT')
        if 'ora' not in columns:
            cursor.execute('ALTER TABLE event ADD COLUMN ora TEXT')
        # --------------------------------------
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                event_id INTEGER,
                group_name TEXT,
                FOREIGN KEY(event_id) REFERENCES event(id)
            )
        ''')
        db.commit()
        # Inserisci eventi di esempio se la tabella è vuota
        events = cursor.execute('SELECT COUNT(*) FROM event').fetchone()[0]
        if events == 0:
            cursor.executemany(
                'INSERT INTO event (title, luogo, date, ora, description) VALUES (?, ?, ?, ?, ?)',
                [
                    ("Open Day", "Aula Magna", "2024-06-15", "09:00", "Giornata di orientamento per studenti e famiglie."),
                    ("Laboratorio di Robotica", "Lab 2", "2024-06-20", "14:30", "Esperienza pratica con robot e automazione."),
                    ("Seminario Sicurezza Online", "Aula Informatica", "2024-06-25", "11:00", "Come proteggersi dai rischi del web."),
                    ("Hackathon Coding", "Aula 101", "2024-07-01", "08:30", "Maratona di programmazione a squadre."),
                    ("Incontro con l'autore", "Biblioteca", "2024-07-03", "10:00", "Presentazione libro e dibattito."),
                    ("Gara di Matematica", "Aula 202", "2024-07-10", "09:30", "Competizione tra studenti delle classi."),
                    ("Workshop di Fotografia", "Aula Arte", "2024-07-12", "15:00", "Laboratorio pratico di fotografia digitale."),
                    ("Seminario di Fisica", "Aula Magna", "2024-07-15", "12:00", "Scoperte recenti nel campo della fisica."),
                    ("Corso di Primo Soccorso", "Palestra", "2024-07-18", "16:00", "Lezioni teoriche e pratiche di primo soccorso."),
                    ("Torneo di Scacchi", "Aula Ricreazione", "2024-07-20", "14:00", "Sfida tra studenti e professori."),
                    ("Laboratorio di Robotica", "Aula Magna", "2024-06-20", "10:00", "Esperienza pratica con robot e automazione."),
                    ("Seminario Sicurezza Online", "Aula 2", "2024-06-25", "09:00", "Come proteggersi dai rischi del web."),
                    ("Corso Python Base", "Lab Informatica", "2024-06-22", "14:00", "Introduzione alla programmazione Python."),
                    ("Workshop Arduino", "Lab Elettronica", "2024-06-23", "11:00", "Costruisci il tuo primo circuito."),
                    ("Giornata dello Sport", "Palestra", "2024-06-24", "08:30", "Tornei e attività sportive."),
                    ("Incontro con l'Autore", "Biblioteca", "2024-06-26", "16:00", "Presentazione libro e firma copie."),
                    ("Visita Aziendale", "Esterno", "2024-06-27", "09:30", "Scopri il mondo del lavoro."),
                    ("Seminario Cybersecurity", "Aula 3", "2024-06-28", "10:30", "Difesa dai cyber attacchi."),
                    ("Laboratorio di Chimica", "Lab Chimica", "2024-06-29", "13:00", "Esperimenti pratici."),
                    ("Corso Excel Avanzato", "Lab Informatica", "2024-06-30", "15:00", "Automatizza i tuoi fogli di calcolo."),
                    ("Proiezione Film", "Aula Magna", "2024-07-01", "17:00", "Cinema e dibattito."),
                    ("Torneo di Scacchi", "Aula 4", "2024-07-02", "12:00", "Sfida i tuoi compagni!")
                ]
            )
            db.commit()

init_db()

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/auth')
def auth():
    if 'user_email' in session:
        return redirect(url_for('calendario'))
    return render_template('auth.html')

@app.route('/calendario', methods=['GET'])
def calendario():
    if 'user_email' not in session:
        return redirect(url_for('auth'))
    db = get_db()
    user = db.execute('SELECT name FROM user WHERE email=?', (session['user_email'],)).fetchone()
    name = user['name'] if user else session['user_email']
    # Converti Row objects in dict per compatibilità con tojson e template
    events = db.execute('SELECT * FROM event').fetchall()
    events = [dict(e) for e in events]
    bookings = db.execute(
        'SELECT event_id FROM booking WHERE email=?', (session['user_email'],)
    ).fetchall()
    booked_event_ids = {b['event_id'] for b in bookings}
    user_role = session.get('user_role', 'utente')
    return render_template(
        'calendario.html',
        name=name,
        email=session['user_email'],
        events=events,
        booked_event_ids=booked_event_ids,
        user_role=user_role
    )

@app.route('/gestione_eventi', methods=['POST', 'PUT'])
def gestione_eventi():
    db = get_db()
    data = request.json

    # Controllo autenticazione e ruolo
    if 'user_email' not in session or session.get('user_role') != 'professore':
        return jsonify({"message": "Non autorizzato. Solo i professori possono creare/modificare eventi."}), 401

    # Controllo presenza dati obbligatori
    required_fields = ['title', 'luogo', 'date', 'ora', 'description']
    if not all(data.get(field) for field in required_fields):
        return jsonify({"message": "Tutti i campi sono obbligatori!"}), 400

    if request.method == 'POST':
        db.execute(
            'INSERT INTO event (title, luogo, date, ora, description) VALUES (?, ?, ?, ?, ?)',
            (
                data['title'],
                data['luogo'],
                data['date'],
                data['ora'],
                data['description']
            )
        )
        db.commit()
        # Recupera tutti gli eventi dopo l'inserimento
        events = db.execute('SELECT * FROM event').fetchall()
        events_list = [
            {
                "id": e["id"],
                "title": e["title"],
                "luogo": e["luogo"],
                "date": e["date"],
                "ora": e["ora"],
                "description": e["description"]
            }
            for e in events
        ]
        return jsonify({"message": "Evento creato con successo!", "events": events_list, "redirect": url_for('lista_eventi')}), 200
    elif request.method == 'PUT':
        if not data.get('id'):
            return jsonify({"message": "ID evento mancante per la modifica."}), 400
        db.execute(
            'UPDATE event SET title=?, luogo=?, date=?, ora=?, description=? WHERE id=?',
            (
                data['title'],
                data['luogo'],
                data['date'],
                data['ora'],
                data['description'],
                data['id']
            )
        )
        db.commit()
        return jsonify({"message": "Evento modificato con successo!"}), 200

@app.route('/iscrizione', methods=['POST'])
def iscrizione():
    data = request.json
    db = get_db()
    db.execute(
        'INSERT INTO booking (email, event_id, group_name) VALUES (?, ?, ?)',
        (data.get('email'), data.get('event_id'), data.get('group_name', ''))
    )
    db.commit()
    return jsonify({"message": "Iscrizione completata!"}), 201

@app.route('/prenotazioni', methods=['GET'])
def get_bookings():
    if 'user_email' not in session:
        return redirect(url_for('welcome'))
    db = get_db()
    bookings = db.execute(
        'SELECT * FROM booking WHERE email=?', (session['user_email'],)
    ).fetchall()
    result = [
        {"id": b["id"], "email": b["email"], "event_id": b["event_id"], "group_name": b["group_name"]}
        for b in bookings
    ]
    return jsonify(result)

@app.route('/prenota', methods=['POST'])
def book_event():
    if 'user_email' not in session:
        return jsonify({"message": "Non autorizzato."}), 401
    data = request.json
    db = get_db()
    db.execute(
        'INSERT INTO booking (email, event_id, group_name) VALUES (?, ?, ?)',
        (session['user_email'], data.get('event_id'), data.get('group_name', ''))
    )
    db.commit()
    return jsonify({"message": "Prenotazione effettuata con successo!"}), 201

@app.route('/annulla_prenotazione', methods=['POST'])
def annulla_prenotazione():
    if 'user_email' not in session:
        return jsonify({"message": "Non autorizzato."}), 401
    data = request.json
    db = get_db()
    db.execute(
        'DELETE FROM booking WHERE email=? AND event_id=?',
        (session['user_email'], data.get('event_id'))
    )
    db.commit()
    return jsonify({"message": "Prenotazione annullata con successo!"}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE email=?', (data['email'],)).fetchone()
    if user:
        return jsonify({"message": "Email già registrata!"}), 400
    db.execute(
        'INSERT INTO user (name, email, password, role) VALUES (?, ?, ?, ?)',
        (data.get("name", ""), data["email"], data["password"], data.get("role", "utente"))
    )
    db.commit()
    session['user_email'] = data['email']
    session['user_role'] = data.get('role', 'utente')
    return jsonify({"message": "Registrazione completata!", "redirect": url_for('calendario')}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE email=? AND password=?',
        (data['email'], data['password'])
    ).fetchone()
    if user:
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        return jsonify({"message": "Login effettuato con successo!", "redirect": url_for('calendario')}), 200
    return jsonify({"message": "Email e/o password non valide."}), 401

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_role', None)
    return redirect(url_for('welcome'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('welcome'))
    db = get_db()
    bookings = db.execute(
        'SELECT * FROM booking WHERE email=?', (session['user_email'],)
    ).fetchall()
    result = [
        {"id": b["id"], "email": b["email"], "event_id": b["event_id"], "group_name": b["group_name"]}
        for b in bookings
    ]
    return jsonify(result)

@app.route('/eventi', methods=['GET', 'POST'])
def eventi():
    if 'user_email' not in session:
        return redirect(url_for('welcome'))
    db = get_db()
    if request.method == 'GET':
        events = db.execute('SELECT * FROM event').fetchall()
        result = [
            {
                "id": e["id"],
                "title": e["title"],
                "luogo": e["luogo"],
                "date": e["date"],
                "ora": e["ora"],
                "description": e["description"]
            }
            for e in events
        ]
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        # Solo professore può creare eventi tramite questa rotta
        if 'user_email' not in session or session.get('user_role') != 'professore':
            return jsonify({"message": "Non autorizzato."}), 401
        required_fields = ['title', 'luogo', 'date', 'ora', 'description']
        if not all(data.get(field) for field in required_fields):
            return jsonify({"message": "Tutti i campi sono obbligatori!"}), 400
        db.execute(
            'INSERT INTO event (title, luogo, date, ora, description) VALUES (?, ?, ?, ?, ?)',
            (
                data['title'],
                data['luogo'],
                data['date'],
                data['ora'],
                data['description']
            )
        )
        db.commit()
        return jsonify({"message": "Evento aggiunto con successo!"}), 201

@app.route('/crea_evento', methods=['POST'])
def crea_evento():
    if 'user_email' not in session or session.get('user_role') != 'professore':
        return jsonify({"message": "Non autorizzato."}), 401
    data = request.json
    required_fields = ['title', 'luogo', 'date', 'ora', 'description']
    if not all(data.get(field) for field in required_fields):
        return jsonify({"message": "Tutti i campi sono obbligatori!"}), 400
    db = get_db()
    db.execute(
        'INSERT INTO event (title, luogo, date, ora, description) VALUES (?, ?, ?, ?, ?)',
        (
            data['title'],
            data['luogo'],
            data['date'],
            data['ora'],
            data['description']
        )
    )
    db.commit()
    return jsonify({"message": "Evento creato con successo!"}), 201

@app.route('/elimina_evento', methods=['POST'])
def elimina_evento():
    if 'user_email' not in session or session.get('user_role') != 'professore':
        return jsonify({"message": "Non autorizzato."}), 401
    data = request.json
    db = get_db()
    db.execute('DELETE FROM event WHERE id=?', (data.get('event_id'),))
    db.execute('DELETE FROM booking WHERE event_id=?', (data.get('event_id'),))
    db.commit()
    return jsonify({"message": "Evento eliminato con successo!"}), 200

@app.route('/crea_evento_page')
def crea_evento_page():
    if 'user_email' not in session or session.get('user_role') != 'professore':
        return redirect(url_for('calendario'))
    return render_template('crea_evento.html', name=session.get('user_email'))

@app.route('/lista_eventi')
def lista_eventi():
    if 'user_email' not in session:
        return redirect(url_for('auth'))
    db = get_db()
    user = db.execute('SELECT name, role FROM user WHERE email=?', (session['user_email'],)).fetchone()
    name = user['name'] if user else session['user_email']
    user_role = user['role'] if user else 'utente'
    events = db.execute('SELECT * FROM event').fetchall()
    bookings = db.execute(
        'SELECT event_id FROM booking WHERE email=?', (session['user_email'],)
    ).fetchall()
    booked_event_ids = {b['event_id'] for b in bookings}
    return render_template(
        'lista_eventi.html',
        name=name,
        email=session['user_email'],
        events=events,
        booked_event_ids=booked_event_ids,
        user_role=user_role
    )

@app.route('/lista_eventi_json')
def lista_eventi_json():
    if 'user_email' not in session:
        return jsonify({'events': [], 'booked_event_ids': [], 'user_role': 'utente'})
    db = get_db()
    user = db.execute('SELECT role FROM user WHERE email=?', (session['user_email'],)).fetchone()
    user_role = user['role'] if user else 'utente'
    events = db.execute('SELECT * FROM event').fetchall()
    bookings = db.execute('SELECT event_id FROM booking WHERE email=?', (session['user_email'],)).fetchall()
    booked_event_ids = [b['event_id'] for b in bookings]
    events_list = [dict(e) for e in events]
    return jsonify({'events': events_list, 'booked_event_ids': booked_event_ids, 'user_role': user_role})

if __name__ == '__main__':
    app.run(debug=True)
