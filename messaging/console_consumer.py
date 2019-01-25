import threading

def _create_callback(show_method=False, show_properties=False, show_body=True):
    def callback(channel, method, properties, body):
        if show_method:
            print("method: {}".format(method))
        if show_properties:
            print("properties: {}".format(properties))
        if show_body:
            print("body: {}".format(body))
    return callback

class ConsoleConsumer(threading.Thread):
    """Consumer representation with state
    to be able interact with it (start, stop)
    """

    def __init__(self, conn, queue_name):
        """Creates console consumer instance with references to connection
        for channels creating
        :param conn - pika connection
        :param queue_name - queue name to consume from

        :type conn: pika.adapters.BlockingConnection
        :type queue_name: str
        """
        super(ConsoleConsumer, self).__init__()
        self.conn = conn
        self.queue_name = queue_name
        self.current_channel = None

    def run(self):
        self.current_channel.start_consuming()

    def start(self,
            show_method=False,
            show_properties=False,
            show_body=True,
            no_ack=True,
            shutdown_current=False):
        """Configure current channel consuming
        :param show_method - does it need to show a method
        :param show_properties - does it need to show properties
        :param show_body - does it need to show a body
        :param no_ack - whether to send an acknowledgement back
        :param shutdown_current - whether to shutdown current channel

        :type show_method: bool
        :type show_properties: bool
        :type show_body: bool
        :type no_ack: bool
        """
        if self.current_channel is not None:
            if shutdown_current:
                self.current_channel.close()
            else:
                raise RuntimeError("consumer in process of consuming"
                        "and shutdown_current flag is disabled")
        self.current_channel = self.conn.channel()
        callback = _create_callback(
                show_method=show_method,
                show_properties=show_properties,
                show_body=show_body)
        self.current_channel.basic_consume(callback,
                self.queue_name, no_ack=no_ack)
        super(ConsoleConsumer, self).start()

    def stop(self):
        """Stops and reset current channel
        """
        self.current_channel.close()
        self.current_channel = None
