"""
py_github_cli github_api module.
"""
import os

import requests
from columnar import columnar
from requests.auth import HTTPBasicAuth


class repository:
    """The class is to be used for all github API methods that act on a
    repository, for example the API endpoints
    OWNER/REPO/releases
    OWNER/REPO/prs
    This class should be extended to support other GET API endpoints and other
    verbs.
    GET API methods:
    get_releases
    get_prs

    Raises:
        ConnectionError: Raises and displays an error when the connection to
        github could not be established
    """

    PREFIX = "https://api.github.com/repos/"

    def __init__(self, repo):
        """The class constructor saves important data

        Args:
            repo (str): The sanitized input repository in the format OWNER/REPO
        """
        self.repo = repo
        self.token = os.environ.get("TOKEN")
        self.user = os.environ.get("USER")

    def get_releases(self):
        """Main method the the command py_github_api releases <repo>
        Prints the top 3 releases when available

        Returns:
            list: A list containing the 3 records
        """
        headers = ["name", "tag name"]
        lines = []
        json_response = self._http_get_request("releases")
        if json_response and len(json_response) > 0:
            print("Listing top 3 releases")
            for r in json_response:
                lines.append([r["name"], r["tag_name"]])
            table = columnar(lines, headers, no_borders=True)
            print(table)
        elif json_response is not None:
            print("No release yet")
        return lines

    def get_prs(self):
        """Main method the the command py_github_api prs <repo>
        Prints the top 3 PRs when available

        Returns:
            list: A list containing the 3 records
        """
        headers = ["number", "title"]
        lines = []
        json_response = self._http_get_request("pulls")
        if json_response and len(json_response) > 0:
            print("Listing top 3 PRs")
            for r in json_response:
                lines.append([r["number"], r["title"]])
            table = columnar(lines, headers, no_borders=True)
            print(table)
        elif json_response is not None:
            print("No prs yet")
        return lines

    def _http_get_request(self, query):
        """A utility method to query the github API with a HTTP GET request
        This method is generic enough to query any API endpoint
        It displays the minimal information from the response such as the
        status_code and the URL that was queried.

        Args:
            query (str): the API to query with a HTTP GET request, for example
            'releases'

        Raises:
            ConnectionError: Raises and displays an error when the connection
            to github could not be established

        Returns:
            json: The HTTP body response in json format or None
        """
        try:
            uri = self.PREFIX + self.repo + "/" + query
            response = requests.get(
                uri,
                params={"per_page": "3"},
                headers={"Accept": "application/vnd.github+json"},
                auth=HTTPBasicAuth(self.user, self.token),
            )
            print("Received response:", response.status_code, response.url)
            if response.status_code == 200:
                json_response = response.json()
                return json_response
            elif response.status_code == 404:
                print(
                    "Received a 404 error, which means either the repo does",
                    "not exist, or it is a private repo. In order to query",
                    "private repos, please set the ENV var USER and TOKEN",
                    "with a personal access token. See README.md for details.",
                )
            else:
                print("Invalid response received from github")
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as ex:
            raise ConnectionError(ex)
