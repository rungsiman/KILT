import os

from kilt.knowledge_source import KnowledgeSource

HOST = os.environ['KILT_MONGO_HOST']
USER = os.environ['KILT_MONGO_USER']
PASSWORD = os.environ['KILT_MONGO_PASSWORD']

ks = KnowledgeSource(f'mongodb://{USER}:{PASSWORD}@{HOST}/admin', collection='wikipedia')
print(ks.get_num_pages())
print(ks.get_page_by_id(27097632))
print(ks.get_page_by_title("Michael Jordan"))
