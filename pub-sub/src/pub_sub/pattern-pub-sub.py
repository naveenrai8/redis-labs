import time

import redis
import threading

from pub_sub.example import run_subscriber

def run_publisher(redis_client, channel: str, count: int=10):
    pub = redis_client.pubsub(ignore_subscribe_messages=True)
    for i in range(count):
        for ch in ["alert.info", "alert.warning", "alert.warning"]:
            subscribers = redis_client.publish(ch, f"Publishing message {i} to channel {ch}")
            print(f"====== subscribers {subscribers} of channel {ch} ======")
            print("\n\n")
            time.sleep(0.001)


def main():
    channel = "alert.*"
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    pub_thread = threading.Thread(target=run_publisher, args=(redis_client, channel))
    sub_1 = redis_client.pubsub()
    sub_1.psubscribe("alert.info")
    sub_2 = redis_client.pubsub()
    sub_2.psubscribe("alert.*")
    sub_1_thread = threading.Thread(target=run_subscriber, args=(sub_1, "Thread alert.info Channel"))
    sub_1_thread.start()

    sub_2_thread = threading.Thread(target=run_subscriber, args=(sub_2, "Thread alert.* Channel"))
    sub_2_thread.start()


    pub_thread.start()

    sub_1_thread.join()
    sub_2_thread.join()
    pub_thread.join()

    print("main done")


if __name__ == "__main__":
    main()
