import json
from collections import Callable
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from kafka import KafkaConsumer
from kafka import KafkaProducer


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


def get_consumer_future(executor: ThreadPoolExecutor, topics: List[str], config: dict, poll_params: dict,
                        records_handler: Callable, worker_id: str = None, poll_times: int = -1):
    consumer = KafkaConsumer(*topics, **config)
    _worker_id = worker_id or uuid4()
    return executor.submit(_consume, worker_id, consumer, poll_params, records_handler, poll_times)


def _consume(worker_id: str, consumer: KafkaConsumer, poll_params: dict, records_handler: Callable, times: int = -1):
    if times < 0:
        while True:
            records_handler(worker_id, consumer.poll(**poll_params))
    else:
        i = 0
        while i < times:
            records_handler(worker_id, consumer.poll(**poll_params))
            i += 1
