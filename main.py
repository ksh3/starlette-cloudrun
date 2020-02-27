import logging

import uvicorn
from starlette import status
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette_prometheus import PrometheusMiddleware, metrics
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src import config, store, task

logger = logging.getLogger(__name__)

app = Starlette()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

if config.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    LOCAL_NETWORKS = ['127.0.0.1:5000', 'localhost:5000']
    app.add_middleware(ProxyHeadersMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=LOCAL_NETWORKS)
    app.add_middleware(CORSMiddleware, allow_origins=LOCAL_NETWORKS)


@app.exception_handler(status.HTTP_403_FORBIDDEN)
@app.exception_handler(status.HTTP_404_NOT_FOUND)
@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def server_error(request, exc) -> str:
    return PlainTextResponse(f"{exc.status_code} ERROR")


@app.on_event('startup')
async def init_server() -> None:
    logger.debug("Connecting PostgreSQL")
    await store.database.connect()


@app.on_event('shutdown')
async def some_shutdown_task() -> None:
    logger.debug("Disconnecting PostgreSQL")
    await store.database.disconnect()


@app.route('/v1/robots/repair', methods=['POST'])
async def repair(request: Request) -> str:
    form = await request.form()
    values = {'robot_id': int(form['robot_id'])}
    robot = await store.Robot.retrieve(values)
    logger.debug(robot)

    task = BackgroundTask(task_repair, robot)
    message = {'message': f'Start repairing {robot.name}.'}
    return JSONResponse(message, background=task)


async def task_repair(robot: store.Robot) -> None:
    task.repair_robot(robot)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=config.DEBUG,
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5000,
        # proxy_headers=True,
        # workers=config.CPU_CORE
    )
