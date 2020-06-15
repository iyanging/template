from typing import Optional

import aioredis

ENCODING = 'utf-8'


class Redis:
    def __init__(self, address: str):
        self.address: str = address
        self.is_connected: bool = False
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        assert not self.is_connected, "Already connected."

        redis = await aioredis.create_redis_pool(self.address)
        self.redis = redis
        self.is_connected = True

    async def disconnect(self):
        assert self.is_connected, "Already disconnected."

        self.redis.close()
        await self.redis.wait_closed()
        self.is_connected = False
        self.redis = None

    async def execute(self, command, *args, **kwargs):
        return await self.redis.execute(command, *args, **kwargs, encoding=ENCODING)
