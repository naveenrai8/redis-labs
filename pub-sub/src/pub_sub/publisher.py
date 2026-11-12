import redis
import time

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# p = redis_client.pubsub()
try:
    for i in range(1):
        subscribers = redis_client.publish('topic', f"Publishing message {i}")
        print(f"Published message to subscribers: {subscribers}")
        time.sleep(1)
finally:
    redis_client.close()

print("Finished")