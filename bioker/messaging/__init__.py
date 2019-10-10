from typing import Callable

import pika
from pika import BasicProperties
from pika.adapters import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel


def create_connection(host: str, user: str = 'guest', password: str = 'guest') -> BlockingConnection:
    credentials = pika.credentials.PlainCredentials(username=user, password=password)
    return pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))


def publish(conn: BlockingConnection, queue_name: str, message_body: bytes,
            exchange: str = '', channel: BlockingChannel = None, properties: BasicProperties = None):
    if not channel:
        ch = conn.channel()
    else:
        ch = channel
    ch.basic_publish(exchange, queue_name, message_body, properties=properties)
    if not channel:
        ch.close()


def consume(conn: BlockingConnection, queue_name: str, extract_func: Callable,
            channel: BlockingChannel = None, auto_ack: bool = False):
    message_received = False
    result = None

    def callback(chan: BlockingChannel, method, properties, body):
        try:
            result = extract_func(chan, method, properties, body)
        except Exception:
            pass
        message_received = True

    if not channel:
        ch = conn.channel()
    else:
        ch = channel
    ch.basic_consume(queue_name, callback, auto_ack=auto_ack)
    while not message_received:
        pass
    if not channel:
        ch.close()
    return result
