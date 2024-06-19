import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_meme(client: AsyncClient, s3_client, setup_s3):
    response = await client.post("/memes", files={"file": ("test_image.jpg", b"test image content")},
                                 data={"description": "test description"})
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert "id" in json_response
    assert "s3_key" in json_response
    assert json_response["description"] == "test description"


@pytest.mark.asyncio
async def test_update_meme(client: AsyncClient, s3_client, setup_s3):
    # Create a meme first
    response = await client.post("/memes", files={"file": ("test_image.jpg", b"test image content")},
                                 data={"description": "test description"})
    meme_id = response.json()["id"]
    new_file = ("new_image.jpg", b"new image content")
    new_description = "updated description"

    response = await client.put(f"/memes/{meme_id}", files={"file": new_file}, data={"description": new_description})
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response["message"] == f"Meme {meme_id} updated successfully"
    assert json_response["description"] == new_description
