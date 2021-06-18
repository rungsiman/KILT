import json
from tqdm import tqdm

from kilt.datasets.base_dataset import Dataset

ENT_START_TOKEN = "[START_ENT]"
ENT_END_TOKEN = "[END_ENT]"


class ZeshelDataset(Dataset):
    def __init__(
        self,
        name,
        input_file,
        output_file
    ):
        super().__init__(name)
        self.input_file = input_file
        self.output_file = output_file

    def get_chunks(self, num_chunks):
        """Returns a single chunk for a zeshel mention file"""
        with open(self.input_file, "r") as reader:
            return [reader.readlines()]

    def process_chunk(self, lines, ks, chunk_id=-1):
        queries = []

        for line in tqdm(lines, desc=f"Processing {self.name}"):
            js = json.loads(line)
            page = ks.get_page_by_id(js["context_document_id"])
            tokens = page["text"].split(' ')

            ent_start_i = js["start_index"]
            ent_end_i = js["end_index"]
            text = " ".join(tokens[:ent_start_i])
            text += f" {ENT_START_TOKEN} " + js["text"] + f" {ENT_END_TOKEN} "
            text += " ".join(tokens[ent_end_i + 1:])

            queries.append({
                "id": js["mention_id"],
                "input": text,
                "output": [
                    {
                        "answer": page["wikias_title"],
                        "provenance": [
                            {
                                "wikias_id": js["label_document_id"],
                                "title": page["wikias_title"],
                            }
                        ]
                    }
                ],
                "meta": {
                    "wikias_id": js["context_document_id"],
                    "category": js["category"]
                }
            })

        return queries, []

    def postprocess_metadata(self, metadata):
        pass


class ZeshelBlinkDataset(Dataset):
    def __init__(
        self,
        name,
        input_file,
        output_file
    ):
        super().__init__(name)
        self.input_file = input_file
        self.output_file = output_file
    
    def get_chunks(self, num_chunks):
        """Returns a single chunk for a zeshel mention file"""
        with open(self.input_file, "r") as reader:
            return [reader.readlines()]

    def process_chunk(self, lines, ks, chunk_id=-1):
        queries = []
        id_map = {}

        for line in tqdm(lines, desc=f"Processing {self.name}"):
            js = json.loads(line)

            text = js["context_left"]
            text += f" {ENT_START_TOKEN} " + js["mention"] + f" {ENT_END_TOKEN} "
            text += js["context_right"]

            queries.append({
                "id": js["mention_id"],
                "input": text,
                "output": [
                    {
                        "answer": js["label_title"],
                        "provenance": [
                            {
                                "wikias_id": js["label_wikias_id"],
                                "title": js["label_title"]
                            }
                        ]
                    }
                ],
                "meta": {
                    "wikias_id": js["context_wikias_id"],
                    "world": js["world"]
                }
            })
        
        return queries, []
    
    def postprocess_metadata(self, metadata):
        pass
