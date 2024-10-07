import requests
import random

URL_POKEMON_API_BASE = "https://pokeapi.co/api/v2/pokemon"
NB_PARTICIPANTS = 16

# Définition des avantages entre types de Pokémon
type_advantages = {
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

def get_pokemons_count():
    """
    Make a GET request to the Pokémon API to retrieve the total count of Pokémon.

    :return: The total number of Pokémon as an integer. If an error occurs
             during the request, it returns 0.
    """
    try:
        response = requests.get(URL_POKEMON_API_BASE)
        response.raise_for_status()
        data = response.json()
        return data["count"]
    except requests.RequestException:
        print("Erreur lors de la requête pour récupération du nombre total de pokémons")
        exit()

def get_random_pokemon_id(pokemons_count):
    """
    :param pokemons_count: The total number of available Pokémon.
    :return: A random Pokémon ID between 1 and the total number of available Pokémon.
    """
    return random.randint(1, pokemons_count)

def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: The ID of the Pokemon to fetch data for.
    :return: A dictionary containing the Pokemon data if the request is successful; None if there is a request error.
    """
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def get_random_pokemons():
    """
    Fetches a list of random Pokemon data. The number of Pokemon is defined by
    the constant NB_PARTICIPANTS. Ensures no duplicates are added to the list.

    :return: A list of random Pokemon data.
    """
    pokemons = []
    pokemons_count = get_pokemons_count()
    while len(pokemons) < NB_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemons_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons

def calculate_pokemon_strength(pokemon):
    """
    :param pokemon: A dictionary representing a Pokémon, which includes its stats.
    :type pokemon: dict
    :return: The total strength of the Pokémon calculated as the sum of its base stats.
    :rtype: int
    """
    # On calcule la force d'un pokémon comme la somme de ses statistiques de base
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength

def get_type_advantage_multiplier(pokemon1, pokemon2):
    """
    :param pokemon1: Dictionary representing the first Pokémon with its respective types.
    :param pokemon2: Dictionary representing the second Pokémon with its respective types.
    :return: A float representing the type advantage multiplier between the two Pokémon.
    """
    # On vérifie les avantages de type entre deux pokémons
    types1 = [t['type']['name'] for t in pokemon1['types']]
    types2 = [t['type']['name'] for t in pokemon2['types']]
    multiplier = 1.0
    for t1 in types1:
        if t1 in type_advantages:
            for t2 in types2:
                if t2 in type_advantages[t1]:
                    multiplier *= 1.5  # Avantage de type
    return multiplier

def simulate_battle(pokemon1, pokemon2):
    """
    :param pokemon1: Dictionary containing attributes of the first Pokémon.
    :param pokemon2: Dictionary containing attributes of the second Pokémon.
    :return: Dictionary containing attributes of the winning Pokémon.
    """
    # On calcule la force de chaque pokémon
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    # On applique les avantages de type
    multiplier1 = get_type_advantage_multiplier(pokemon1, pokemon2)
    multiplier2 = get_type_advantage_multiplier(pokemon2, pokemon1)

    adjusted_strength1 = strength1 * multiplier1
    adjusted_strength2 = strength2 * multiplier2

    print(f"Combat entre {pokemon1['name']} et {pokemon2['name']} :")
    print(f" - {pokemon1['name']} : Force totale = {strength1} (après avantage de type : {adjusted_strength1})")
    print(f" - {pokemon2['name']} : Force totale = {strength2} (après avantage de type : {adjusted_strength2})")

    # On compare les forces pour déterminer le vainqueur
    if adjusted_strength1 > adjusted_strength2:
        print(f" --> Vainqueur : {pokemon1['name']}\n")
        return pokemon1
    elif adjusted_strength2 > adjusted_strength1:
        print(f" --> Vainqueur : {pokemon2['name']}\n")
        return pokemon2
    else:
        # En cas d'égalité parfaite, on choisit un vainqueur aléatoire
        winner = random.choice([pokemon1, pokemon2])
        print(f" --> Égalité parfaite, vainqueur aléatoire : {winner['name']}\n")
        return winner

def simulate_round(pokemons):
    """
    :param pokemons: List of Pokémon objects participating in the round.
    :return: List of Pokémon objects that won their respective battles.
    """
    # On simule un round de combats
    winners = []
    for i in range(0, len(pokemons), 2):
        winner = simulate_battle(pokemons[i], pokemons[i + 1])
        winners.append(winner)
    return winners

def main():
    """
    Main function to run a Pokémon tournament.
    Ensures the number of participants is a power of 2 and at least 2.
    Randomly selects Pokémon, prints them, and simulates tournament rounds until a champion is declared.

    :return: None
    """
    if NB_PARTICIPANTS < 2 or (NB_PARTICIPANTS & (NB_PARTICIPANTS - 1)) != 0:
        print("Le nombre de participants doit être une puissance de 2 et supérieur ou égal à 2.")
        return

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