import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_listar_usuarios_unauthenticated():
    response = client.get("/usuarios/")
    assert response.status_code == 401