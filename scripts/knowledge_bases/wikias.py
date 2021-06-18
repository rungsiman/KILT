import json
import argparse

from kilt.knowledge.wikias import Wikias

DEFAULT_CONFIG = {
    "host": "localhost",
    "db": "kilt",
    "collection": "wikias"
}


def import_to_kilt(base_config, wikias_config):
    config = DEFAULT_CONFIG

    for config_item in (base_config, wikias_config):
        if config_item is not None:
            with open(config_item) as reader:
                config = {**config, **json.load(reader)}
    
    mongo_connection_string = "mongodb://"

    if "username" in config and "password" in config:
        mongo_connection_string += config["username"] + ":" + config["password"] + "@"
    
    mongo_connection_string += config["host"] + "/admin"
    wikias = Wikias(mongo_connection_string, collection=config["collection"])
    wikias.import_to_kilt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base_config",
        dest="base_config",
        type=str,
        help="Path to MongoDB connection configuration file"
    )

    parser.add_argument(
        "--wikias_config",
        dest="wikias_config",
        type=str,
        help="Path to Wikias collection configuration file"
    )

    params = parser.parse_args()
    import_to_kilt(params.base_config, params.wikias_config)
