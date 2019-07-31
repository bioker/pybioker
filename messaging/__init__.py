import pika

def pika_conn(host, user='guest', password='guest'):
    """Creates pika BlockingConnection with passed parameters

    :param host - amqp server hostname
    :param user - username (default 'guest')
    :param password - password (default 'guest')

    :type host: str
    :type user: str
    :type password: str

    :rtype: pika.BlockingConnection
    """
    credentials = pika.credentials.PlainCredentials(
            username=user,
            password=password)
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        credentials=credentials))


def publish(conn, queue_name, message_body, 
            channel=None,
            properties=None):
    """Publish single message to queue

    :param conn - pika connection
    :param queue_name - queue name to publish
    :param message_body - message body

    :type conn: pika.adapters.BlockingConnection
    :type queue_name: str
    :type message_body: str
    :type channel: pika.adapters.blocking_connection.BlockingChannel
    """
    ch = None
    if not channel:
        ch = conn.channel()
    else:
        ch = channel
    ch.basic_publish('', queue_name, message_body, properties=properties)
    if not channel:
        ch.close()

def consume(conn, queue_name, extract_func, channel=None, no_ack=False):
    """Consumes single message from queue

    :param conn - pika connection
    :param queue_name - queue name to publish
    :param extract_func - function to extract result
    :param channel - channel to use for consuming (optional)

    :type conn: pika.adapters.BlockingConnection
    :type queue_name: str
    :type extract_func: function
    :type channel: pika.adapters.blocking_connection.BlockingChannel
    """
    message_received = False
    result = None
    def callback(channel, method, properties, body):
        try:
            result = extract_func(channel, method, properties, body)
        except Exception:
            pass
        message_received = True
    ch = None
    if not channel:
        ch = conn.channel()
    else:
        ch = channel
    ch.basic_consume(callback, queue_name, no_ack=no_ack)
    while not message_received:
        pass
    if not channel:
        ch.close()
    return result 
