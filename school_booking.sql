PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'utente'
);

CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    luogo TEXT,
    date TEXT,
    ora TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    event_id INTEGER,
    group_name TEXT,
    FOREIGN KEY(event_id) REFERENCES event(id)
);

-- Eventi di esempio
INSERT INTO event (title, luogo, date, ora, description) VALUES
('Open Day', 'Aula Magna', '2024-06-15', '09:00', 'Giornata di orientamento per studenti e famiglie.'),
('Laboratorio di Robotica', 'Lab 2', '2024-06-20', '14:30', 'Esperienza pratica con robot e automazione.'),
('Seminario Sicurezza Online', 'Aula Informatica', '2024-06-25', '11:00', 'Come proteggersi dai rischi del web.');
