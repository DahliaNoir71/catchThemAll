import requests
import random

URL_POKEMON_API_BASE = "https://pokeapi.co/api/v2/pokemon"
NB_PARTICIPANTS = 16


def get_pokemons_count():
    """
    Fetches the total count of Pokémon from the Pokémon API.

    :return: The total count of Pokémon if the request is successful; otherwise, returns 0.
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
    :param pokemons_count: The total number of available Pokemon.
    :return: A random Pokemon ID between 1 and the total count.
    """
    return random.randint(1, pokemons_count)


def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: Identification number of the Pokémon to fetch data for
    :return: JSON response containing Pokémon data or None if an error occurs
    """
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Pas de pokémon avec l'ID : {pokemon_id}")
        return None


def get_random_pokemons():
    """
    :return: A list of random, unique Pokémon data dictionaries. The number of Pokémon returned is determined by the constant NB_PARTICIPANTS. Each Pokémon data dictionary contains information about the Pokémon fetched using its ID.
    """
    pokemons = []
    pokemons_count = get_pokemons_count()
    while len(pokemons) < NB_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemons_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons


def print_pokemon_info(pokemon):
    """
    :param pokemon: A dictionary containing information about a Pokémon, including its name, type(s), height, weight, stats, and abilities.
    :return: None
    """
    print(f"{pokemon['name']}")
    print(f"   - Type(s) : {[t['type']['name'] for t in pokemon['types']]}")
    print(f"   - Taille : {pokemon['height']}")
    print(f"   - Poids : {pokemon['weight']}")
    print(f"   - Statistiques :")
    for stat in pokemon['stats']:
        print(f"     * {stat['stat']['name']} : {stat['base_stat']}")
    print(f"   - Capacités : {[ability['ability']['name'] for ability in pokemon['abilities']]}")


def main():
    """
    Retrieves a list of random Pokémon and prints their information.

    :return: None
    """
    random_pokemons = get_random_pokemons()
    print("Les 16 Pokémon choisis aléatoirement sont :")
    for i, pokemon in enumerate(random_pokemons, start=1):
        print(f"{i}. ", end="")
        print_pokemon_info(pokemon)


if __name__ == "__main__":
    main()
