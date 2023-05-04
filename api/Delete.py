from api.api_calls import APICallsClass
from requests import HTTPError


class Delete_Trashed_Pages_And_Blogposts:
    def __init__(self, config, log):
        self.log = log,
        self.url = config['INSTANCE']['source_url']
        self.username = config['INSTANCE']['username']
        self.password = config['INSTANCE']['password']
       # self.spacekey = config['SPACEKEY']['spacekey']

        self.api = APICallsClass(base_url=self.url, username=self.username, password=self.password)

    def delete_trashed_pages_and_blogposts(self, endpoint):
        """
        This function send a DELETE request to delete the pages and blogposts which IDs were collected during GET request
        of all trashed pages and blogposts
        :return:
        """
        try:

            request_call = self.api.delete(endpoint)
            print(f"Sucessfully deleted with statuscode: {request_call.status_code}")
        except HTTPError as err:
            self.log.error(f"Error in function get_list_of_deleted_objects: {err}")
            exit(1)
