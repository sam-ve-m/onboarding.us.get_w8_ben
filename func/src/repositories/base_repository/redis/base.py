# STANDARD LIBS
import pickle
from typing import Union

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import InternalServerError
from func.src.infrastructure.redis.infrastructure import RedisInfrastructure


class BaseRepositoryRedis(RedisInfrastructure):
    prefix = ""

    @classmethod
    async def get(cls, key: str) -> Union[dict, str, bytes]:
        redis = cls.get_redis()
        if type(key) != str:
            raise InternalServerError("Redis.Cache.Keys::get::Error on getting redis keys")
        key = f"{cls.prefix}{key}"
        value = await redis.get(name=key)
        return value and pickle.loads(value) or value
