
"""Jira API binding for Python 3.x

Learn more:

https://docs.atlassian.com/software/jira/docs/api/REST/9.16.0/

Copyright Atlassian developer. See license.md for details.
"""
import requests

from requests.auth import HTTPBasicAuth


class JiraAPIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url

    def get_search(self, query):
        """Issue a GET request (read) against the API.

        Args:
            filter{id}: The API method to call including parameters,
            e.g. GET /rest/api/2/filter/{id}.

        Returns:
            JSON representation of the search results.
        """
        return self.__send_request('GET', query)

    def __send_request(self, method, query):
        url = self.__url + '?' + query
        # Store all results
        all_results = []
        params = {}

        headers = {"Content-Type": "application/json"}

        # Pagination variables
        max_results = 100
        total = None
        params['startAt'] = 0

        while True:
            # Send GET request
            response = requests.get(
                        url,
                        headers=headers,
                        auth=HTTPBasicAuth(self.user, self.password),
                        params=params)

            data = response.json()

            all_results.extend(data['issues'])
            if total is None:
                total = data['total']

            # Increment the startAt parameter
            params['startAt'] += max_results

            # Check if we've retrieved all results
            if params['startAt'] >= total:
                break

        # Print the total number of issues retrieved
        print(f"Total issues retrieved: {len(all_results)}")
        return all_results
