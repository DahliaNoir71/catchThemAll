import requests
import random

URL_POKEMON_API_BASE = "https://pokeapi.co/api/v2/pokemon"
NB_PARTICIPANTS = 16

def get_pokemons_count():
    try:
        response = requests.get(URL_POKEMON_API_BASE)
        response.raise_for_status()
        data = response.json()
        return data["count"]
    except requests.RequestException:
        print("Erreur lors de la requête pour récupération du nombre total de pokémons")
        return 0

def get_random_pokemon_id(pokemons_count):
    return random.randint(1, pokemons_count)

def fetch_pokemon_data(pokemon_id):
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Pas de pokémon avec l'ID : {pokemon_id}")
        return None

def get_random_pokemons():
    pokemons = []
    pokemons_count = get_pokemons_count()
    while len(pokemons) < NB_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemons_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons

def calculate_pokemon_strength(pokemon):
    # On calcule la force d'un pokémon comme la somme de ses statistiques de base
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength

def simulate_battle(pokemon1, pokemon2):
    # On calcule la force de chaque pokémon
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    print(f"Combat entre {pokemon1['name']} et {pokemon2['name']} :")
    print(f" - {pokemon1['name']} : Force totale = {strength1}")
    print(f" - {pokemon2['name']} : Force totale = {strength2}")

    # On compare les forces pour déterminer le vainqueur
    if strength1 > strength2:
        print(f" --> Vainqueur : {pokemon1['name']}\n")
        return pokemon1
    else:
        print(f" --> Vainqueur : {pokemon2['name']}\n")
        return pokemon2

def simulate_round(pokemons):
    # On simule un round de combats
    winners = []
    for i in range(0, len(pokemons), 2):
        winner = simulate_battle(pokemons[i], pokemons[i + 1])
        winners.append(winner)
    return winners

def main():
    random_pokemons = get_random_pokemons()
    print(f"Les {NB_PARTICIPANTS} Pokémon choisis aléatoirement sont :")
    for i, pokemon in enumerate(random_pokemons, start=1):
        print(f"{i}. {pokemon['name']}")
    
    round_number = 1
    current_pokemons = random_pokemons
    while len(current_pokemons) > 1:
        print(f"\n--- Tour {round_number} ---\n")
        current_pokemons = simulate_round(current_pokemons)
        round_number += 1
    
    print("\nLe champion est :")
    print(f"{current_pokemons[0]['name']}")

if __name__ == "__main__":
    main()