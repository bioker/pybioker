from concurrent.futures.thread import ThreadPoolExecutor

from bioker.kafka import get_consumer_future

consumer_config = {'bootstrap_servers': 'kafka1:29092,kafka2:29092,kafka3:29092', 'group_id': 'test-consumer'}
poll_params = {'timeout_ms': 1000}


def records_handler(worker_id, records):
    print(worker_id, records)


with ThreadPoolExecutor() as executor:
    futures = [get_consumer_future(executor, ['test'], consumer_config, poll_params,
                                   records_handler, str(worker_id), poll_times=3)
               for worker_id in range(3)]
    [future.result() for future in futures]
