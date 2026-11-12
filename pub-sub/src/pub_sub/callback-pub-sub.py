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


def main():
    channel = "channel"
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    pub_thread = threading.Thread(target=run_publisher, args=(redis_client, channel))
    sub = redis_client.pubsub()
    sub.subscribe(channel)
    sub_thread = threading.Thread(target=run_subscriber, args=(sub, "Thread Channel"))
    sub_thread.start()
    pub_thread.start()
    sub_thread.join()
    pub_thread.join()

    print("main done")


if __name__ == "__main__":
    main()
