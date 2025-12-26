import pytest
import os
import sys
from services.auth_service import AuthService
from database.connection import DatabaseConnection
from database.create_tables import create_tables

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
    """Set up clean database before each test"""
    
    db = DatabaseConnection()
    cursor = db.get_cursor()

    # تنظيف الجداول (بالترتيب عشان الـ FK)
    cursor.execute("DELETE FROM chat_messages")
    cursor.execute("DELETE FROM notifications")
    cursor.execute("DELETE FROM submissions")
    cursor.execute("DELETE FROM attendance")
    cursor.execute("DELETE FROM grade_summary")
    cursor.execute("DELETE FROM user_preferences")
    cursor.execute("DELETE FROM announcements")
    cursor.execute("DELETE FROM enrollment")
    cursor.execute("DELETE FROM assignments")
    cursor.execute("DELETE FROM lectures")
    cursor.execute("DELETE FROM courses")
    cursor.execute("DELETE FROM users")

    db.commit()

    # إنشاء الجداول (لو مش موجودة)
    create_tables()

    # Users ثابتين للاختبارات
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

