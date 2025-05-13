from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Carica i dati delle auto dal file JSON
    with open('cars.json', 'r') as f:
        auto = json.load(f)
    
    # Renderizza la pagina principale con la lista di tutte le auto
    return render_template('index.html', auto=auto)

@app.route('/filtra_auto', methods=['POST'])
def filtra_auto():
    # Riceve i dati dal form
    dati = request.json
    
    # Carica i dati delle auto dal file JSON
    with open('cars.json', 'r') as f:
        auto = json.load(f)

    # Filtra le auto in base ai criteri forniti
    risultati = [
        a for a in auto
        if (dati['marca'] == '' or a['marca'].lower() == dati['marca'].lower()) and
           (dati['modello'] == '' or a['modello'].lower() == dati['modello'].lower()) and
           (dati['motore'] == '' or a['motore'].lower() == dati['motore'].lower()) and
           (dati['colore'] == '' or a['colore'].lower() == dati['colore'].lower())
    ]

    # Restituisce i risultati come JSON
    return jsonify(risultati)

@app.route('/lista_auto', methods=['GET'])
def lista_auto():
    # Carica i dati delle auto dal file JSON
    with open('cars.json', 'r') as f:
        auto = json.load(f)
    
    # Restituisce la lista di tutte le auto come JSON
    return jsonify(auto)

if __name__ == '__main__':
    # Avvia l'app Flask in modalità debug
    app.run(debug=True)
