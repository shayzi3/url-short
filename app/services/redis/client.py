from redis.asyncio import Redis



class RedisPool(Redis):
     def __init__(self) -> None:
          super().__init__()