def get_auth_header(client, email, password):
    client.post("/api/v1/auth/signup", json={"email": email, "password": password})
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_get_document(client):
    headers = get_auth_header(client, "user1@example.com", "pass1234")
    
    # Create
    create_res = client.post("/api/v1/documents/", json={
        "title": "Doc 1",
        "description": "First Doc"
    }, headers=headers)
    assert create_res.status_code == 201
    doc_id = create_res.json()["id"]

    # Get Single
    get_res = client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Doc 1"

def test_user_isolation(client):
    headers_user1 = get_auth_header(client, "alice@example.com", "pass1234")
    headers_user2 = get_auth_header(client, "bob@example.com", "pass1234")

    payload = {
        'title' :'Alice Docs',
        'description': ''
     }
    res = client.post('/api/v1/documents',json =payload, headers = headers_user1)
    assert res.status_code == 201
    alice_doc_id = res.json()['id']

    bob_res = client.get(f'api/v1/documents/{alice_doc_id}',headers = headers_user2)
    assert bob_res.status_code == 404
    assert bob_res.json()["detail"] == "Document not found"
   