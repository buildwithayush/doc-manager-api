def get_auth_header(client, email, password):
    client.post("/api/v1/auth/signup", json={"email": email, "password": password})
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_get_document(client,valid_pdf_bytes):
    headers = get_auth_header(client, "user1@example.com", "pass1234")
    file_payload = {"file": ("patch_test.pdf", valid_pdf_bytes, "application/pdf")}

    # Create
    res = client.post(
        "/api/v1/documents/upload",
        data={"title": "Doc 1", "description": "First Doc"},
        files=file_payload,
        headers=headers,
    )
    doc_id = res.json()['id']
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Doc 1"
    assert data["file_size"] == len(valid_pdf_bytes)
    assert "users/" in data["file_path"]
    assert "file_path" in data

    # Get Single
    get_res = client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Doc 1"

def test_patch_document_metadata(client,valid_pdf_bytes):
    headers = get_auth_header(client, "patch_tester@example.com", "password123")

    file_payload = {"file": ("patch_test.pdf", valid_pdf_bytes, "application/pdf")}
    upload_res = client.post(
        "/api/v1/documents/upload",
        data={"title": "Original Title", "description": "Original Description"},
        files=file_payload,
        headers=headers
    )
    doc_id = upload_res.json()["id"]

    patch_res = client.patch(
        f"/api/v1/documents/{doc_id}",
        json={"title": "Modified Title"},
        headers=headers
    )
    
    assert patch_res.status_code == 200
    updated_data = patch_res.json()
    assert updated_data["title"] == "Modified Title"
    assert updated_data["description"] == "Original Description"

def test_user_isolation(client,valid_pdf_bytes):
    headers_user1 = get_auth_header(client, "alice@example.com", "pass1234")
    headers_user2 = get_auth_header(client, "bob@example.com", "pass1234")

    file_payload = {"file": ("alice.pdf", valid_pdf_bytes, "application/pdf")}
    res = client.post(
        '/api/v1/documents/upload',
        data={'title': 'Alice Docs', 'description': 'This Is Alice Docs'},
        files=file_payload,
        headers=headers_user1
    )
    assert res.status_code == 201
    alice_doc_id = res.json()['id']

    bob_res = client.get(f'/api/v1/documents/{alice_doc_id}', headers=headers_user2)
    assert bob_res.status_code == 404
    assert bob_res.json()["detail"] == "Document not found"

def test_delete_document_and_storage_cleanup(client, valid_pdf_bytes):
    headers = get_auth_header(client, "deleter@example.com", "password123")

    file_payload = {"file": ("delete_test.pdf", valid_pdf_bytes, "application/pdf")}
    upload_res = client.post(
        "/api/v1/documents/upload",
        data={"title": "To Be Deleted", "description": "This document will be deleted."},
        files=file_payload,
        headers=headers
    )

    doc_id = upload_res.json()["id"]

    del_res = client.delete(f"/api/v1/documents/{doc_id}", headers=headers)
    assert del_res.status_code == 204   

    get_res = client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert get_res.status_code == 404
