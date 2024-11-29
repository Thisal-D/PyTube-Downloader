from urllib import request
import requests
from typing import List, Dict
from .json_utility import JsonUtility


class DataRetriveUtility:
    CONTRIBUTORS_TEXT_URL = "https://raw.githubusercontent.com/Thisal-D/PyTube-Downloader/main/contributors.txt"
    VERSION_FILE_URL = "https://raw.githubusercontent.com/Thisal-D/PyTube-Downloader/main/VERSION"

    @staticmethod
    def get_contributors_data() -> List[Dict]:
        """
        Retrieve contributors data from a GitHub repository.

        Returns:
            list: A list of dictionaries containing contributor information.
        """
        contributors = []
        try:
            data = requests.get(DataRetriveUtility.CONTRIBUTORS_TEXT_URL).text
            for contributor_data in data.split("\n"):
                try:
                    profile_url, username = contributor_data.split("@%@")
                    contributors.append({
                        "profile_url": profile_url,
                        "user_name": username,
                    })
                except Exception as error:
                    print(f"data_retrive_utility.py L54 : {error}")
        except Exception as error:
            print(f"data_retrive_utility.py L43 : {error}")
            return None
        
        return contributors
    
    @staticmethod
    def get_latest_version():
        """
        Retrieve latest version from a GitHub repository.

        Returns:
            string: The latest version number.
        """
        try:
            data = requests.get(DataRetriveUtility.VERSION_FILE_URL).text.strip()
            # Extract the version number from the string "VERSION = '2.0.2'"
            # Split at "=" and remove extra characters like spaces and quotes
            version = data.split('=')[1].strip().strip("'")
        
        except Exception as error:
            print(f"data_retrive_utility.py L43 : {error}")
            return None
        
        return version
    
    def get_current_version():
        """
        Read current version from info.json file.
        
        return:
            string: current version
        """
        version = JsonUtility.read_from_file("data\\info.json")["version"]
        return version
    
    