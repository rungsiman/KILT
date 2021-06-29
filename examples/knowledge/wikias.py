import os

from kilt.knowledge.wikias import Wikias

HOST = os.environ['KILT_MONGO_HOST']
USER = os.environ['KILT_MONGO_USER']
PASSWORD = os.environ['KILT_MONGO_PASSWORD']

wk = Wikias(f'mongodb://{USER}:{PASSWORD}@{HOST}/admin', collection='wikias')
wk.import_to_kilt()
