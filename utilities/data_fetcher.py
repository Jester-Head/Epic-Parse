from config import CLASSES
from file_utils import finish_json_file, read_json_file, remove_last_comma, start_json_file, write_json_array_to_file
from data_processing import extract_info_from_url, extract_spec_talent_trees
from wow_api import WoWData
import pandas as pd


def get_spell_index(access_token, filename='spell_index.json'):
    """Writes all spells to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - filename (str): The filename to write the spells to.

    Returns:
    - None
    """
    start_json_file(filename)
    wow_data = WoWData()
    response = wow_data.get_spells(access_token)
    page_count = response["pageCount"]
    write_json_array_to_file(filename, response)
    for page in range(2, page_count + 1):
        response = wow_data.get_spells(access_token, page=str(page))
        write_json_array_to_file(filename, response)
    remove_last_comma(filename)
    finish_json_file(filename)
    return


def get_all_spells(access_token, read_file, write_file='spells.json'):
    """Retrieves descriptions of all spells and writes them to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - read_file (str): The filename to read the spells from.
    - write_file (str): The filename to write the spell descriptions to.

    Returns:
    - None
    """
    start_json_file(write_file)
    data = read_json_file(read_file)
    df = pd.json_normalize(data, record_path=['results'])
    spell_ids = list(df['data.id'])

    for spell_id in spell_ids:
        response = WoWData().get_spell_description(
            access_token=access_token, spell_id=spell_id)
        write_json_array_to_file(write_file, response)

    remove_last_comma(write_file)
    finish_json_file(write_file)


def save_talent_index(file, func):
    """
    Executes a provided function to retrieve the talent index data and saves it as a JSON file.

    Parameters:
    - file (str): The filename to which the talent index will be written.
    - func (function): A function that, when executed, will return the talent index data. This function should not require any arguments.

    Note: This function does not return a value. If there is no response from the 'func' function, the file will be written with whatever 'func' returns, which could be an empty array or None.

    The resulting JSON file structure will include a list of all the talent IDs available in the game.
    """
    response = func
    write_json_array_to_file(file, response)
    remove_last_comma(file)


def get_all_pve_talents(access_token, read_file, write_file='pve_talents.json'):
    """
    Retrieves descriptions of all PvE talents from the WoW API and writes them to a JSON file.

    Parameters:
    - access_token (str): The WoW API access token.
    - read_file (str): The filename from which the talent IDs will be read.
    - write_file (str): The filename to which the talent descriptions will be written. The default is 'pve_talents.json'.

    Note: This function does not return a value. If there is no response from the API, an error message will be printed to the console.

    The resulting JSON file will contain descriptions for each talent ID read from the 'read_file'.
    """
    start_json_file(write_file)
    data = read_json_file(read_file)
    for talents in data['talents']:
        desc = WoWData().get_talent_description(
            access_token=access_token, talent_id=talents['id'])
        write_json_array_to_file(write_file, desc)
    remove_last_comma(write_file)
    finish_json_file(write_file)
    return


def get_all_pvp_talents(access_token, read_file, write_file='pvp_talents.json'):
    """
    Retrieves descriptions of all PvP talents and writes them to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - file (str): The filename to write the talent descriptions to. Default is 'PvPtemp.json'.

    Returns:
    - None: This function does not return a value. If there is no response from the API, an error message is printed to the console.
    """

    start_json_file(write_file)
    data = read_json_file(read_file)
    for talents in data['pvp_talents']:
        desc = WoWData().get_pvp_talent_description(
            access_token=access_token, pvp_talent_id=talents['id'])
        write_json_array_to_file(write_file, desc)
    remove_last_comma(write_file)
    finish_json_file(write_file)
    return


def save_talent_tree_index(access_token, file):
    """
    Fetch talent tree index data from the API and save it as a JSON file.

    This function makes an API request to fetch talent tree index data from the World of Warcraft API.
    The API request is made using the provided access token, and the talent tree index data is saved as a JSON file specified by the 'file' parameter.

    Parameters:
    - access_token (str): The access token required to make API requests.
    - file (str): The filename to which the talent tree index data will be written as a JSON file.

    Returns:
    - None: This function does not return a value.
    """
    response = WoWData().get_talent_tree_index(access_token=access_token)
    write_json_array_to_file(filename=file, data=response)
    remove_last_comma(file)


def save_talent_tree_nodes(access_token, read_file, write_file):
    """
    Fetch and save talent tree nodes for each class and specialization.

    This function retrieves talent tree nodes for each class and specialization
    specified in the input JSON file, and saves the responses as separate JSON files.

    Parameters:
        access_token (str): The access token required to make API requests.
        read_file (str): The path to the JSON file containing class and specialization data.
        write_file (str): The base path for saving the talent tree node JSON files.

    Returns:
        None
    """
    # Extract class and specialization information from the JSON file
    df = extract_spec_talent_trees(read_file)
    urls = df['url'].apply(extract_info_from_url)

    for url in urls:
        name = CLASSES[str(url[0])]
        talentTreeId = str(url[0])
        file = f'{write_file}{name}.json'
        file = str.replace(file, ' ', '')
        start_json_file(file)

        # Fetch talent tree nodes and save the response as a JSON file
        response = WoWData().get_talent_tree_nodes(access_token, talentTreeId)
        write_json_array_to_file(filename=file, data=response)
        remove_last_comma(file)
        finish_json_file(file)
