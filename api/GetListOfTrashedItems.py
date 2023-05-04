import json

import requests
from urllib3.exceptions import InsecureRequestWarning

from api.api_calls import APICallsClass
from extract_json import json_extract

from requests import HTTPError


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GetListOfTrashedItems:
    def __init__(self, config, log):
        self.log = log
        self.url = config['INSTANCE']['source_url']
        self.username = config['INSTANCE']['username']
        self.password = config['INSTANCE']['password']
        self.api = APICallsClass(base_url=self.url, username=self.username, password=self.password)
    def get_list_of_deleted_objects(self):
        """
        This function sends two GET requests to receive a list of trashed pages in trash AND a list of trashed blogposts
        in trash. Today, there is no possibility to get attachments in trash.
        The response of each GET request is saved in a separate json. After that, the id is extracted and saved in a list.
        Both single lists (one containing ids of all pages, one containing ids of all blogposts) are merged in a single list.

        :return: list of pages and blogposts currently available in the trash by id
        """

        try:
            self.log.info(f"Initialize GET request")
            # send two rest calls to get deleted pages and deleted blogposts. Today, there is no endpoint supporting deletion of attachments
            request_call = self.api.get(endpoint='rest/api/content?spaceKey=MT&status=trashed')
            request_call_blogposts = self.api.get(endpoint='rest/api/content?spaceKey=MT&status=trashed&type=blogpost')
            #request_call_attachments = self.api.get(endpoint='rest/api/content?spaceKey=MT&status=trashed&type=attachment')
            # check if request was successfully by scanning status_code == 200)
            if request_call.status_code & request_call_blogposts.status_code ==200:
                json_data = json.loads(request_call.content)
                json_data_blogposts = json.loads(request_call_blogposts.content)
               # json_data_attachments = json.loads(request_call_attachments.content)
                trashed_pages_by_id = json_extract(json_data, 'id')
                trashed_blogposts_by_id = json_extract(json_data_blogposts, 'id')
              #  trashed_attachments_by_id = json_extract(json_data_attachments, 'id')
                self.log.info(f"{trashed_pages_by_id}")
                self.log.info(f"{trashed_blogposts_by_id}")
                #self.log.info(f"{trashed_attachments_by_id}")
                trashed_pages_and_blogposts = []
                trashed_pages_and_blogposts.extend(trashed_blogposts_by_id)
                trashed_pages_and_blogposts.extend(trashed_pages_by_id)
               # trashed_pages_and_blogposts.extend(trashed_attachments_by_id)
                return trashed_pages_and_blogposts



#TODO make spacekey editable
#TODO make endpoint editable

        except HTTPError as err:
            self.log.error(f"Error in function get_list_of_deleted_objects: {err}")
            exit(1)

