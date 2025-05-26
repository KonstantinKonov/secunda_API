import pytest
from unittest.mock import AsyncMock

from src.services.building import BuildingService
from src.schemas import BuildingRead, BuildingCreate


@pytest.mark.asyncio
async def test_get_all_returns_list_of_buildings():
    mock_repo = AsyncMock()
    mock_repo.get_all.return_value = [
        BuildingRead(id=1, address="г. Санкт-Петербург, ул. Центральная 1", latitude=69.42, longitude=42.69)
    ]

    service = BuildingService(db=AsyncMock())
    service.repo = mock_repo

    result = await service.get_all()

    assert isinstance(result, list)
    assert result[0].id == 1
    mock_repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_returns_building():
    mock_repo = AsyncMock()
    mock_repo.get_one.return_value = BuildingRead(id=1, address="ул. Пушкина", latitude=1.0, longitude=2.0)

    service = BuildingService(db=AsyncMock())
    service.repo = mock_repo

    result = await service.get_by_id(1)

    assert result.id == 1
    assert result.address == "ул. Пушкина"
    mock_repo.get_one.assert_awaited_once_with(id=1)


@pytest.mark.asyncio
async def test_create_returns_created_building():
    mock_repo = AsyncMock()
    create_data = BuildingCreate(address="ул. Лесная", latitude=1.1, longitude=2.2)
    mock_repo.add.return_value = BuildingRead(id=5, **create_data.model_dump())

    service = BuildingService(db=AsyncMock())
    service.repo = mock_repo

    result = await service.create(create_data)

    assert result.id == 5
    assert result.address == "ул. Лесная"
    mock_repo.add.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_update_commits_and_returns_updated_building():
    mock_repo = AsyncMock()
    update_data = BuildingCreate(address="ул. Новая", latitude=3.3, longitude=4.4)

    service = BuildingService(db=AsyncMock())
    service.repo = mock_repo

    service.get_by_id = AsyncMock(return_value=BuildingRead(id=1, **update_data.model_dump()))

    result = await service.update(1, update_data)

    mock_repo.edit.assert_awaited_once_with(id=1, data=update_data)
    service.db.commit.assert_awaited_once()
    assert result.address == "ул. Новая"


@pytest.mark.asyncio
async def test_delete_executes_and_commits():
    mock_repo = AsyncMock()

    service = BuildingService(db=AsyncMock())
    service.repo = mock_repo

    await service.delete(2)

    mock_repo.delete.assert_awaited_once_with(id=2)
    service.db.commit.assert_awaited_once()
