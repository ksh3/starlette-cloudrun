import logging
import time
import asyncio

from . import store

logger = logging.getLogger(__name__)


async def repair_robot(robot: store.Robot) -> None:
    # FIX ROBOT.
    pass


async def count_ref(robot: store.Robot) -> None:
    # FIX ROBOT.
    await asyncio.sleep(12)
    await robot.count_ref()
