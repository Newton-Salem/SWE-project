import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from services.course_service import CourseService
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

@pytest.fixture
def test_users():
    """Create test users"""
    auth_service = AuthService()
    auth_service.register_user("Teacher", "teacher@test.com", "pass123", "teacher")
    auth_service.register_user("Student", "student@test.com", "pass123", "student")
    
    teacher = auth_service.authenticate("teacher@test.com", "pass123")
    student = auth_service.authenticate("student@test.com", "pass123")
    
    return {"teacher": teacher, "student": student}

def test_create_course(test_users):
    """Test course creation"""
    course_service = CourseService()
    course_service.create_course(
        test_users["teacher"].user_id, 
        "Test Course", 
        "TEST101", 
        "Test Description"
    )
    
    courses = course_service.get_teacher_courses(test_users["teacher"].user_id)
    assert len(courses) == 1
    assert courses[0].title == "Test Course"
    assert courses[0].code == "TEST101"

def test_join_course(test_users):
    """Test student joining a course"""
    course_service = CourseService()
    course_service.create_course(
        test_users["teacher"].user_id, 
        "Test Course", 
        "TEST101", 
        "Test Description"
    )
    
    success, message = course_service.join_course(test_users["student"].user_id, "TEST101")
    assert success is True
    
    student_courses = course_service.get_student_courses(test_users["student"].user_id)
    assert len(student_courses) == 1

def test_join_invalid_course(test_users):
    """Test joining with invalid course code"""
    course_service = CourseService()
    success, message = course_service.join_course(test_users["student"].user_id, "INVALID")
    assert success is False
    assert "Invalid" in message or "invalid" in message.lower()