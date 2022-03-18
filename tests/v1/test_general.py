"""Test general API functionality."""


def test_healthcheck(client):
    """Test healthcheck."""
    response = client.get("/healthcheck")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("message") == "alive and kicking"
