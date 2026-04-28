import sys
import os

sys.path.insert(0, os.getcwd())

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_student():
    response = client.post("/auth/register", json={
        "username": "student1",
        "password": "123456",
        "role": "student"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_login_student():
    client.post("/auth/register", json={
        "username": "student2",
        "password": "123456",
        "role": "student"
    })

    response = client.post("/auth/login", json={
        "username": "student2",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_wrong_login():
    response = client.post("/auth/login", json={
        "username": "wrong",
        "password": "wrong"
    })

    assert response.status_code == 401


def test_protected_route_without_token():
    response = client.get("/profile")

    assert response.status_code == 401


def test_student_cannot_create_exam():
    client.post("/auth/register", json={
        "username": "student3",
        "password": "123456",
        "role": "student"
    })

    login = client.post("/auth/login", json={
        "username": "student3",
        "password": "123456"
    })

    token = login.json()["access_token"]

    response = client.post("/exams", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 403


def test_admin_can_create_exam():
    client.post("/auth/register", json={
        "username": "admin1",
        "password": "123456",
        "role": "admin"
    })

    login = client.post("/auth/login", json={
        "username": "admin1",
        "password": "123456"
    })

    token = login.json()["access_token"]

    response = client.post("/exams", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200