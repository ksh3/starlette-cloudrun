import pytest
from starlette.testclient import TestClient

from main import app
from src import store


class TestView:

    def test_repair(self):
        with TestClient(app) as client:
            response = client.post(
                "/v1/robots/repair", data={"robot_id": 1}
            )
            assert response.status_code == 200


class TestModel:

    @pytest.mark.asyncio
    async def test_retrieve(self):
        await store.database.connect()
        res = await store.Robot.retrieve({'robot_id': 1})
        assert res.name == 'GUIDO'
        await store.database.disconnect()
