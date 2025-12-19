import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from services.auth_service import AuthService

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(autouse=True)
def setup_database():
    """Set up database before each test"""
    from database.create_tables import create_tables
    create_tables()
    
    # Create test users
    auth_service = AuthService()
    auth_service.register_user("Teacher", "teacher@test.com", "pass123", "teacher")
    auth_service.register_user("Student", "student@test.com", "pass123", "student")
    yield

def test_login_flow(client):
    """Test complete login flow"""
    # Test login page loads
    response = client.get('/auth/login')
    assert response.status_code == 200
    
    # Test login with valid credentials
    response = client.post('/auth/login', data={
        'email': 'teacher@test.com',
        'password': 'pass123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_registration_flow(client):
    """Test complete registration flow"""
    # Test registration page loads
    response = client.get('/auth/register')
    assert response.status_code == 200
    
    # Test registration
    response = client.post('/auth/register', data={
        'name': 'New User',
        'email': 'newuser@test.com',
        'password': 'pass123',
        'role': 'student'
    }, follow_redirects=True)
    assert response.status_code == 200

