def test_signup_with_invalid_email(client):
    payload = {
        "email": "tester@example",
        "password": "strongpassword123"
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    data = response.json()
    
    assert response.status_code == 422
    assert 'detail' in data


def test_signup_sucess(client):
    payload = {
            "email": "tester@example.com",
            "password": "strongpassword123"
     }
    response = client.post("/api/v1/auth/signup", json=payload)   
    data =response.json()
    assert response.status_code == 201
    assert data["email"] == "tester@example.com"
    assert "id" in data
    assert data["is_active"] is True
    assert "password" not in data

def test_signup_duplicate_email(client,test_user):
    
    response = client.post("/api/v1/auth/signup", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == 'Email is already registered.'

def test_login_with_wrong_password(client, test_user):
    payload = {**test_user, 'password': 'pasword123'}

    response = client.post('/api/v1/auth/login',json=payload)
    data =response.json()
    assert response.status_code == 401
    assert data['detail'] == 'Invalid email or password'

def test_login_success(client,test_user):
       

    response = client.post('/api/v1/auth/login',json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_login_with_nonexistent_email(client):
    payload ={
         'email' :'newtester@example.com',
         'password' :'strongpassword123'
        }  

    response = client.post('/api/v1/auth/login',json=payload)
    assert response.status_code == 401
    data = response.json()  
    assert data['detail'] == 'Invalid email or password'

    
def test_get_current_user_without_token(client):
   response = client.get('/api/v1/auth/me')
   assert response.status_code == 401

def test_get_current_user_with_invalid_token(client):
    headers = {
        'Authorization':'Bearer invalid-token'
    }  
    response = client.get('/api/v1/auth/me' ,headers=headers)
    assert response.status_code == 401
    assert response.json()['detail'] == 'Could not validate credentials'

def test_get_current_user_with_valid_token(client, test_user):
    login_response = client.post('/api/v1/auth/login', json=test_user)
    assert login_response.status_code == 200
    access_token = login_response.json()['access_token']
    headers = {
        'Authorization' :f'Bearer {access_token}'
    }
    response = client.get('/api/v1/auth/me',headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['email'] == 'tester@example.com'
