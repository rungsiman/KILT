import os

from kilt import dataset_mapper
from kilt.datasets.zeshel import ZeshelBlinkDataset
from kilt.knowledge.wikias import Wikias

HOST = os.environ['KILT_MONGO_HOST']
USER = os.environ['KILT_MONGO_USER']
PASSWORD = os.environ['KILT_MONGO_PASSWORD']

ks = Wikias(f'mongodb://{USER}:{PASSWORD}@{HOST}/admin', collection='wikias')

for stage in ('train', 'val', 'test'):
    zd = ZeshelBlinkDataset.from_config_file(f'zeshel-{stage}', f'kilt/configs/mapping/zeshel_blink_{stage}.json')
    dataset_mapper.map_dataset(dataset=zd, knowledge_source=ks)
