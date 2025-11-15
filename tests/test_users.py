from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_users():
    # create
    r = client.post('/users/', json={'username': 'alice', 'full_name': 'Alice'})
    assert r.status_code == 201
    data = r.json()
    assert data['username'] == 'alice'

    # get
    r = client.get('/users/')
    assert r.status_code == 200
    assert any(u['username']=='alice' for u in r.json())