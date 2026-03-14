def test_get_spotify_mock_data(client):
    response = client.get("/api/spotify/artist/frank-ocean")
    assert response.status_code == 200
    assert "Frank Ocean" in response.json()["name"]
