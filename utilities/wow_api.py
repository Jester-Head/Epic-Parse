import json
import re

import pandas as pd
import pymongo
import requests
from constant import CLIENT_ID, CLIENT_SECRET, CONNECTION, DB_NAME
from requests.auth import HTTPBasicAuth


class WoWData:
    """
    A class used to interact with the World of Warcraft (WoW) API to retrieve data.

    Attributes:
    - base_url (str): A string representing the base URL of the API.
    - namespace (str): A string representing the namespace to use for requests.
    - locale (str): A string representing the locale to use for requests.

    Methods:
    - get_data(access_token, url): Sends a GET request to the specified URL and returns the JSON response. Raises an exception if the request fails.
    - get_spells(access_token, document_type="spell", orderby="id"): Retrieves a list of spells from the WoW API.
    - get_talent_index(access_token): Retrieves the talent index from the WoW API.
    - get_pvp_talent_index(access_token): Retrieves the PvP talent index from the API.
    - get_tech_talent_index(access_token): Retrieves the tech talent index from the API.
    - get_description(access_token, spell_id): Retrieves the description of a spell with the specified ID from the API.
    - create_access_token(client_id, client_secret, region="us"): Generates an access token using the specified credentials.
    """

    def __init__(self):
        """
    Initializes a new instance of the WoWData class, setting up the base URL, namespace, and locale.
    """
        self.base_url = "https://us.api.blizzard.com/data/wow/"
        self.namespace = "static-us"
        self.locale = "en_US"

    def create_access_token(self, client_id, client_secret, region="us"):
        """
        Create an access token for accessing the WoW API.

        Parameters:
        - client_id (str): The client ID for your Blizzard API account.
        - client_secret (str): The client secret for your Blizzard API account.
        - region (str): The region to create the access token for. Default is "us".

        Returns:
        - dict: A dictionary containing the access token information, including the access token and its type.
        """
        url = f"https://{region}.battle.net/oauth/token"
        body = {"grant_type": "client_credentials"}
        auth = HTTPBasicAuth(client_id, client_secret)

        response = requests.post(url, data=body, auth=auth, timeout=5)
        return response.json()

    def get_data(self, access_token, url):
        """
        Sends a GET request to the specified URL and returns the JSON response. Raises an exception if the request fails.

        Parameters:
        - access_token (dict): A dictionary representing the access token to use for the request.
        - url (str): A string representing the URL to send the request to.

        Returns:
        - dict: A dictionary representing the JSON response from the API.
        """
        response = requests.get(url, timeout=5)
        if response.ok:
            return response.json()
        else:
            return None

#  Spell API

    def get_spells(self, access_token, document_type="spell", orderby="id", page="1"):
        """
        Retrieves a list of spells from the WoW API.

        Parameters:
        - access_token (dict): A dictionary representing the access token to use for the request.
        - document_type (str): A string representing the type of document to retrieve (default: "spell").
        - orderby (str): A string representing the field to order the results by (default: "id").
        - page (str): A string representing the page number to retrieve (default: "1").

        Returns:
        - dict: A dictionary representing the JSON response from the API.
        """
        url = f"{self.base_url}search/{document_type}?namespace={self.namespace}&orderby={orderby}&_page={page}"
        url += f"&access_token={access_token['access_token']}"

        return self.get_data(access_token, url)

    def get_spell_description(self, access_token, spell_id):
        """
        Retrieves the description of a specific spell in WoW using its ID.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.
        - spell_id (str): The ID of the spell to get the description for.

        Returns:
        - dict: A dictionary containing the description of the specified spell or None if the request was unsuccessful.
        """
        url = f"{self.base_url}spell/{spell_id}?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

#  Talent API

    def get_talent_index(self, access_token):
        """
        Retrieves the talent index from the WoW API.

        Parameters:
        - access_token (dict): A dictionary representing the access token to use for the request.

        Returns:
        - dict: A dictionary representing the JSON response from the API.
        """
        url = f"{self.base_url}talent/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_pvp_talent_index(self, access_token):
        """
        Retrieves the PvP talent index from the WoW API.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.

        Returns:
        - dict: A dictionary containing the PvP talent index data or None if the request was unsuccessful.
        """
        url = f"{self.base_url}pvp-talent/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_pvp_talent_description(self, access_token, pvp_talent_id):
        """
        Retrieves the description of a specific PvP talent in WoW using its ID.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.
        - pvp_talent_id (str): The ID of the PvP talent to get the description for.

        Returns:
        - dict: A dictionary containing the description of the specified PvP talent or None if the request was unsuccessful.
        """
        url = f"{self.base_url}pvp-talent/{pvp_talent_id}?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_talent_description(self, access_token, talent_id):
        """
        Retrieves the description of a specific talent in WoW using its ID.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.
        - talent_id (str): The ID of the talent to get the description for.

        Returns:
        - dict: A dictionary containing the description of the specified talent or None if the request was unsuccessful.
        """
        url = f"{self.base_url}talent/{talent_id}?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_talent_tree(self, access_token, talent_tree):
        """
        Retrieves the description of a specific talent in WoW using its ID.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.
        - talent_id (str): The ID of the talent to get the description for.

        Returns:
        - dict: A dictionary containing the description of the specified talent or None if the request was unsuccessful.
        """
        url = f"{self.base_url}talent-tree/{talent_tree}?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_spec_tree(self, access_token, talent_tree, spec_Id):
        """
        Retrieves the description of a specific talent in WoW using its ID.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.
        - talent_id (str): The ID of the talent to get the description for.

        Returns:
        - dict: A dictionary containing the description of the specified talent or None if the request was unsuccessful.
        """
        url = f"{self.base_url}talent-tree/{talent_tree}/playable-specialization/{spec_Id}?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)
