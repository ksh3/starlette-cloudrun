import logging
import time

from . import store

logger = logging.getLogger(__name__)


async def repair_robot(robot: store.Robot) -> None:
    # FIX ROBOT.
    time.sleep(4)
    logger.debug("TASK HAS DONE")
