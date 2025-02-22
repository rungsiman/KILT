from pymongo import MongoClient

DEFAULT_MONGO_CONNECTION_STRING = "mongodb://127.0.0.1:27017/admin"


class KnowledgeBase:
    def __init__(
        self,
        mongo_connection_string: str,
        database: str,
        collection: str,
        page_id_attr: str,
        page_title_attr: str,
        page_description_attr: str
    ):
        if mongo_connection_string is None:
            mongo_connection_string = DEFAULT_MONGO_CONNECTION_STRING

        self.client = MongoClient(mongo_connection_string)
        self.db = self.client[database]
        self.collection = self.db[collection]

        self.page_id_attr = page_id_attr
        self.page_title_attr = page_title_attr
        self.page_description_attr = page_description_attr

    def get_all_pages_cursor(self):
        cursor = self.collection.find({})
        return cursor
    
    def get_num_pages(self):
        return self.collection.count()
    
    def get_page_by_id(self, page_id):
        page = self.collection.find_one({"_id": str(page_id)})
        return page
    
    def get_page_by_title(self, page_title, attempt=0):
        page = self.collection.find_one({self.page_title_attr: str(page_title)})
        return page

    def get_page_from_url(self, url):
        ...

    @staticmethod
    def build_connection_string(host, username=None, password=None):
        if username is not None and password is not None:
            return f'mongodb://{username}:{password}@{host}/admin'
        else:
            return f'mongodb://{host}/admin'
