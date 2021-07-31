import json
import os
from tqdm import tqdm

from kilt.knowledge.base import KnowledgeBase


class Wikias(KnowledgeBase):
    page_id_attr = 'wikias_id'
    page_title_attr = 'wikias_title'
    page_description_attr = 'text'

    def __init__(
        self,
        mongo_connection_string=None,
        database="kilt",
        collection="wikias",
    ):
        super().__init__(mongo_connection_string, database, collection)

    def import_to_kilt(self, input_folder='original_data/zeshel/documents'):
        if self.get_num_pages():
            print('Documents already exist in the database.')
            return

        for file in tqdm(next(os.walk(input_folder))[2], desc='Importing zeshel'):
            with open(os.path.join(input_folder, file)) as reader:
                docs = []

                for line in reader.readlines():
                    page = json.loads(line)
                    docs.append({
                        '_id': page['document_id'],
                        self.page_id_attr: page['document_id'],
                        self.page_title_attr: page['title'],
                        'text': page['text'],
                        'domain': file.replace('.json', '')
                    })
                
                self.collection.insert_many(docs)
        
        print(f'Imported {self.get_num_pages()} documents.')
