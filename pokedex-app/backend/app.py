from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  

@app.route('/api/pokemon/<name>')
def get_pokemon(name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            'name': data['name'],
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'] for t in data['types']]
        })
    return jsonify({'error': 'Pokemon not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
