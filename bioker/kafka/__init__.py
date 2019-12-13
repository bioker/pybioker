import json
from typing import List

from kafka import KafkaConsumer, KafkaProducer


def get_consumer_from_config_string(configs_string: str, topics: List[str],
                                    bootstrap_servers: str = 'kafka:8082') -> KafkaConsumer:
    configs = json.loads(configs_string)
    if bootstrap_servers is not None:
        configs['bootstrap_servers'] = bootstrap_servers
    return KafkaConsumer(*topics, **configs)


def get_producer_from_config_string(configs_string: str, bootstrap_servers: str = 'kafka:8082') -> KafkaProducer:
    configs = json.loads(configs_string)
    if bootstrap_servers is not None:
        configs['bootstrap_servers'] = bootstrap_servers
    return KafkaProducer(**configs)
