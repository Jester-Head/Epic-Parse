import json
import os
import pandas as pd
from data_processing import extract_talent_nodes, flatten_pve_to_dataframe, flatten_trees, merge_frames, add_class_spec_name


def start_json_file(file):
    """ 
    Prepares a file for writing JSON data by adding an opening square bracket.

    Parameters:
    - file (str): The filename or path to the file.

    Returns:
    - None
    """
    with open(file, 'w+') as f:
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


def convert_talents_to_csv(path, json_data):
    # Flatten each entry in the JSON data with the safe method
    flattened_data_safe = [flatten_pve_to_dataframe(
        entry) for entry in json_data]

    # Convert to DataFrame
    df_safe = pd.DataFrame(flattened_data_safe)

    # Export to CSV
    df_safe.to_csv(path, index=False)


def update_talents_csv(file_dir):
    """
    Update CSV files located in the specified directory with class and spec names.

    The function will:
    1. List all files in the provided directory.
    2. For each file, read its contents into a DataFrame.
    3. Add class and spec names to the DataFrame using the add_class_spec_name function.
    4. Write the updated DataFrame back to the same file, overwriting the original contents.

    Args:
    - file_dir (str): Path to the directory containing the CSV files to be updated.

    Returns:
    None

    Notes:
    - This function assumes that the add_class_spec_name function is defined and takes a DataFrame and a filename as its arguments.
    - It overwrites the original files in place with the updated data.
    """
    file_list = os.listdir(file_dir)
    file_p = [os.path.join(file_dir, f) for f in file_list]
    for file in file_p:
        df = add_class_spec_name(pd.read_csv(file), file)
        df.to_csv(file, index=False, mode='w+')


def combine_files(source_directory, output_file, file_extension='.csv'):
    """
    Combine all files with a specific extension from a directory and its subdirectories into a single file using pandas.

    Args:
    - source_directory (str): Path to the directory to start searching for files.
    - output_file (str): Path to the output file where all contents will be written.
    - file_extension (str): Extension of the files to be combined. Default is '.csv'.

    Returns:
    None
    """

    # Create a list comprehension to capture all file paths
    file_paths = [os.path.join(dirpath, filename)
                  for dirpath, dirnames, filenames in os.walk(source_directory)
                  for filename in filenames if filename.endswith(file_extension)]

    # Read and concatenate all the dataframes
    all_data = pd.concat([pd.read_csv(filepath)
                         for filepath in file_paths], ignore_index=True)

    # Write the combined dataframe to the output file
    all_data.to_csv(output_file, index=False)


def convert_talent_nodes_csv(source_directory):
    """
    Converts JSON files in a given directory to CSV format.

    This function searches for all JSON files within the specified directory.
    For each JSON file, it extracts the talent nodes using the 
    `extract_talent_nodes` function and then saves the resulting data 
    as a CSV file in the same directory. Existing CSV files in the directory 
    are skipped during the conversion process.

    Parameters:
    - source_directory (str): The path to the directory containing the JSON files.

    Returns:
    None. The resulting CSV files are saved directly to the source directory.

    Note:
    - Ensure that the `os` module is imported before using this function.
    - This function relies on the `extract_talent_nodes` function to process the JSON data.
    """
    json_name = list()
    for root, dirs, files in os.walk(source_directory):
        for name in files:
            if not name.endswith('.csv'):  # Skip .csv files
                json_name.append(name)

    for n in json_name:
        df = extract_talent_nodes(source_directory+n)
        csv_name = str.replace(n, '.json', '.csv')
        df.to_csv(source_directory+csv_name, index=False, header=df.columns)
