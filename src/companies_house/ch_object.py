"""Object used to collect data from Companies House API."""
import os
import requests
import json
import datetime
import time


class CompaniesHouseService:
    """
    A wrapper around the companies house API.

    Attributes:
        search_url (str): Base url for Companies House search query.
        company_url (str): Base url for Companies House company query.

    """

    search_url = "https://api.companieshouse.gov.uk/search/companies?q="
    company_url = "https://api.companieshouse.gov.uk/company/"
    people_url = "https://api.companieshouse.gov.uk/search/officers?q="
    document_url = "https://document-api.company-information.service.gov.uk/document/"

    def __init__(
        self,
        ch_number: str,
        key: str = 'wSuDcPn_U0376euJz2zJmrZoYePPLXCjvM2OMuAJ',
        time_between_requests: float = 0.5,
    ) -> None:
        """
        Args:
            ch_number (str): Companies house number for the company
            key (str): The API key issued in the Companies House API
                applications.
            time_between_requests (float): Time in seconds between requests to
                the API to prevent spam. Default is 0.5 to prevent calls
                exceeding the 600 per 5 minutes limit.

        """
        self.ch_number = ch_number
        self.key = key
        self.time_between_requests = time_between_requests

        #: datetime: Timestamp instantiated as NoneType
        self.last_request_timestamp = None

    def query_ch_api(
        self,
        url: str,
        explanation: str,
        parameters: dict = None,
        extract=True,
        retries=0,
        max_retries=0,
    ) -> dict:
        """Sends a request to the Companies House API.

        Args:
            url (str): The specific url to be queried depending on the type
                of request (search, profile etc.).
            explanation (str): The type of request being made

            parameters (str): The query parameter to be sent alongside the url.

        Returns:
            dict: A structured dictionary containing all of the information
                returned by the API.

        """
        self._rate_limiting()

        resultQuery = requests.get(url, params=parameters, auth=(self.key, ""))
        if resultQuery.status_code == 200:
            if extract:
                try:
                    return json.JSONDecoder().decode(resultQuery.text)
                except Exception as e:
                    print(f"Extraction of {explanation} failed. Exception: {e}")
                    return resultQuery.text

        elif resultQuery.status_code != 404 and retries < max_retries:
            return self.query_ch_api(
                url, explanation, parameters, extract, retries + 1, max_retries
            )
        else:
            print(
                f"{explanation} failed with error code: {resultQuery.status_code} | "
                f"Reason: {resultQuery.reason}"
            )
            return ""
        return resultQuery.text

    def query_ch_document_api(
        self,
        url: str,
        explanation: str,
        parameters: dict = None,
        extract=True,
        retries=0,
        max_retries=0,
    ) -> dict:
        """Sends a request to the Companies House API.

        Args:
            url (str): The specific url to be queried depending on the type
                of request (search, profile etc.).
            explanation (str): The type of request being made

            parameters (str): The query parameter to be sent alongside the url.

        Returns:
            dict: A structured dictionary containing all of the information
                returned by the API.

        """
        self._rate_limiting()

        resultQuery = requests.get(url, params=parameters, auth=(self.key, ""), stream=True)
        if resultQuery.status_code == 200:
            if extract:
                try:
                    return json.JSONDecoder().decode(resultQuery.content)
                except Exception as e:
                    print(f"Extraction of {explanation} failed. Exception: {e}")
                    return resultQuery.content

        elif resultQuery.status_code != 404 and retries < max_retries:
            return self.query_ch_api(
                url, explanation, parameters, extract, retries + 1, max_retries
            )
        else:
            print(
                f"{explanation} failed with error code: {resultQuery.status_code} | "
                f"Reason: {resultQuery.reason}"
            )
            return b''
        return resultQuery.content

    def _rate_limiting(self):
        """Waits up to the defined time between requests.

        If more than the defined "time_between_requests" has passed (in
        seconds) since the last call, this function will not wait any time.
        The last_request_timestamp class variable is reset to the current
        time every time this method is called.

        """
        if self.last_request_timestamp is None:
            self.last_request_timestamp = datetime.datetime.now()

        else:
            current_time = datetime.datetime.now()

            time_since_request = (
                current_time - self.last_request_timestamp
            ).total_seconds()

            wait_time = max(self.time_between_requests - time_since_request, 0)

            time.sleep(wait_time)
            self.last_request_timestamp = datetime.datetime.now()
