import time

import redis
import os

CHANNEL = os.getenv("REDIS_CHANNEL", "topic")
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

print("Starting subscriber...")
subscribers = redis_client.pubsub()
subscribers.subscribe('topic')

print(f"Subscribed to {CHANNEL!r}, waiting for messages...")
try:
    for message in subscribers.listen():
        print(f"[{message['channel']}] {message['data']}")
except KeyboardInterrupt:
    pass
finally:
    subscribers.close()
    redis_client.close()

