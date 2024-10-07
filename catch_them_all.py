import requests
import random

BASE_URL_POKEMON_API = "https://pokeapi.co/api/v2/pokemon"
NUMBER_OF_PARTICIPANTS = 16

TYPE_ADVANTAGES = {
    "normal": [],
    "fire": ["grass", "bug", "ice", "steel"],
    "water": ["fire", "ground", "rock"],
    "electric": ["water", "flying"],
    "grass": ["water", "ground", "rock"],
    "ice": ["grass", "ground", "flying", "dragon"],
    "fighting": ["normal", "rock", "steel", "ice", "dark"],
    "poison": ["grass", "fairy"],
    "ground": ["fire", "electric", "poison", "rock", "steel"],
    "flying": ["grass", "fighting", "bug"],
    "psychic": ["fighting", "poison"],
    "bug": ["grass", "psychic", "dark"],
    "rock": ["fire", "ice", "flying", "bug"],
    "ghost": ["psychic", "ghost"],
    "dragon": ["dragon"],
    "dark": ["psychic", "ghost"],
    "steel": ["rock", "ice", "fairy"],
    "fairy": ["fighting", "dragon", "dark"]
}


def get_total_pokemons():
    try:
        response = requests.get(BASE_URL_POKEMON_API)
        response.raise_for_status()
        return response.json()["count"]
    except requests.RequestException:
        print("Erreur lors de la requête pour récupération du nombre total de pokémons")
        exit()


def get_random_pokemon_id(pokemon_count):
    return random.randint(1, pokemon_count)


def fetch_pokemon_data(pokemon_id):
    try:
        url = f"{BASE_URL_POKEMON_API}/{pokemon_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_random_pokemons():
    pokemons = []
    pokemon_count = get_total_pokemons()
    while len(pokemons) < NUMBER_OF_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemon_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons


def calculate_pokemon_strength(pokemon):
    return sum(stat['base_stat'] for stat in pokemon['stats'])


def get_type_advantage_multiplier(pokemon1, pokemon2):
    types1 = [t['type']['name'] for t in pokemon1['types']]
    types2 = [t['type']['name'] for t in pokemon2['types']]
    multiplier = 1.0
    for t1 in types1:
        if t1 in TYPE_ADVANTAGES:
            for t2 in types2:
                if t2 in TYPE_ADVANTAGES[t1]:
                    multiplier *= 1.5
    return multiplier


def simulate_battle(pokemon1, pokemon2):
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)
    multiplier1 = get_type_advantage_multiplier(pokemon1, pokemon2)
    multiplier2 = get_type_advantage_multiplier(pokemon2, pokemon1)
    adjusted_strength1 = strength1 * multiplier1
    adjusted_strength2 = strength2 * multiplier2

    print(f"Combat entre {pokemon1['name']} et {pokemon2['name']} :")
    print(f" - {pokemon1['name']} : Force totale = {strength1} (après avantage de type : {adjusted_strength1})")
    print(f" - {pokemon2['name']} : Force totale = {strength2} (après avantage de type : {adjusted_strength2})")

    if adjusted_strength1 > adjusted_strength2:
        print(f" --> Vainqueur : {pokemon1['name']}\n")
        return pokemon1
    elif adjusted_strength2 > adjusted_strength1:
        print(f" --> Vainqueur : {pokemon2['name']}\n")
        return pokemon2
    else:
        winner = random.choice([pokemon1, pokemon2])
        print(f" --> Égalité parfaite, vainqueur aléatoire : {winner['name']}\n")
        return winner


def simulate_round(pokemons):
    winners = []
    for i in range(0, len(pokemons), 2):
        winner = simulate_battle(pokemons[i], pokemons[i + 1])
        winners.append(winner)
    return winners


def main():
    if NUMBER_OF_PARTICIPANTS < 2 or (NUMBER_OF_PARTICIPANTS & (NUMBER_OF_PARTICIPANTS - 1)) != 0:
        print("Le nombre de participants doit être une puissance de 2 et supérieur ou égal à 2.")
        return
    random_pokemons = get_random_pokemons()
    print(f"Les {NUMBER_OF_PARTICIPANTS} Pokémon choisis aléatoirement sont :")
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
