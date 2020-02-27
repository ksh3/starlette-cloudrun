from __future__ import annotations

import dataclasses
import logging
import typing
from abc import ABCMeta
from datetime import datetime

import databases
import pytz

from . import config

database = databases.Database(config.DATABASE_URL)

logger = logging.getLogger(__name__)
if config.DEBUG:
    logger.setLevel(logging.DEBUG)


class ModelInterface(metaclass=ABCMeta):

    @classmethod
    async def execute(cls, args) -> typing.Optional[typing.Mapping]:
        return await database.fetch_one(**args)

    @classmethod
    async def create(cls):
        return await NotImplementedError

    @classmethod
    async def update(cls):
        return await NotImplementedError

    @classmethod
    async def delete(cls):
        return await NotImplementedError


@dataclasses.dataclass
class Robot(ModelInterface):
    id: int
    name: str
    created_at: datetime = datetime.utcnow().replace(tzinfo=pytz.utc)

    @classmethod
    async def retrieve(cls: Robot, values: {'robot_id': int}) -> Robot:
        res = await super().execute({
            'query': """
                SELECT * from
                robots
                WHERE id = :robot_id
            """,
            'values': values
        })
        return cls(**res)
