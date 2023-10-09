
import hashlib
import json
import os
import re

import pandas as pd
from config import CLASSES, CLIENT_ID, CLIENT_SECRET, ALL_ABILITIES, EXCLUDED_EXT, PVE_TALENTS_CSV, PVP_TALENTS_CSV, SPELLS_CSV

from wow_api import WoWData


def load_json_data(path):
    """
    Loads JSON data from a file and converts it to a DataFrame.

    This function reads JSON data from a file and converts it to a DataFrame using `pd.json_normalize()`.

    Args:
        path (str): Path to the JSON file.

    Returns:
        DataFrame: DataFrame containing the JSON data.

    Raises:
        FileNotFoundError: If the specified file is not found.
        JSONDecodeError: If the file does not contain valid JSON data.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data = pd.json_normalize(data)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data in file: {path}, Error: {e}")


def extract_info_from_url(url):
    """ 
    Extracts talent tree and specialization numbers from a provided URL.

    Parameters:
    - url (str): The URL from which to extract information.

    Returns:
    - tuple: A tuple containing talent tree and specialization numbers or (None, None) if no match is found.
    """
    match = re.search(r'talent-tree/(\d+)/playable-specialization/(\d+)', url)
    return tuple(map(int, match.groups())) if match else (None, None)


def extract_spec_talent_trees(json_file):
    """ 
    Extracts specialization and talent tree information from a JSON file and returns it as a DataFrame.

    Parameters:
    - json_file (str): Path to the JSON file containing talent tree information.

    Returns:
    - DataFrame: A DataFrame with columns for talent tree ID, specialization ID, class name, and class-specification.
    """
    df = load_json_data(json_file)
    specs = df['spec_talent_trees']
    spec = specs[0]
    spec_df = pd.DataFrame(spec)
    spec_df['url'] = pd.json_normalize(spec_df['key'])
    spec_df.drop(columns=['key'], inplace=True)
    return spec_df


def save_spec_trees(read_file, write_dir):
    """ 
    Reads talent tree information from a CSV file and saves each talent tree's data as a separate JSON file.

    Parameters:
    - read_file (str): Path to the CSV file containing talent tree information.
    - write_dir (str): Directory where the JSON files will be saved.

    Returns:
    - None
    """
    wow = WoWData()
    access_token = wow.create_access_token(CLIENT_ID, CLIENT_SECRET)
    talent_tree_info_df = extract_talent_tree_info(read_file)
    spec_names = talent_tree_info_df['name']
    class_spec = talent_tree_info_df['class_spec']
    for i in range(len(spec_names)):
        df2 = talent_tree_info_df.iloc[i][:]
        talent_tree = df2['talent_tree']
        spec_id = df2['spec']
        response = wow.get_spec_tree(
            access_token=access_token, talent_tree=talent_tree, spec_Id=spec_id)
        file_name = f'{write_dir}\{class_spec[i]}.json'
        with open(file_name, 'w+') as f:
            f.write(json.dumps(response, indent=4))


def merge_frames(spell_nodes, choice_tooltip):
    """
    Merge two DataFrames, 'choice_tooltip' and 'spell_nodes', based on specific column mappings.

    Parameters:
    - choice_tooltip (pandas.DataFrame): The DataFrame containing choice tooltip data.
    - spell_nodes (pandas.DataFrame): The DataFrame containing spell nodes data.

    Returns:
    - pandas.DataFrame: The merged DataFrame.
    """
    choice_tooltip_mapping = {
        'talent.key.href': 'talent_href',
        'talent.name': 'talent_name',
        'talent.id': 'talent_id',
        'spell_tooltip.spell.key.href': 'spell_href',
        'spell_tooltip.spell.name': 'spell_name',
        'spell_tooltip.spell.id': 'spell_id',
        'spell_tooltip.description': 'spell_description',
        'spell_tooltip.cast_time': 'cast_time',
        'spell_tooltip.power_cost': 'power_cost',
        'spell_tooltip.cooldown': 'cooldown'
    }
    spell_node_mapping = {
        'rank': 'rank',
        'default_points': 'default_points',
        'tooltip.talent.key.href': 'talent_href',
        'tooltip.talent.name': 'talent_name',
        'tooltip.talent.id': 'talent_id',
        'tooltip.spell_tooltip.spell.key.href': 'spell_href',
        'tooltip.spell_tooltip.spell.name': 'spell_name',
        'tooltip.spell_tooltip.spell.id': 'spell_id',
        'tooltip.spell_tooltip.description': 'spell_description',
        'tooltip.spell_tooltip.cast_time': 'cast_time',
        'tooltip.spell_tooltip.power_cost': 'power_cost',
        'tooltip.spell_tooltip.cooldown': 'cooldown',
        'tooltip.spell_tooltip.range': 'tooltip_range',
        'choice_of_tooltips': 'choice_of_tooltips'
    }

    spell_nodes.rename(columns=spell_node_mapping, inplace=True)
    choice_tooltip.rename(columns=choice_tooltip_mapping, inplace=True)
    df = pd.merge(choice_tooltip, spell_nodes, how='outer', on=[
                  'talent_href', 'talent_name', 'talent_id', 'spell_href', 'spell_name', 'spell_id', 'spell_description', 'cast_time'])
    return df


def flatten_trees(json_file):
    """
    Flatten specific nodes from the JSON data in the specified file.

    This function loads JSON data from a file, flattens specific nodes, and returns the extracted data as a DataFrame.

    Parameters:
        json_file (str): The path to the JSON file.

    Returns:
        DataFrame: DataFrame containing the flattened nodes.
    """
    # Load JSON data from the file
    df = load_json_data(json_file)

    # Flatten the 'class_talent_nodes' node
    class_nodes = pd.json_normalize(df['class_talent_nodes'], sep='_')
    spell_nodes = pd.json_normalize(
        class_nodes.iloc[0], record_path=['ranks'], errors='ignore')

    # Extract choice nodes and flatten them further
    nodes = spell_nodes['choice_of_tooltips'].dropna(
    ).explode().reset_index()
    spell_nodes = spell_nodes.drop(columns=['choice_of_tooltips'])
    choice_nodes = pd.json_normalize(nodes['choice_of_tooltips'])

    return spell_nodes, choice_nodes


def extract_talent_tree_info(csv_file):
    """ 
    Extracts talent tree information from a CSV dataset.

    Parameters:
    - csv_file (str): Path to the CSV file containing the dataset.

    Returns:
    - DataFrame: A DataFrame containing the extracted talent tree information.
    """
    df = pd.read_csv(csv_file)

    # Extract talent tree and specialization from the 'url' column using the helper function
    df[['talent_tree', 'spec']] = df['url'].apply(
        extract_info_from_url).apply(pd.Series)

    # Perform additional computations
    if 'talent_tree' in df.columns:
        df['class'] = df['talent_tree'].apply(lambda x: CLASSES[f'{x}'])
        df['class_spec'] = df['name'] + ' ' + df['class']

    return df


def flatten_pve_to_dataframe(pve_data):
    """
    Function to flatten each talent entry with handling missing keys.

    Args:
        pve_data (list): A list of dictionaries, each containing details about a PvE talent.

    Returns:
        DataFrame: A pandas DataFrame containing a flattened version of the input dictionary, 
                   where each key-value pair from the dictionary corresponds to a column in the DataFrame.
                   Each DataFrame will have a single row.
    """
    def flatten_entry_safe(entry):
        flattened = {
            '_links_self_href': entry['_links']['self']['href'] if '_links' in entry and 'self' in entry['_links'] else None,
            'id': entry.get('id'),
            'spell_key_href': entry['spell']['key']['href'] if 'spell' in entry and 'key' in entry['spell'] else None,
            'spell_name': entry['spell'].get('name') if 'spell' in entry else None,
            'spell_id': entry['spell'].get('id') if 'spell' in entry else None,
            'playable_class_key_href': entry['playable_class']['key']['href'] if 'playable_class' in entry and 'key' in entry['playable_class'] else None,
            'playable_class_name': entry['playable_class'].get('name') if 'playable_class' in entry else None,
            'playable_class_id': entry['playable_class'].get('id') if 'playable_class' in entry else None,
            'playable_specialization_key_href': entry['playable_specialization']['key']['href'] if 'playable_specialization' in entry and 'key' in entry['playable_specialization'] else None,
            'playable_specialization_name': entry['playable_specialization'].get('name') if 'playable_specialization' in entry else None,
            'playable_specialization_id': entry['playable_specialization'].get('id') if 'playable_specialization' in entry else None
        }

        # Add rank descriptions
        for i in range(1, 4):  # Assuming maximum of 3 ranks for simplicity
            rank_key = f'rank_{i}_description'
            if 'rank_descriptions' in entry and len(entry['rank_descriptions']) >= i:
                flattened[rank_key] = entry['rank_descriptions'][i -
                                                                 1].get('description')
            else:
                flattened[rank_key] = None

        return flattened

    # Flatten each entry in the JSON data with the safe method
    flattened_pve_data = [flatten_entry_safe(entry) for entry in pve_data]

    # Convert to DataFrame and return
    return pd.DataFrame(flattened_pve_data)


def flatten_pvp_to_dataframe(pvp_data):
    """
    Flattens a list of PvP talent entries from World of Warcraft and returns a DataFrame.

    Args:
        pvp_data (list): A list of dictionaries, each containing details about a PvP talent.

    Returns:
        DataFrame: A pandas DataFrame with each talent entry flattened into a row.
    """

    # Helper function to flatten each individual PvP talent entry
    def flatten_pvp_entry(entry):
        flattened = {
            '_links_self_href': entry['_links']['self']['href'] if '_links' in entry and 'self' in entry['_links'] else None,
            'id': entry.get('id'),
            'spell_key_href': entry['spell']['key']['href'] if 'spell' in entry and 'key' in entry['spell'] else None,
            'spell_name': entry['spell'].get('name') if 'spell' in entry else None,
            'spell_id': entry['spell'].get('id') if 'spell' in entry else None,
            'playable_specialization_key_href': entry['playable_specialization']['key']['href'] if 'playable_specialization' in entry and 'key' in entry['playable_specialization'] else None,
            'playable_specialization_name': entry['playable_specialization'].get('name') if 'playable_specialization' in entry else None,
            'playable_specialization_id': entry['playable_specialization'].get('id') if 'playable_specialization' in entry else None,
            'description': entry.get('description'),
            'unlock_player_level': entry.get('unlock_player_level')
        }

        # Add compatible slots
        for i in range(1, 5):  # Assuming maximum of 4 slots for simplicity
            slot_key = f'slot_{i}'
            if 'compatible_slots' in entry and len(entry['compatible_slots']) >= i:
                flattened[slot_key] = entry['compatible_slots'][i-1]
            else:
                flattened[slot_key] = None

        return flattened

    # Flatten each entry in the provided PvP data
    flattened_pvp_data = [flatten_pvp_entry(entry) for entry in pvp_data]

    # Convert to DataFrame and return
    return pd.DataFrame(flattened_pvp_data)

def add_class_spec_name(data_frame, file_path, excluded_extensions=EXCLUDED_EXT):
    """
    Add class name to the data frame based on the file name.

    This function extracts the class name from the provided file name and adds it as a new column
    'playable_class.name' to the data frame.

    Parameters:
        data_frame (pd.DataFrame): The input data frame to which the class name will be added.
        file_path (str): The path to the file containing the talent tree data.
        excluded_extensions (list): List of file extensions to exclude from the file name.

    Returns:
        pd.DataFrame: The updated data frame with the 'playable_class.name' column added.
    """
    basename = os.path.basename(file_path)

    # Remove specified extensions from the file name
    if excluded_extensions:
        for extension in excluded_extensions:
            basename = re.sub(rf'(\.{extension})', '', basename)

    # Remove any remaining spaces or underscores
    class_name = re.sub(r'(\s|_|\.+)', '', basename).strip()

    # List of class names without spaces
    classes = [str.replace(c, ' ', '') for c in list(CLASSES.values())]

    # Check if the extracted name matches any class name
    class_name = class_name if class_name in classes else None

    # Add the class name to the data frame
    data_frame['playable_class.name'] = class_name

    return data_frame



def extract_talent_nodes(file_path):
    """
    Extracts talent nodes from a JSON file and processes them into a DataFrame.

    This method reads a JSON file containing talent nodes, extracts relevant 
    information about spells associated with each talent node, and returns a 
    DataFrame with the spell's name and its description.

    Nodes without the 'ranks' key are skipped during the extraction process.

    Parameters:
    - file_path (str): The path to the JSON file to be processed.

    Returns:
    - DataFrame: A DataFrame with columns 'spell_name' and 'description'. 

    Raises:
    - FileNotFoundError: If the specified file_path does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    data = load_json_data(file_path)
    data.drop(columns='spec_talent_trees', inplace=True)

    # Flatten the 'talent_nodes' key and filter out nodes without 'ranks'
    nodes = data['talent_nodes'].explode().dropna()
    nodes_with_ranks = nodes[nodes.apply(lambda x: 'ranks' in x)]

    talent_nodes_df = pd.json_normalize(
        nodes_with_ranks, record_path=['ranks'], errors='ignore')

    spells = talent_nodes_df[[
        'tooltip.spell_tooltip.spell.name', 'tooltip.spell_tooltip.description']].dropna()

    spells.rename(columns={'tooltip.spell_tooltip.spell.name': 'spell_name',
                           'tooltip.spell_tooltip.description': 'description'}, inplace=True)
    spells=add_class_spec_name(spells,file_path)
    return spells



