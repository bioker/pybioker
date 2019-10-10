from contextlib import contextmanager
from typing import ContextManager, Callable

import pika
from pika.adapters import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel


def create_connection(host: str, user: str = 'guest', password: str = 'guest') -> BlockingConnection:
    credentials = pika.credentials.PlainCredentials(username=user, password=password)
    return pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))


@contextmanager
def closable_connection(host: str, user: str = 'guest',
                        password: str = 'guest') -> ContextManager[BlockingConnection]:
    connection = create_connection(host, user, password)
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def closable_channel(connection: BlockingConnection) -> ContextManager[BlockingChannel]:
    channel = connection.channel()
    try:
        yield channel
    finally:
        channel.close()


def wrap_with_channel(connection: BlockingConnection, function: Callable[[BlockingChannel], None]) -> BlockingChannel:
    channel = connection.channel()
    function(channel)
    return channel