#  Tech Talent API

    def get_tech_talent_index(self, access_token):
        """
        Retrieves the tech talent index from the WoW API.

        Parameters:
        - access_token (dict): A dictionary containing the access token returned by `create_access_token()`.

        Returns:
        - dict: A dictionary containing the tech talent index data or None if the request was unsuccessful.
        """
        url = f"{self.base_url}tech-talent/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)


########################################################

def get_spell_index(access_token, filename):
    """
    Writes all spells to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - filename (str): The filename to write the spells to.

    Returns:
    - None.
    """
    wow_data = WoWData()
    # Get the first page of spells.
    response = wow_data.get_spells(access_token)
    # Get the number of pages of spells.
    page_count = response["pageCount"]
    with open(filename, "a+") as f:
        # Write the first page of spells to the file.
        f.write("[" + json.dumps(response, indent=4))
        # Iterate through the remaining pages of spells.
        for page in range(2, page_count + 1):
            response = wow_data.get_spells(access_token, page=str(page))
            f.write("," + json.dumps(response, indent=4))
        f.write("]")
    return


def get_all_spells(access_token, read_file, write_file):
    """
    Retrieves descriptions of all spells and writes them to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - read_file (str): The filename to read the spells from.
    - write_file (str): The filename to write the spell descriptions to.

    Returns:
    - None.
    """
    with open(file=read_file, mode='r+', encoding='utf-8') as rf:
        # Read the spell data from the read_file.
        data = json.loads(rf.read())
    with open(write_file, mode='a+', encoding='utf-8') as wf:
        # Start writing the spell descriptions as a JSON array.
        wf.write("[")
        for spells in data:
            for spell in spells['results']:
                # Get the description of each spell using its ID.
                response = WoWData().get_spell_description(
                    access_token=access_token, spell_id=spell['data']['id'])
                wf.write(json.dumps(response, indent=4) + ',')
    remove_last_comma(write_file)
    with open(write_file, '+a') as f:
        # Complete the JSON array by adding the closing square bracket.
        f.write(']')
    return


def get_all_talent_trees(access_token, data=None, collection=None, file=None):
    wow = WoWData()
    with open(file=file, mode='a+', encoding='utf-8') as f:
        f.write('[')
        for d in data:
            response = wow.get_talent_tree(access_token, d)
            f.write(json.dumps(response, indent=4) + ',')
    remove_last_comma(file)
    with open(file=file, mode='+a') as f:
        # Complete the JSON array by adding the closing square bracket.
        f.write(']')
    return


def extract_spec_info(file=None):
    # Read the file
    df = pd.read_csv(file)

    # Initialize lists to hold the extracted values
    talent_tree = []
    spec = []

    # Iterate through each row in the dataframe
    for link in df['url']:
        # Extract the numbers following "talent-tree/" and "playable-specialization/"
        # using regular expressions
        match = re.search(
            r'talent-tree/(\d+)/playable-specialization/(\d+)', link)
        if match:
            # If a match was found, add the numbers to the respective lists
            talent_tree.append(int(match.group(1)))
            spec.append(int(match.group(2)))
        else:
            # If no match was found, add NaN to the respective lists
            talent_tree.append(None)
            spec.append(None)

    # Add the extracted values as new columns in the dataframe
    df['talent_tree'] = talent_tree
    df['spec'] = spec

    df[['talent_tree', 'spec']]
    # Initialize lists to hold the extracted values
    talent_tree = []
    spec = []

    # Iterate through each row in the dataframe
    for url in df['url']:
        # Extract the numbers following "talent-tree/" and "playable-specialization/"
        # using regular expressions
        match = re.search(
            r'talent-tree/(\d+)/playable-specialization/(\d+)', url)
        if match:
            # If a match was found, add the numbers to the respective lists
            talent_tree.append(int(match.group(1)))
            spec.append(int(match.group(2)))
        else:
            # If no match was found, add NaN to the respective lists
            talent_tree.append(None)
            spec.append(None)

    # Add the extracted values as new columns in the dataframe
    df['talent_tree'] = talent_tree
    df['spec'] = spec

    return df[['name', 'talent_tree', 'spec']]


