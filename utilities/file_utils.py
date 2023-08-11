import json
import os
import pandas as pd
from data_processing import flatten_pve_to_dataframe, flatten_trees, merge_frames


def start_json_file(file):
    """ 
    Prepares a file for writing JSON data by adding an opening square bracket.

    Parameters:
    - file (str): The filename or path to the file.

    Returns:
    - None
    """
    with open(file, 'w') as f:
        f.write("[")
    pass


def finish_json_file(file):
    """ 
    Finalizes the JSON file by adding a closing square bracket.

    Parameters:
    - file (str): The filename or path to the file.

    Returns:
    - None
    """
    with open(file, 'a+') as f:
        f.write("]")


def write_json_array_to_file(filename, data, end=False):
    with open(filename, 'a+') as f:
        f.write(json.dumps(data, indent=4) + ("" if end else ","))


def remove_last_comma(file):
    """ 
    Removes the last comma in a file to ensure valid JSON formatting.

    Parameters:
    - file (str): The filename or path to the file.

    Returns:
    - None
    """
    with open(file, 'r+') as f:
        f.seek(0, 2)  # Move the file pointer to the end of the file
        pos = f.tell()  # Get the current position of the file pointer
        pos -= 1  # Move one position back to skip the last comma
        while pos >= 0:
            f.seek(pos)
            char = f.read(1)
            if char == ',':
                f.seek(pos)
                f.truncate()  # Delete the comma
                break
            pos -= 1


def convert_json_to_csv(directory):
    """ 
    Converts all JSON files in a specified directory to CSV format.

    Parameters:
    - directory (str): The directory containing the JSON files to convert.

    Returns:
    - None
    """
    for root, dirs, files in os.walk(directory):
        for name in files:
            csv_name = str.replace(name, '.json', '.csv')
            spell_nodes, choice_nodes = flatten_trees(os.path.join(root, name))
            df = merge_frames(spell_nodes, choice_nodes)

            if 'power_cost_x' in df.columns:
                df["power_cost_x"].fillna('', inplace=True)
                df["power_cost_y"].fillna('', inplace=True)
                df["power_cost"] = df["power_cost_x"] + "" + df["power_cost_y"]
                df.drop(columns=['power_cost_x', 'power_cost_y'], inplace=True)

            if 'cooldown_x' in df.columns:
                df["cooldown_x"].fillna('', inplace=True)
                df["cooldown_x"].fillna('', inplace=True)
                df["cooldown"] = df['cooldown_x'] + df["cooldown_y"]
                df.drop(columns=['cooldown_x', 'cooldown_y'], inplace=True)

            output_dir = 'data/talent_trees_csv'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            df.to_csv(os.path.join(output_dir, csv_name), index=False)


def read_json_file(filename):
    with open(filename, 'r+') as f:
        try:
            return json.loads(f.read())
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            return None


def convert_talents_to_csv(path,json_data):
    # Flatten each entry in the JSON data with the safe method
    flattened_data_safe = [flatten_pve_to_dataframe(entry) for entry in json_data]

    # Convert to DataFrame
    df_safe = pd.DataFrame(flattened_data_safe)

    # Export to CSV
    df_safe.to_csv(path, index=False)