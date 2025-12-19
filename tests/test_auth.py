import pytest
import os
import sys

# Add parent directory to path
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
    yield
    # Cleanup if needed

def test_user_registration():
    """Test user registration"""
    auth_service = AuthService()
    success, message = auth_service.register_user(
        "Test User", "test@example.com", "password123", "student"
    )
    assert success is True
    assert message == "Registered successfully"

def test_duplicate_email_registration():
    """Test that duplicate email registration fails"""
    auth_service = AuthService()
    auth_service.register_user("Test User", "test@example.com", "password123", "student")
    success, message = auth_service.register_user(
        "Another User", "test@example.com", "password456", "student"
    )
    assert success is False
    assert "already registered" in message.lower()

def test_user_authentication():
    """Test user authentication"""
    auth_service = AuthService()
    auth_service.register_user("Test User", "test@example.com", "password123", "student")
    
    user = auth_service.authenticate("test@example.com", "password123")
    assert user is not None
    assert user.email == "test@example.com"
    assert user.role == "student"

def test_wrong_password():
    """Test authentication with wrong password"""
    auth_service = AuthService()
    auth_service.register_user("Test User", "test@example.com", "password123", "student")
    
    user = auth_service.authenticate("test@example.com", "wrongpassword")
    assert user is None

def test_nonexistent_user():
    """Test authentication with non-existent user"""
    auth_service = AuthService()
    user = auth_service.authenticate("nonexistent@example.com", "password123")
    assert user is None

