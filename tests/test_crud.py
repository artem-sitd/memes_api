import pytest

from pathlib import Path

file_to_send = Path(__file__).parent / "index.png"


@pytest.mark.asyncio
async def test_create_meme(client, s3_client_test):
    response = await client.post("/post_memes",
                                 files={"file": open(file_to_send, 'rb')})
    print(f">>>>>>>>>>>>>>>>>>>{response.text}")
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response
    assert "src" in json_response
    assert json_response["description"] == "index.png"

# @pytest.mark.asyncio
# async def test_update_meme(client: AsyncClient, s3_client, setup_s3):
#     response = await client.post("/memes",
#                                  files={"file": ("image2_test.jpeg", b"test image content")},
#                                  data={"description": "test description"})
#     meme_id = response.json()["id"]
#     new_file = ("new_image.jpg", b"new image content")
#     new_description = "updated description"
#
#     response = await client.put(f"/memes/{meme_id}", files={"file": new_file}, data={"description": new_description})
#     assert response.status_code == status.HTTP_200_OK
#     json_response = response.json()
#     assert json_response["message"] == f"Meme {meme_id} updated successfully"
#     assert json_response["description"] == new_description
