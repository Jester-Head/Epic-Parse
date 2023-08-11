import requests
from requests.auth import HTTPBasicAuth
import config


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
        self.base_url = config.BASE_URL
        self.namespace = config.NAMESPACE
        self.locale = config.LOCALE

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
        Sends a GET request to the specified URL and returns the JSON response.
        Raises an exception if the request fails.

        Parameters:
        - access_token (dict): A dictionary representing the access token to use for the request. The dictionary must have an 'access_token' key.
        - url (str): A string representing the URL to send the request to.

        Returns:
        - dict: A dictionary representing the JSON response from the API. The structure of this dictionary will depend on the specific API endpoint. If the request fails, returns None.
        """

        response = requests.get(url,timeout=0.001)
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

    def get_playable_spec_index(self, access_token):

        url = f"{self.base_url}playable-specialization/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)
    
    def get_talent_tree_index(self, access_token):
        url = f"{self.base_url}talent-tree/index?namespace={self.namespace}&locale={self.locale}"
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



