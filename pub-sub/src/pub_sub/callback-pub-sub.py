import time

import redis
import threading

from pub_sub.example import run_subscriber

def run_publisher(redis_client, channel: str, count: int=10):
    pub = redis_client.pubsub(ignore_subscribe_messages=True)
    for i in range(count):
        subscribers = redis_client.publish(channel, f"Publishing message {i}")
        print(subscribers)
        time.sleep(0.001)

def subscriber_callback(message):
        data = message["data"]
        channel = message["channel"]
        print(f"  [Callback] Received on '{channel}': {data}")

def main():
    channel = "call-back-channel"
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    sub = redis_client.pubsub()
    sub.subscribe(**{"call-back-channel":subscriber_callback})
    sub_worker = sub.run_in_thread(sleep_time=0.1)
    run_publisher(redis_client, channel)

    sub_worker.stop()
    sub_worker.join()

    print("main done")


if __name__ == "__main__":
    main()
