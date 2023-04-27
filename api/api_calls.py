import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class APICallsClass:
    """
    Helper Functions for the classic HTTP - REST Calls
    HEAD, GET, PUT, POST, OPTIONS, TRACE, DELETE
    """

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.method_whitelist = ["HEAD", "GET", "PUT", "POST", "OPTIONS", "TRACE", "DELETE"]

    def get(self, endpoint, params=None):
        """
        api function to build GET Request
        :param endpoint: this will be added to the base_url
        :param params:
        :return: fully build GET Call
        """
        if params is None:
            params = {}
        # Create a session
        session = requests.Session()
        retries = Retry(total=10, backoff_factor=5, status_forcelist=[502, 503, 504],
                        method_whitelist=self.method_whitelist)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session.get(self.base_url + endpoint, auth=(self.username, self.password), verify=False, timeout=600,
                           params=params)

    def post(self, endpoint, data, params=None, headers=None):
        """
        Api function to build POST Request
        :param endpoint: url which will be added to base_url
        :param data: the data which should be post
        :param params:
        :param headers:
        :return: Fully build POST Call
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        session = requests.Session()
        retries = Retry(total=10, backoff_factor=5, status_forcelist=[502, 503, 504],
                        method_whitelist=self.method_whitelist)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session.post(self.base_url + endpoint, json=data, auth=(self.username, self.password),
                            verify=False, timeout=600, params=params, headers=headers)

    def post_file(self, endpoint, files, headers=None):
        """
        Api function to build POST Request to post files
        :param endpoint: url which will be added to base_url
        :param files: the file, which should be posted
        :param headers:
        :return: Fully build POST Call to post files
        """
        if headers is None:
            headers = {}
        session = requests.Session()
        retries = Retry(total=10, backoff_factor=5, status_forcelist=[502, 503, 504],
                        method_whitelist=self.method_whitelist)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session.post(self.base_url + endpoint, files=files, auth=(self.username, self.password),
                            verify=False, timeout=600, headers=headers)

    def put(self, endpoint, data, params=None):
        """
        PUT is used to send data to a server to create/update a resource
        calling the same PUT request multiple times will always produce the same result (Idempotent)
        :param endpoint: url which will be added to base_url
        :param data: the data which should be post
        :param params:
        :return: Fully build PUT Call
        """
        if params is None:
            params = {}
        session = requests.Session()
        retries = Retry(total=10, backoff_factor=5, status_forcelist=[502, 503, 504],
                        method_whitelist=self.method_whitelist)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session.put(self.base_url + endpoint, json=data, auth=(self.username, self.password),
                           verify=False, timeout=600, params=params)

    def get_attachment(self, url):
        """
        api function to build GET Request for receiving files
        :param url: the url there the file is located
        :return: fully build GET Call
        """
        session = requests.Session()
        retries = Retry(total=10, backoff_factor=5, status_forcelist=[502, 503, 504],
                        method_whitelist=self.method_whitelist)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session.get(url, auth=(self.username, self.password), verify=False, timeout=600)

    def delete(self, url):
        """
        api function to build DELETE Request for a specific endpoint.
        :param endpoint: the url which contains the trashed item to be deleted
        :param headers:
        :return: deletion of trash for every item meeting the criteria
        """


        session = requests.Session()
        retries = Retry(total=10, backoff_factor=5, status_forcelist=[502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session.delete( self.base_url + url, auth=(self.username, self.password),
                              verify=False, timeout=600)