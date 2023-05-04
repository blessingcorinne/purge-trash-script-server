import logging
import os.path
import yaml
import sys
from datetime import datetime
import requests
from api.Delete import Delete_Trashed_Pages_And_Blogposts
from api.api_calls import APICallsClass


from api.GetListOfTrashedItems import GetListOfTrashedItems

def __init__(self, config, log):
    self.log = log,
    self.url = config['INSTANCE']['source_url']
    self.username = config['INSTANCE']['username']
    self.password = config['INSTANCE']['password']

    self.api = APICallsClass(base_url=self.url, username=self.username, password=self.password)



dirpath = os.path.dirname(__file__)
config_filepath = os.path.join(dirpath, 'config/config.yml')

if not os.path.exists("logs"):
    os.makedirs("logs")


logging.basicConfig(
    filename='logs/Log_List_Of_Trashed_Objects',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    filemode='a',
    level=logging.DEBUG
)

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))


def check_if_file_exists(file_name):
    """
    Helper function to check if a file exist
    :param file_name: insert file
    :return: Boolean
    """
    if not os.path.exists(file_name):
        return False
    return True


def load_yaml(filepath):
    """
    Helper function for loading a yaml file
    :param filepath: insert file
    :return: loaded data from the yaml file
    """
    if check_if_file_exists(file_name=filepath):
        with open(filepath, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            log.info(f"data loaded")
        return data_loaded
    log.info(f"No Config-file found. Terminate Script")
    exit()
    return None

if __name__ == '__main__':
    start_time = datetime.now()
    list_of_trashed_objects_by_id=[]
    config= load_yaml(filepath=config_filepath)
    log.info(f"Start GET request to fetch list of trashed items in trash")
    list_of_trashed_objects_by_id = GetListOfTrashedItems(config=config, log=log).get_list_of_deleted_objects()
    log.info(f"list of trashed pages and blogposts: {list_of_trashed_objects_by_id}")
    for i in range(len(list_of_trashed_objects_by_id)):
        id = list_of_trashed_objects_by_id[i]
        final_endpoint = 'rest/api/content/' + id + '?status=trashed'
        delete_pages = Delete_Trashed_Pages_And_Blogposts(config, log)
        r = delete_pages.delete_trashed_pages_and_blogposts(final_endpoint)

        log.info(f"deleted page with id: {id}")
        list_of_trashed_objects_by_id = GetListOfTrashedItems(config=config, log=log).get_list_of_deleted_objects()


    log.info(f"list of trashed pages and blogposts after calling delete_trashed_pages_and_blogposts: {list_of_trashed_objects_by_id}")









