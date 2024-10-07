import requests
import random

URL_POKEMON_API_BASE = "https://pokeapi.co/api/v2/pokemon"
NB_PARTICIPANTS = 16


def get_pokemons_count():
    pokemon_count = 0
    try:
        response = requests.get(URL_POKEMON_API_BASE)
        response.raise_for_status()
        data = response.json()
        pokemon_count = data["count"]
    except requests.RequestException as e:
        print(f"Erreur lors de la requête pour récupération du nombre total de pokémons")
    return pokemon_count


def get_random_pokemon():
    try:
        # PokeAPI contient actuellement 1010 pokémon, donc on tire un ID entre 1 et 1010
        pokemon_id = random.randint(1, 1010)
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Erreur lors de la requête pour le pokémon avec l'ID {pokemon_id}: {e}")
        return None

def get_16_random_pokemons():
    pokemons = []
    while len(pokemons) < 16:
        pokemon_data = get_random_pokemon()
        if pokemon_data:
            pokemons.append(pokemon_data)
    return pokemons

def main():
    print(get_pokemons_count())
    random_pokemons = get_16_random_pokemons()
    print("Les 16 Pokémon choisis aléatoirement sont :")
    for i, pokemon in enumerate(random_pokemons, start=1):
        print(f"{i}. {pokemon['name']}")
        print(f"   - Type(s) : {[t['type']['name'] for t in pokemon['types']]}")
        print(f"   - Taille : {pokemon['height']}")
        print(f"   - Poids : {pokemon['weight']}")
        print(f"   - Statistiques :")
        for stat in pokemon['stats']:
            print(f"     * {stat['stat']['name']} : {stat['base_stat']}")
        print(f"   - Capacités : {[ability['ability']['name'] for ability in pokemon['abilities']]}")

if __name__ == "__main__":
    main()