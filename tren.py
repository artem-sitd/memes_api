json_response = {"memes": [
    {
        "description": "poetry.jpeg",
        "id": 0
    },
    {
        "description": "index.png",
        "id": 1
    }]
}
print(json_response["memes"][0]["description"] in ("index.png", "poetry.jpeg"))
print(not json_response["memes"][2]["description"] in ("index.png", "poetry.jpeg"))
