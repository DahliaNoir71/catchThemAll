import requests
import random

BASE_URL_API = "https://pokeapi.co/api/v2/"

# URL de l'API Pokémon pour récupérer les données de base des pokémons et des types
URL_POKEMON_API_BASE = "%spokemon" % BASE_URL_API
URL_TYPE_API = "%stype" % BASE_URL_API
NB_PARTICIPANTS = 32


def get_type_advantages():
    """
    Fetches advantages of a Pokémon type using the PokeAPI.

    :return: A dictionary where keys are Pokémon types, and values are lists of types they are strong against.
    """
    URL_TYPE_API = "https://pokeapi.co/api/v2/type/"


def fetch_type_details(type_url):
    """
    :param type_url: The URL to fetch the type details from
    :return: A dictionary containing the type details returned from the requested URL
    """
    response = requests.get(type_url)
    response.raise_for_status()
    return response.json()


def get_type_advantages():
    """
    Fetches Pokemon type advantages from an external API.

    This function retrieves type information from a specified URL, extracts
    data about which types are strong against others, and compiles them into a
    dictionary. If there is an error during the request process, it prints an error
    message and returns an empty dictionary.

    :return: A dictionary where the keys are Pokemon type names and the values are lists of type names that they are strong against.
    """
    type_advantages = {}
    try:
        # Récupérer les informations sur les types de l'API
        response = requests.get(URL_TYPE_API)
        response.raise_for_status()
        types_data = response.json()["results"]

        # Itérer sur chaque type et récupérer ses relations de dégâts
        for type_info in types_data:
            type_name = type_info["name"]
            type_details = fetch_type_details(type_info["url"])
            strong_against = [relation["name"] for relation in type_details["damage_relations"]["double_damage_to"]]
            type_advantages[type_name] = strong_against
    except requests.RequestException as e:
        print("Erreur lors de la requête pour récupérer les avantages de type :", e)
    return type_advantages


def get_pokemons_count():
    """
    Fetches the total count of Pokémon from the Pokémon API.

    :return: Total number of Pokémon available from the API. Returns 0 if there is an error during the request.
    """
    try:
        response = requests.get(URL_POKEMON_API_BASE)
        response.raise_for_status()
        data = response.json()
        return data["count"]
    except requests.RequestException:
        print("Erreur lors de la requête pour récupération du nombre total de pokémons")
        return 0


def get_random_pokemon_id(pokemons_count):
    """
    :param pokemons_count: The total number of available Pokémon.
    :return: A random Pokémon ID within the range from 1 to pokemons_count.
    """
    return random.randint(1, pokemons_count)


def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: The ID of the Pokémon to fetch data for.
    :return: A dictionary containing the Pokémon data if the request is successful, otherwise None.
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
    Fetches a list of random Pokémon data.

    :return: A list of dictionaries where each dictionary represents a Pokémon's data.
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
    :param pokemon: A dictionary representing a Pokémon, including its statistics.
    :type pokemon: dict
    :return: The total strength of the Pokémon, calculated by summing up its base stats.
    :rtype: int
    """
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength


def get_type_advantage_multiplier(pokemon1, pokemon2, type_advantages):
    """
    :param pokemon1: Dictionary representing the first Pokemon with its types.
    :param pokemon2: Dictionary representing the second Pokemon with its types.
    :param type_advantages: Dictionary that maps Pokemon types to their advantages against other types.
    :return: A float representing the type advantage multiplier of the first Pokemon against the second.
    """
    # Récupérer les types des deux Pokémon
    types1 = [t['type']['name'] for t in pokemon1['types']]
    types2 = [t['type']['name'] for t in pokemon2['types']]
    multiplier = 1.0

    # Vérifier les avantages de type de pokemon1 contre pokemon2
    for t1 in types1:
        if t1 in type_advantages:
            for t2 in types2:
                if t2 in type_advantages[t1]:
                    multiplier *= 1.5  # Avantage de type
    return multiplier


def simulate_battle(pokemon1, pokemon2, type_advantages):
    """
    :param pokemon1: Dictionary representation of the first Pokémon, containing at least a 'name' key and other relevant attributes.
    :param pokemon2: Dictionary representation of the second Pokémon, containing at least a 'name' key and other relevant attributes.
    :param type_advantages: Dictionary that holds type advantage multipliers; keys are type pairs and values are multipliers.
    :return: The Pokémon dictionary of the winner of the battle.
    """
    # Calculer la force de chaque Pokémon
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    # Appliquer les avantages de type
    multiplier1 = get_type_advantage_multiplier(pokemon1, pokemon2, type_advantages)
    multiplier2 = get_type_advantage_multiplier(pokemon2, pokemon1, type_advantages)

    adjusted_strength1 = strength1 * multiplier1
    adjusted_strength2 = strength2 * multiplier2

    # Afficher les détails du combat
    print(f"Combat entre {pokemon1['name']} et {pokemon2['name']} :")
    print(f" - {pokemon1['name']} : Force totale = {strength1} (après avantage de type : {adjusted_strength1})")
    print(f" - {pokemon2['name']} : Force totale = {strength2} (après avantage de type : {adjusted_strength2})")

    # Déterminer le vainqueur
    if adjusted_strength1 > adjusted_strength2:
        print(f" --> Vainqueur : {pokemon1['name']}\n")
        return pokemon1
    elif adjusted_strength2 > adjusted_strength1:
        print(f" --> Vainqueur : {pokemon2['name']}\n")
        return pokemon2
    else:
        # En cas d'égalité parfaite, choisir un vainqueur aléatoire
        winner = random.choice([pokemon1, pokemon2])
        print(f" --> Égalité parfaite, vainqueur aléatoire : {winner['name']}\n")
        return winner


def simulate_round(pokemons, type_advantages):
    """
    :param pokemons: List of pokemons participating in the simulation round.
    :param type_advantages: Dictionary mapping pokemon types to their advantages.
    :return: List of winning pokemons for the given round.
    """
    winners = []
    for i in range(0, len(pokemons), 2):
        winner = simulate_battle(pokemons[i], pokemons[i + 1], type_advantages)
        winners.append(winner)
    return winners


def main():
    """
    Checks the number of participants to ensure it is a power of 2 and at least 2, retrieves type advantages and random Pokémon, then simulates battles between them until a champion is determined.

    :return: None
    """
    # Vérifier que le nombre de participants est une puissance de 2 et au moins égal à 2
    if NB_PARTICIPANTS < 2 or (NB_PARTICIPANTS & (NB_PARTICIPANTS - 1)) != 0:
        print("Le nombre de participants doit être une puissance de 2 et supérieur ou égal à 2.")
        return

    # Récupérer les avantages de type
    type_advantages = get_type_advantages()

    # Récupérer les Pokémon aléatoires
    random_pokemons = get_random_pokemons()
    print("Les 32 Pokémon choisis aléatoirement sont :")
    for i, pokemon in enumerate(random_pokemons, start=1):
        print(f"{i}. {pokemon['name']}")

    # Simuler les tours de combats
    round_number = 1
    current_pokemons = random_pokemons
    while len(current_pokemons) > 1:
        print(f"\n--- Tour {round_number} ---\n")
        current_pokemons = simulate_round(current_pokemons, type_advantages)
        round_number += 1

    # Afficher le champion
    print("\nLe champion est :")
    print(f"{current_pokemons[0]['name']}")


if __name__ == "__main__":
    main()