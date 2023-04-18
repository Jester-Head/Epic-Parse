import requests
from constant import CLIENT_ID, CLIENT_SECRET
from requests.auth import HTTPBasicAuth
import json


class WoW_Data:
    def __init__(self):
        # Initialize base API URL, namespace, and locale
        self.base_url = "https://us.api.blizzard.com/data/wow/"
        self.namespace = "static-us"
        self.locale = "en_US"

    def get_spells(self, access_token, documentType="spell", orderby="id"):
        """
        Get spells data from the Blizzard API.

        :param access_token: Access token to authenticate with Blizzard API.
        :param documentType: Type of document to search for (default is 'spell').
        :param orderby: Order results by a specific field (default is 'id').
        """
        url = f"{self.base_url}search/{documentType}?namespace={self.namespace}&orderby={orderby}&access_token={access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            print('Success!')
            return response.json()
        elif response.status_code == 404:
            print('Not Found.')
            return None

    def get_talent_index(self, access_token):
        """
        Get talent index data from the Blizzard API.

        :param access_token: Access token to authenticate with Blizzard API.
        """
        url = f"{self.base_url}talent/index?namespace={self.namespace}&locale={self.locale}&access_token={access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            print('Success!')
            return response.json()
        elif response.status_code == 404:
            print('Not Found.')
            return None

    def get_pvp_talent_index(self, access_token):
        """
        Get PvP talent index data from the Blizzard API.

        :param access_token: Access token to authenticate with Blizzard API.
        """
        url = f"{self.base_url}pvp-talent/index?namespace={self.namespace}&locale={self.locale}&access_token={access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            print('Success!')
            return response.json()
        elif response.status_code == 404:
            print('Not Found.')
            return None

    def get_tech_talent_index(self, access_token):
        """
        Get tech talent index data from the Blizzard API.

        :param access_token: Access token to authenticate with Blizzard API.
        """
        url = f"{self.base_url}tech-talent/index?namespace={self.namespace}&locale={self.locale}&access_token={access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            print('Success!')
            return response.json()
        elif response.status_code == 404:
            print('Not Found.')
            return None

    def create_access_token(self, client_id, client_secret, region='us'):
        """
        Create an access token for authentication with the Blizzard API.

        :param client_id: Client ID for Blizzard API.
        :param client_secret: Client secret for Blizzard API.
        :param region: Region for Blizzard API (default is 'us').
        """
        url = f"https://{region}.battle.net/oauth/token"
        body = {"grant_type": "client_credentials"}
        auth = HTTPBasicAuth(client_id, client_secret)

        response = requests.post(url, data=body, auth=auth)
        return response.json()

