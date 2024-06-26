from redis import Redis
from echo_harvest.internals.schemas import MetaData
from echo_harvest.helpers.logger import logging as logger
import json


class RedisHandler:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self._key = "recent_track_metadata"

    def get_last_player_metadata(self) -> MetaData:
        """GET the latest played music metadata"""
        metadata = self.redis.get(self._key)
        if metadata:
            metadata = json.loads(metadata)
        logger.debug(f"REDIS::GET:{metadata}")
        return metadata

    def store_track_metadata(self, metadata: MetaData) -> None:
        """SET the current music metadata"""

        if self.get_last_player_metadata():
            self.redis.delete(self._key)

        self.redis.set(self._key, json.dumps(metadata.__dict__, default=str))
        logger.debug(f"REDIS::INSERT:{metadata}")
