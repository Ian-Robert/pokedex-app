from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__) #Initializes the Flask App. __name__ tells Flask where to find files
CORS(app) # Enables cross-origin requests so React can call backend API.

GEN_INFO = {
        "1": {"limit": 151, "offset": 0},
        "2": {"limit": 100, "offset": 151},
        "3": {"limit": 135, "offset": 251},
        "4": {"limit": 107, "offset": 386},
        "5": {"limit": 156, "offset": 493},
        }

# pokemon list by generation
@app.route('/api/gen/<gen_number>')
def get_generation(gen_number):
    if gen_number not in GEN_INFO:
        return jsonify({"error": "Generation not found"}), 404

    info = GEN_INFO[gen_number]
    url = f"https://pokeapi.co/api/v2/pokemon?limit={info['limit']}&offset={info['offset']}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'failed to fetch from PokeAPI'}), 500

    data = response.json()
    pokemon_list = [{"name": p["name"], "url": p["url"]} for p in data['results']]

    return jsonify(pokemon_list)

#get individual pokemon info
@app.route('/api/pokemon/<name>') # Defines a route / endpoint, runs the function if the specific route's visited.
def get_pokemon(name): 
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}') 
    if response.status_code == 200:                                       
        data = response.json()
        return jsonify({
            'name': data['name'],
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'] for t in data['types']],
            'stats': {s['stat']['name']: s['base_stat'] for s in data['stats']}
        })
    return jsonify({'error': 'Pokemon not found'}), 404

if __name__ == "__main__": 
    app.run(debug=True)
