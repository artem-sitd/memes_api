from pathlib import Path

import pytest

file_to_post = Path(__file__).parent / "index.png"
file_to_put = Path(__file__).parent / "nginx.png"
file_to_post2 = Path(__file__).parent / "poetry.jpeg"


@pytest.mark.asyncio(scope="session")
async def test_post_and_put_meme(client):
    # post
    response = await client.post(
        "/post_memes", files={"file": open(file_to_post, "rb")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response
    assert "src" in json_response
    assert json_response["description"] == "index.png"
    post_id_memes = json_response.get("id")

    # put
    response = await client.put(
        f"/put_memes/{post_id_memes}", files={"file": open(file_to_put, "rb")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response
    assert "src" in json_response
    assert json_response["description"] == "nginx.png"
    post_id_memes = json_response.get("id")

    # delete
    response = await client.delete(f"/delete_memes/{post_id_memes}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == {"message": f"Meme id: {post_id_memes} deleted"}


@pytest.mark.asyncio(scope="session")
async def test_post_and_get(client):
    # post
    response = await client.post(
        "/post_memes", files={"file": open(file_to_post2, "rb")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response
    assert "src" in json_response
    assert json_response["description"] == "poetry.jpeg"
    post_id_memes = json_response["id"]

    # get {id}
    response2 = await client.get(f"/get_memes/{post_id_memes}")
    assert response2.status_code == 200
    json_response2 = response2.json()
    assert "id" in json_response2
    assert "src" in json_response2
    assert json_response2["description"] == "poetry.jpeg"

    # post
    response = await client.post(
        "/post_memes", files={"file": open(file_to_post, "rb")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response
    assert "src" in json_response
    assert json_response["description"] == "index.png"
    post_id_memes = json_response.get("id")

    # get all
    response = await client.get("/get_memes")
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response["memes"][0]
    assert "src" in json_response["memes"][0]
    assert "page" in json_response
    assert "page_size" in json_response
    assert len(json_response["memes"]) == 2
    assert json_response["memes"][0]["description"] in ("index.png", "poetry.jpeg")
    assert json_response["memes"][1]["description"] in ("index.png", "poetry.jpeg")
