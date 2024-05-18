import json


class JsonUtility:
    """
    A utility class for handling JSON data.
    """

    @staticmethod
    def read_from_file(file_path: str) -> dict:
        """
        Read JSON data from a file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The JSON data read from the file.
        """
        with open(file_path, "r", encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        return json_data

    @staticmethod
    def write_to_file(file_path: str, data: dict) -> None:
        """
        Write JSON data to a file.

        Args:
            file_path (str): The path to the JSON file.
            data (dict): The JSON data to be written.
        """
        with open(file_path, "w", encoding='utf-8') as json_file:
            try:
                json.dump(obj=data, fp=json_file, indent=4, sort_keys=True)
            except Exception as error:
                print(f"json_utility.py L-37 : {error}")
                json.dump(obj=data, fp=json_file, indent=4, sort_keys=False)
                

    @staticmethod
    def convert_lists_to_tuples(data: dict) -> dict:
        """
        Convert lists in a dictionary to tuples recursively.

        Args:
            data (dict): The dictionary containing JSON-like data.

        Returns:
            dict: The dictionary with lists converted to tuples.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        for sub_sub_key, sub_sub_value in sub_value.items():
                            if isinstance(sub_sub_value, list):
                                data[key][sub_key][sub_sub_key] = tuple(sub_sub_value)
                    elif isinstance(sub_value, list):
                        data[key][sub_key] = tuple(sub_value)
            elif isinstance(value, list):
                data[key] = tuple(value)
        return data
