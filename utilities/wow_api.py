import requests
from requests.auth import HTTPBasicAuth

class WoWData:
    """
    A class that interacts with the World of Warcraft API to retrieve data.

    Attributes:
    - base_url: A string representing the base URL of the API.
    - namespace: A string representing the namespace to use for requests.
    - locale: A string representing the locale to use for requests.

    Methods:
    - get_data(access_token, url): Sends a GET request to the specified URL and returns the JSON response.
    - get_spells(access_token, document_type="spell", orderby="id"): Retrieves a list of spells from the API.
    - get_talent_index(access_token): Retrieves the talent index from the API.
    - get_pvp_talent_index(access_token): Retrieves the PvP talent index from the API.
    - get_tech_talent_index(access_token): Retrieves the tech talent index from the API.
    - get_description(access_token, spell_id): Retrieves the description of a spell with the specified ID from the API.
    - create_access_token(client_id, client_secret, region="us"): Generates an access token using the specified credentials.
    """

    def __init__(self):
        """
        Initializes a new instance of the WoWData class.
        """
        self.base_url = "https://us.api.blizzard.com/data/wow/"
        self.namespace = "static-us"
        self.locale = "en_US"

    def get_data(self, access_token, url):
        """
        Sends a GET request to the specified URL and returns the JSON response.

        Parameters:
        - access_token: A dictionary representing the access token to use for the request.
        - url: A string representing the URL to send the request to.

        Returns:
        - A dictionary representing the JSON response from the API.
        """
        response = requests.get(url)
        if response.ok:
            print("Success!")
            return response.json()
        else:
            print("Not Found.")
            return None

    def get_spells(self, access_token, document_type="spell", orderby="id"):
        """
        Retrieves a list of spells from the API.

        Parameters:
        - access_token: A dictionary representing the access token to use for the request.
        - document_type: A string representing the type of document to retrieve (default: "spell").
        - orderby: A string representing the field to order the results by (default: "id").

        Returns:
        - A dictionary representing the JSON response from the API.
        """
        url = f"{self.base_url}search/{document_type}?namespace={self.namespace}&orderby={orderby}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_talent_index(self, access_token):
        """
        Retrieves the talent index from the API.

        Parameters:
        - access_token: A dictionary representing the access token to use for the request.

        Returns:
        - A dictionary representing the JSON response from the API.
        """
        url = f"{self.base_url}talent/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)

    def get_pvp_talent_index(self, access_token):
        """Return the PvP talent index for World of Warcraft.

        Parameters:
        - access_token: A dictionary containing the access token
                returned by `create_access_token()`.

        Returns:
        - dict or None: A dictionary containing the PvP talent index data
                or None if the request was unsuccessful.
        """

        url = f"{self.base_url}pvp-talent/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)


    def get_tech_talent_index(self, access_token):
        """Return the tech talent index for World of Warcraft.

        Parameters:
        - access_token: A dictionary containing the access token
                returned by `create_access_token()`.

        Returns:
        - dict or None: A dictionary containing the tech talent index data
                or None if the request was unsuccessful.
        """ 

        url = f"{self.base_url}tech-talent/index?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)


    def get_description(self, access_token, spell_id):
        """Return the description of a specific spell in World of Warcraft.

        Parameters:
        - access_token: A dictionary containing the access token
                returned by `create_access_token()`.
        - spell_id: The ID of the spell to get the description for.

        Returns:
        - dict or None: A dictionary containing the description of the
                specified spell or None if the request was unsuccessful.
        """

        url = f"{self.base_url}spell/{spell_id}?namespace={self.namespace}&locale={self.locale}"
        url += f"&access_token={access_token['access_token']}"
        return self.get_data(access_token, url)


    def create_access_token(self, client_id, client_secret, region="us"):
        """Create an access token for accessing the Blizzard API.

        Parameters:
        - client_id (str): The client ID for your Blizzard API account.
        - client_secret (str): The client secret for your Blizzard API account.
        - region (str): The region to create the access token for. Default is "us".

        Returns:
        - dict: A dictionary containing the access token information, including
                the access token and its type.
        """

        url = f"https://{region}.battle.net/oauth/token"
        body = {"grant_type": "client_credentials"}
        auth = HTTPBasicAuth(client_id, client_secret)

        response = requests.post(url, data=body, auth=auth)
        return response.json()
