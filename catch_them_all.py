import requests
import random

URL_POKEMON_API_BASE = "https://pokeapi.co/api/v2/pokemon"
NB_PARTICIPANTS = 16




def get_pokemons_count():
    """
    Retrieves the total count of Pokémons from the Pokémon API.

    :return: The total number of Pokémons as an integer. Returns 0 if the request fails.
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
    :return: A random Pokémon ID within the range [1, pokemons_count].
    """
    return random.randint(1, pokemons_count)


def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: The ID of the Pokémon to fetch data for.
    :return: JSON data of the Pokémon if successful, otherwise None.
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
    :return: A list of unique random Pokémon data dictionaries. The list will contain a number
             of dictionaries equal to the value of NB_PARTICIPANTS. Each dictionary represents
             a single Pokémon's data fetched from an external source.
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
    :param pokemon: Dictionary containing the information about a Pokémon.
                    It should include keys such as 'name', 'types', 'height',
                    'weight', 'stats', and 'abilities', with corresponding
                    values describing the Pokémon's attributes.
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

def print_pokemons_infos(random_pokemons):
    """
    :param random_pokemons: A list containing randomly selected Pokémon objects
    :return: None
    """
    print(f"Les {NB_PARTICIPANTS} Pokémon choisis aléatoirement sont :")
    for i, pokemon in enumerate(random_pokemons, start=1):
        print(f"{i}. ", end="")
        print_pokemon_info(pokemon)


def main():
    """
    Main function to execute the random Pokemon selection and information display process.

    :return: None
    """
    random_pokemons = get_random_pokemons()
    print_pokemons_infos(random_pokemons)

if __name__ == "__main__":
    main()
