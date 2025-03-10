import pytest
import httpx


@pytest.fixture(scope="module")
def global_header():
    token_in_header = {"Authorization": ""}
    return token_in_header


@pytest.fixture(scope="module")
def global_fields():
    connect_fields = {
        "contract_id": "",
        "document_id": ""
    }
    return connect_fields


@pytest.mark.asyncio
async def test_auth_get_token(global_header):
    data = {
        "grant_type": "password",
        "username": "root",
        "password": "root",
        "client_id": "string",
        "client_secret": "string"
    }
    async with httpx.AsyncClient(base_url="http://127.0.0.0:8001") as client:
        response = await client.post("/api/v1/auth/token", data=data)
        response_json = response.json()
        token = response_json["access_token"]

        assert response.status_code == 200

        global_header["Authorization"] = f"Bearer {token}"


@pytest.mark.asyncio
async def test_upload_file(global_header):
    # загрузка файла
    test_file = ("test_file.txt", b"test content")

    async with httpx.AsyncClient(base_url="http://127.0.0.0:8001") as client:
        response = await client.post(
            "/api/v1/dbo/download_document",
            files={"file": test_file},
            headers=global_header
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["message"] == "File uploaded successfully"


@pytest.mark.asyncio
async def test_create_document(global_fields, global_header):
    data = {
        "name": "test_document",
        "discription": "test document for pytest",
        "path": "uploads/test.html",
        "user_id": "2fc61051-1775-4c54-bac6-1074c36e8c35"
    }

    async with httpx.AsyncClient(base_url="http://127.0.0.0:8001") as ac:
        response = await ac.post(
            "/api/v1/abc/",
            json=data,
            headers=global_header
        )
        responce_json = response.json()
        assert response.status_code == 201
        assert responce_json["user_id"] == "2fc61051-1775-4c54-bac6-1074c36e8c35"
        global_fields["document_id"] = responce_json["id"]


@pytest.mark.asyncio
async def test_create_contract(global_fields, global_header):
    data = {
        "name": "test_contract",
        "discription": "test contract for pytest",
        "user_id": "2fc61051-1775-4c54-bac6-1074c36e8c35"
    }

    async with httpx.AsyncClient(base_url="http://127.0.0.0:8001") as client:
        response = await client.post(
            "/api/v1/cm/",
            json=data,
            headers=global_header
        )
        responce_json = response.json()
        assert response.status_code == 201
        assert responce_json["user_id"] == "2fc61051-1775-4c54-bac6-1074c36e8c35"
        global_fields["contract_id"] = responce_json["id"]


@pytest.mark.asyncio
async def test_connect_contract_document(global_fields, global_header):

    data = {
        "contract_id": global_fields["contract_id"],
        "document_id": global_fields["document_id"]
    }

    async with httpx.AsyncClient(base_url="http://127.0.0.0:8001") as client:
        response = await client.post(
            "/api/v1/cm/connect_document",
            json=data,
            headers=global_header
        )
        assert response.status_code == 200
