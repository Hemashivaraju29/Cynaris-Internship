import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

API_PATH = Path(__file__).resolve().parents[1] / "api.py"
SPEC = importlib.util.spec_from_file_location("cia_api", API_PATH)
cia_api = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cia_api)
client = TestClient(cia_api.app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_and_count_csv():
    response = client.post(
        "/cia/upload",
        files={"file": ("sales.csv", "Region,Sales\nEast,100\nWest,200\n", "text/csv")},
    )
    assert response.status_code == 200
    session_id = response.json()["session_id"]

    result = client.post(
        "/cia/query",
        json={"session_id": session_id, "question": "How many rows?"},
    )
    assert result.status_code == 200
    assert result.json()["answer"] == 2


def test_reject_non_csv_file():
    response = client.post(
        "/cia/upload",
        files={"file": ("notes.txt", "hello", "text/plain")},
    )
    assert response.status_code == 400

def test_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_css_file_loads():
    response = client.get("/style.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


def test_javascript_file_loads():
    response = client.get("/script.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]