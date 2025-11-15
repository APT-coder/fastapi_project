from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_items():
    r = client.post('/items/', json={'title': 'Item 1', 'description':'desc1'})
    assert r.status_code == 201
    data = r.json()
    assert data['title'] == 'Item 1'

    r = client.get('/items/')
    assert r.status_code == 200
    assert any(i['title']=='Item 1' for i in r.json())