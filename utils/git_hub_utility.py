from urllib import request


class GitHubUtility:
    CONTRIBUTORS_FIND_STRING = '"CONTRIBUTORS INFO",'
    CONTRIBUTORS_TEXT_URL = "https://github.com/Thisal-D/PyTube-Downloader/blob/main/contributors.txt"
    
    @staticmethod
    def get_contributors_data():
        """
        Retrieve contributors data from a GitHub repository.

        Returns:
            list: A list of dictionaries containing contributor information.
        """
        contributors = []
        try:
            data = request.urlopen(GitHubUtility.CONTRIBUTORS_TEXT_URL).read().decode()

            start_index = data.find(GitHubUtility.CONTRIBUTORS_FIND_STRING)
            end_index = data.find("]", start_index)

            contributors_urls_usernames = (
                data[start_index + len(GitHubUtility.CONTRIBUTORS_FIND_STRING): end_index].replace('"', "").split(",")
            )

            for contributor_url_username in contributors_urls_usernames:
                profile_url, username = contributor_url_username.split("@%@")
                contributors.append({
                    "profile_url": profile_url,
                    "user_name": username,
                })

        except Exception as error:
            print(f"git_hub_utility.py L35 : {error}")
            return None

        return contributors
