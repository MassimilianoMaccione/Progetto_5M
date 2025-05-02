from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filtra_auto', methods=['POST'])
def filtra_auto():
    dati = request.json
    with open('cars.json', 'r') as f:
        auto = json.load(f)

    risultati = [
        a for a in auto
        if (dati['marca'] == '' or a['marca'].lower() == dati['marca'].lower()) and
           (dati['modello'] == '' or a['modello'].lower() == dati['modello'].lower()) and
           (dati['motore'] == '' or a['motore'].lower() == dati['motore'].lower()) and
           (dati['colore'] == '' or a['colore'].lower() == dati['colore'].lower())
    ]

    return jsonify(risultati)

if __name__ == '__main__':
    app.run(debug=True)
