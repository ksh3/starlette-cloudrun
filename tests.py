import pytest
from starlette.testclient import TestClient
from databases import Database, DatabaseURL

from main import app
from src import store, config


class TestView:

    def test_repair(self):
        with TestClient(app) as client:
            response = client.post(
                "/v1/robots/repair", data={"robot_id": 1}
            )
            assert response.status_code == 200

    def test_retrieve(self):
        with TestClient(app) as client:
            response = client.get("/v1/robots/1")
            assert response.status_code == 200


class TestModel:

    def setup_method(self, method):
        store.database.url = DatabaseURL(config.TEST_DATABASE_URL)
        self.test_db: Database = store.database

    @pytest.mark.asyncio
    async def test_retrieve(self):
        await self.test_db.connect()
        res = await store.Robot.retrieve({'robot_id': 1})
        assert res.name == 'GUIDO'
        await self.test_db.disconnect()

    @pytest.mark.asyncio
    async def test_count(self):
        await self.test_db.connect()
        old_robot = await store.Robot.retrieve({'robot_id': 1})
        await old_robot.count_ref()
        new_robot = await store.Robot.retrieve({'robot_id': 1})
        assert old_robot.count + 1 == new_robot.count
        await self.test_db.disconnect()
