from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

CARS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'cars.json')

@app.route('/')
def index():
    # Carica i dati delle auto dal file JSON
    with open(CARS_JSON_PATH, 'r', encoding='utf-8') as f:
        auto = json.load(f)
    # Renderizza la pagina principale con la lista di tutte le auto
    return render_template('index.html', auto=auto)

@app.route('/filtra_auto', methods=['POST'])
def filtra_auto():
    dati = request.json
    with open(CARS_JSON_PATH, 'r', encoding='utf-8') as f:
        auto = json.load(f)
    risultati = []
    for i in auto:
        if ((not dati.get('marca') or i['marca'].lower() == dati['marca'].lower()) and
            (not dati.get('modello') or i['modello'].lower() == dati['modello'].lower()) and
            (not dati.get('motore') or i['motore'].lower() == dati['motore'].lower()) and
            (not dati.get('colore') or i['colore'].lower() == dati['colore'].lower())):
            risultati.append(i)
    return jsonify(risultati)

@app.route('/lista_auto', methods=['GET'])
def lista_auto():
    with open(CARS_JSON_PATH, 'r', encoding='utf-8') as f:
        auto = json.load(f)
    return jsonify(auto)

if __name__ == '__main__':
    app.run(debug=True)