def get_all_spec_trees(access_token, data=None, file='temp.json'):
    """
    Makes API requests to obtain spec trees and saves all responses in a single JSON file.

    This function takes data with talent tree and spec IDs, along with an access token, to make API requests and saves all the responses in a single JSON file specified by the 'file' parameter.

    Parameters:
        access_token (str): The access token required to make API requests.
        data (dict): Data containing talent tree and spec IDs for API requests. Default is None.
        file (str): The name of the output JSON file to save all responses. Default is 'temp.json'.

    Returns:
        None
    """
    if data is None:
        raise ValueError("Data must be provided to make API requests.")

    with open(file, 'w', encoding='utf-8') as f:
        f.write('[')
        for i in range(len(data)):
            response = WoWData().get_spec_tree(access_token=access_token, talent_tree=data[i]['talent_tree'], spec_Id=data[i]['spec'])
            f.write(json.dumps(response, indent=4) + ',')
        f.write(']')
        

def get_all_spec_trees(file):
    """
    Reads data from the specified JSON file and saves each response in separate JSON files.

    This function reads data from the specified JSON file, processes it, and saves each response from the data in separate JSON files. The filenames will be derived from the 'name' column in the DataFrame.

    Parameters:
        file (str): The path to the JSON file containing the data.

    Returns:
        None
    """
    access_token = WoWData().create_access_token(CLIENT_ID, CLIENT_SECRET)
    df = extract_spec_info(file)
    spec_names = df['name']
    for i in range(len(spec_names)):
        df2 = df.iloc[i][:]
        talent_tree = df2['talent_tree']
        spec_Id = df2['spec']
        response = WoWData().get_spec_tree(access_token=access_token, talent_tree=talent_tree, spec_Id=spec_Id)
        file_name = f'{spec_names[i]}.json'
        with open(file_name, 'w') as f:
            f.write(json.dumps(response, indent=4))


def add_to_db(collection, data):
    """
    Add data to a MongoDB collection by inserting the 'results' list of each set of data provided
    into the specified collection within the MongoDB database.

    Parameters:
    - collection (pymongo.collection.Collection): The MongoDB collection where the data will be inserted.
    - data (list): The data to be inserted into the collection.

    Returns:
    - None
    """
    pattern = r"static-(\d+\.\d+\.\d+)"
    patch = ''
    for d in data:
        pattern = r"static-(\d+\.\d+\.\d+)"
        link = d['_links']['self']['href']
        patch = re.findall(pattern, link)
        # Insert each data entry into the collection.
        collection.insert_one(d)
    # Update the 'patch' field for all documents in the collection.
    collection.update_many({}, {"$set": {"patch": patch[0]}})
    return


def get_all_pve_talents(access_token, file='PvEtemp.json'):
    """
    Retrieves descriptions of all PvE talents and writes them to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - file (str): The filename to write the talent descriptions to. Default is 'PvEtemp.json'.

    Returns:
    - None or str: Returns None if successful or an error message if there is no response.
    """
    response = WoWData().get_talent_index(access_token=access_token)
    if response:
        talents = response['talents']
        talent_ids = list()
        with open(file, '+a') as f:
            f.write('[')
            for talent in talents:
                talent_ids.append(talent['id'])
            for talent_id in talent_ids:
                desc = WoWData().get_talent_description(
                    access_token=access_token, talent_id=talent_id)
                f.write(json.dumps(desc, indent=4) + ',')
        remove_last_comma(file)
        with open(file, '+a') as f:
            f.write(']')
        return
    else:
        return 'Error: No Response'


def get_all_pvp_talents(access_token, file='PvPtemp.json'):
    """
    Retrieves descriptions of all PvP talents and writes them to a file.

    Parameters:
    - access_token (str): The WoW API access token.
    - file (str): The filename to write the talent descriptions to. Default is 'PvPtemp.json'.

    Returns:
    - None or str: Returns None if successful or an error message if there is no response.
    """
    response = WoWData().get_pvp_talent_index(access_token)
    if response:
        talents = response['pvp_talents']
        talent_ids = list()
        with open(file, '+a') as f:
            f.write('[')
            for talent in talents:
                talent_ids.append(talent['id'])
            for talent_id in talent_ids:
                desc = WoWData().get_pvp_talent_description(
                    access_token=access_token, pvp_talent_id=talent_id)
                f.write(json.dumps(desc, indent=4) + ',')
        remove_last_comma(file)
        with open(file, '+a') as f:
            f.write(']')
        return
    else:
        return 'Error: No Response'


def remove_last_comma(file):
    """
    Removes the last comma from a file.

    Parameters:
    - file (str): The filename of the file from which the comma will be removed.

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


def connect(collection, con=CONNECTION, db_name=DB_NAME):
    """
    Connects to a MongoDB collection and returns the collection object.

    Parameters:
    - collection (str): The name of the collection to connect to.
    - con (str): The MongoDB connection string. Default is CONNECTION.
    - db_name (str): The name of the database. Default is DB_NAME.

    Returns:
    - pymongo.collection.Collection: The MongoDB collection object.
    """
    client = pymongo.MongoClient(con)
    db = client[db_name]
    Collection = db[collection]
    return Collection



