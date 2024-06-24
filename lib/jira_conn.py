
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

        headers = {"Content-Type": "application/json"}

        # Pagination variables
        start_at = 0
        max_results = 100
        total = 1  # Initial value greater than start_at to enter the loop

        while start_at < total:
            # Send GET request
            response = requests.get(url, \
                headers=headers, \
                auth=HTTPBasicAuth(self.user, self.password))

            if response.status_code == 200:
                data = response.json()
                all_results.extend(data['issues'])
                total = data['total']  # Update total based on the response
                start_at += max_results  # Move to the next page
            else:
                print(f"Failed to fetch data: {response.status_code}")
                print(response.text)
                break

        # Print the total number of issues retrieved
        print(f"Total issues retrieved: {len(all_results)}")
        return data
